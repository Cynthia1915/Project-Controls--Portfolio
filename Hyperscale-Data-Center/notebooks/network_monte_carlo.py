#!/usr/bin/env python3
"""Reproducible, calendar-simplified CPM Monte Carlo on a single-project P6 XER.

Uses working-hour durations/relationship lags as continuous hours, NOT a P6
calendar-aware schedule. Actual dates, out-of-sequence progress, constraints,
resources and P6 scheduling options are not reconstructed. Do not compare
absolute dates to contractual RFS without independent P6 reconciliation.
"""
import argparse
import csv
import json
import math
import random
from collections import defaultdict, deque
from pathlib import Path
from audit_xer import read_xer


def number(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric field: {value!r}") from exc


def network(tables):
    tasks = tables["TASK"]
    if not tasks or len(tables["PROJECT"]) != 1:
        raise ValueError("Requires TASK and exactly one PROJECT record")
    ids = [t["task_id"] for t in tasks]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate internal task_id")
    by_id = {t["task_id"]: t for t in tasks}
    code = {k: v["task_code"] for k, v in by_id.items()}
    if len(set(code.values())) != len(code):
        raise ValueError("Duplicate task_code")
    incoming = defaultdict(list)
    following = defaultdict(list)
    indegree = {k: 0 for k in ids}
    for r in tables["TASKPRED"]:
        pred, succ = r["pred_task_id"], r["task_id"]
        if pred not in by_id or succ not in by_id:
            raise ValueError(f"Unknown predecessor/successor: {pred} -> {succ}")
        typ = r["pred_type"].removeprefix("PR_")
        if typ not in ("FS", "SS", "FF", "SF"):
            raise ValueError(f"Unsupported relationship type: {typ}")
        lag = number(r.get("lag_hr_cnt"))
        incoming[succ].append((pred, typ, lag))
        following[pred].append(succ)
        indegree[succ] += 1
    q = deque(sorted((k for k in ids if indegree[k] == 0), key=lambda k: code[k]))
    order = []
    while q:
        k = q.popleft()
        order.append(k)
        for s in following[k]:
            indegree[s] -= 1
            if indegree[s] == 0:
                q.append(s)
    if len(order) != len(ids):
        raise ValueError("Cycle in activity logic")
    duration = {}
    for k, t in by_id.items():
        field = "remain_drtn_hr_cnt" if t.get("status_code") in ("TK_Active", "TK_Complete") else "target_drtn_hr_cnt"
        value = number(t.get(field))
        if value < 0:
            raise ValueError(f"Negative duration for {code[k]}")
        duration[k] = 0 if t.get("status_code") == "TK_Complete" else value
    return order, code, incoming, duration


def forward(order, incoming, durations):
    starts, finishes = {}, {}
    for k in order:
        d = durations[k]
        s = 0.0
        for pred, typ, lag in incoming[k]:
            # Generalized precedence lower bounds on successor start.
            candidate = {"FS": finishes[pred] + lag,
                         "SS": starts[pred] + lag,
                         "FF": finishes[pred] + lag - d,
                         "SF": starts[pred] + lag - d}[typ]
            s = max(s, candidate)
        starts[k], finishes[k] = s, s + d
    return starts, finishes


def simulate(tables, runs=1000, seed=42, low=0.8, high=1.3, target_code="RFS-040"):
    if runs < 1 or not (0 < low <= 1 <= high):
        raise ValueError("Require runs >= 1 and 0 < low <= 1 <= high")
    order, codes, incoming, nominal = network(tables)
    target_ids = [k for k, c in codes.items() if c == target_code]
    if len(target_ids) != 1:
        raise ValueError(f"Target milestone {target_code!r} not uniquely found")
    target = target_ids[0]
    rng = random.Random(seed)
    values = []
    # Mode=1.0; triangular min/max are illustrative independent duration multipliers.
    for _ in range(runs):
        durations = {k: (rng.triangular(low, high, 1.0) * v if v else 0.0)
                     for k, v in nominal.items()}
        _, finishes = forward(order, incoming, durations)
        values.append(finishes[target])
    values.sort()
    _, nominal_finishes = forward(order, incoming, nominal)
    def quantile(p):
        pos = (len(values) - 1) * p
        lo, hi = math.floor(pos), math.ceil(pos)
        return values[lo] + (values[hi] - values[lo]) * (pos - lo)
    return {"activity_count": len(order), "relationships": len(tables["TASKPRED"]),
            "target_milestone": target_code, "runs": runs, "seed": seed,
            "duration_multiplier": {"min": low, "mode": 1.0, "max": high},
            "nominal_relative_work_hours": round(nominal_finishes[target], 2),
            "p50_relative_work_hours": round(quantile(.50), 2),
            "p80_relative_work_hours": round(quantile(.80), 2),
            "p90_relative_work_hours": round(quantile(.90), 2),
            "min_relative_work_hours": round(values[0], 2),
            "max_relative_work_hours": round(values[-1], 2),
            "limitations": "Continuous-hour precedence model only; not P6 calendar-aware or contractual finish-date confidence."}, values


def main():
    p = argparse.ArgumentParser()
    p.add_argument("xer")
    p.add_argument("--runs", type=int, default=1000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--target", default="RFS-040")
    p.add_argument("--output-dir", default="risk_outputs")
    args = p.parse_args()
    summary, values = simulate(read_xer(args.xer), runs=args.runs, seed=args.seed, target_code=args.target)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "network_risk_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with (out / "network_risk_samples.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["run_sorted", "relative_work_hours"])
        w.writerows(enumerate(values, start=1))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
