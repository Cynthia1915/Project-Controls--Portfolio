#!/usr/bin/env python3
"""Read-only Primavera P6 XER schedule health checks for DC-HYP-FINAL-6.

Usage:
  python audit_xer.py path/to/update01.xer --output-dir audit_outputs
No P6 records are modified. This is not a CPM engine or DCMA certification.
"""
import argparse
import csv
import json
from collections import Counter, defaultdict, deque
from datetime import datetime
from pathlib import Path

def read_xer(path):
    raw = Path(path).read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1252")
    tables = defaultdict(list)
    table, fields = None, []
    for line in text.splitlines():
        parts = line.split("\t")
        tag = parts[0]
        if tag == "%T":
            table, fields = (parts[1] if len(parts) > 1 else None), []
        elif tag == "%F":
            fields = parts[1:]
        elif tag == "%R" and table and fields:
            values = parts[1:]
            if len(values) != len(fields):
                raise ValueError(f"{table}: expected {len(fields)} fields, got {len(values)}")
            tables[table].append(dict(zip(fields, values)))
    return tables

def amount(v):
    try:
        return float(v or 0)
    except (ValueError, TypeError):
        return 0.0

def date(v):
    if not v:
        return None
    return datetime.strptime(v[:16], "%Y-%m-%d %H:%M")

def audit(tables):
    tasks = tables["TASK"]
    preds = tables["TASKPRED"]
    projects = tables["PROJECT"]
    costs = tables["PROJCOST"]
    if not tasks:
        raise ValueError("No TASK table found")
    if len(projects) != 1:
        raise ValueError("Expected one project; split multi-project exports before auditing")
    project = projects[0]
    data_date = date(project.get("last_recalc_date", ""))
    ids = {t["task_id"] for t in tasks}
    codes = [t["task_code"] for t in tasks]
    findings = []
    def flag(code, severity, activity, detail):
        findings.append(dict(check=code, severity=severity, activity_id=activity, detail=detail))

    if len(codes) != len(set(codes)):
        flag("DUPLICATE_ACTIVITY_ID", "HIGH", "", "Duplicate task_code values")
    incoming, outgoing = Counter(), Counter()
    adjacency = defaultdict(set)
    edge_keys = Counter()
    types = Counter()
    positive_lags = 0
    negative_lags = 0
    for p in preds:
        src, dst = p.get("pred_task_id", ""), p.get("task_id", "")
        typ = p.get("pred_type", "")
        lag = amount(p.get("lag_hr_cnt"))
        types[typ] += 1
        edge_keys[(src, dst, typ)] += 1
        if src not in ids or dst not in ids:
            flag("INVALID_REFERENCE", "HIGH", "", f"predecessor={src}, successor={dst}")
            continue
        incoming[dst] += 1
        outgoing[src] += 1
        adjacency[src].add(dst)
        if src == dst:
            flag("SELF_LINK", "HIGH", "", f"task_id={src}")
        if lag > 0:
            positive_lags += 1
            flag("POSITIVE_LAG_REVIEW", "REVIEW", next((t["task_code"] for t in tasks if t["task_id"] == dst), ""), f"{typ} lag={lag} hours; predecessor task_id={src}")
        elif lag < 0:
            negative_lags += 1
            flag("NEGATIVE_LAG", "HIGH", "", f"predecessor={src}, successor={dst}, lag={lag}h")
    for key, count in edge_keys.items():
        if count > 1:
            flag("DUPLICATE_RELATIONSHIP", "MEDIUM", "", f"{key}: {count} identical records")
    indegree = {i: 0 for i in ids}
    for src, successors in adjacency.items():
        for dst in successors:
            indegree[dst] += 1
    queue = deque(i for i, n in indegree.items() if n == 0)
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for successor in adjacency[node]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                queue.append(successor)
    if visited < len(ids):
        flag("CYCLIC_LOGIC", "HIGH", "", f"{len(ids) - visited} nodes not topologically resolved")
    states = Counter()
    for t in tasks:
        code = t["task_code"]
        state = t.get("status_code", "")
        states[state] += 1
        start = date(t.get("act_start_date", ""))
        finish = date(t.get("act_end_date", ""))
        remaining = amount(t.get("remain_drtn_hr_cnt"))
        if not incoming[t["task_id"]]:
            flag("OPEN_START", "REVIEW", code, "No predecessor")
        if not outgoing[t["task_id"]]:
            flag("OPEN_FINISH", "REVIEW", code, "No successor")
        if state == "TK_Complete" and (not start or not finish or remaining > 0):
            flag("COMPLETE_STATUS_CONFLICT", "HIGH", code, f"actual start={start}, finish={finish}, remaining hours={remaining}")
        if state == "TK_Active" and (not start or finish):
            flag("ACTIVE_STATUS_CONFLICT", "HIGH", code, f"actual start={start}, finish={finish}")
        if state == "TK_NotStart" and (start or finish):
            flag("NOT_STARTED_ACTUALS", "HIGH", code, f"actual start={start}, finish={finish}")
        if start and finish and finish < start:
            flag("REVERSED_ACTUAL_DATES", "HIGH", code, "Actual finish precedes actual start")
        if data_date and any(d and d > data_date for d in (start, finish)):
            flag("ACTUAL_AFTER_DATA_DATE", "HIGH", code, "Actual date later than project data date")
        if t.get("cstr_type", "") not in ("", "CS_MEO", "CS_ALAP"):
            flag("CONSTRAINT_REVIEW", "REVIEW", code, f"constraint type={t['cstr_type']}")
    target = sum(amount(c.get("target_cost")) for c in costs)
    actual = sum(amount(c.get("act_cost")) for c in costs)
    if target > 0 and actual == 0 and (states["TK_Complete"] or states["TK_Active"]):
        flag("ZERO_P6_ACTUAL_COST", "HIGH", "", "Progress exists but P6 expense actual costs are zero. Reconcile external AC; do not invent actuals.")
    summary = {
        "project_id": project.get("proj_short_name", ""),
        "data_date": project.get("last_recalc_date", ""),
        "activities": len(tasks),
        "relationships": len(preds),
        "relationship_types": dict(types),
        "positive_lag_links": positive_lags,
        "negative_lag_links": negative_lags,
        "activity_statuses": dict(states),
        "wbs_elements": len(tables["PROJWBS"]),
        "expense_records": len(costs),
        "target_expense_cost": round(target, 2),
        "actual_expense_cost": round(actual, 2),
        "checks": dict(Counter(f["check"] for f in findings)),
        "limitations": "Read-only structural checks. No P6 rescheduling, resource leveling, driving-path or earned-value verification."
    }
    return summary, findings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("xer", help="Primavera P6 .xer file")
    parser.add_argument("--output-dir", default="audit_outputs")
    args = parser.parse_args()
    summary, findings = audit(read_xer(args.xer))
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "schedule_audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with (out / "schedule_audit_findings.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["check", "severity", "activity_id", "detail"])
        writer.writeheader()
        writer.writerows(findings)
    print(json.dumps(summary, indent=2))
    print(f"Written: {out / 'schedule_audit_findings.csv'}")

if __name__ == "__main__":
    main()
