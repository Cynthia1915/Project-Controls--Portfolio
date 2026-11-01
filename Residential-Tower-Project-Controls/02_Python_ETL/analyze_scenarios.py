"""Reproducible four-scenario XER audit and recovery comparison.

Usage:
 python 02_Python_ETL/analyze_scenarios.py --input 01_P6_Exports --output 03_Processed_Data

Uses Primavera PROJECT.scd_end_date (stored P6 forecast) and TASK/TASKPRED
records. Does not recompute CPM or claim resource feasibility.
"""
from __future__ import annotations
import argparse
import csv
from datetime import datetime
from pathlib import Path
from collections import Counter

SCENARIOS = {
    "Baseline": "RES-TWR-BL01.xer",
    "Update 01": "RES-TWR-UPD01.xer",
    "Recovery A": "RES-TWR-REC-A.xer",
    "Recovery B": "RES-TWR-REC-B.xer",
}
STATUSES = {"TK_Complete": "Completed", "TK_Active": "In Progress",
            "TK_NotStart": "Not Started"}


def records(path):
    table = None
    fields = None
    with path.open(encoding="utf-8-sig", errors="replace", newline="") as handle:
        for number, line in enumerate(handle, 1):
            parts = line.rstrip("\r\n").split("\t")
            kind = parts[0]
            if kind == "%T":
                table, fields = parts[1], None
            elif kind == "%F":
                fields = parts[1:]
            elif kind == "%R":
                if not table or not fields:
                    raise ValueError(f"{path}:{number}: record without table or fields")
                vals = parts[1:]
                if len(vals) > len(fields):
                    raise ValueError(f"{path}:{number}: unexpected columns")
                yield table, dict(zip(fields, vals + [""] * (len(fields)-len(vals))))


def load(path):
    tables = {"PROJECT": [], "TASK": [], "TASKPRED": []}
    for table, record in records(path):
        if table in tables:
            tables[table].append(record)
    if len(tables["PROJECT"]) != 1:
        raise ValueError(f"{path}: expected one PROJECT, got {len(tables['PROJECT'])}")
    return tables


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def edge_set(tables):
    ids = {r["task_id"]: r["task_code"] for r in tables["TASK"]}
    edges = set()
    for r in tables["TASKPRED"]:
        predecessor = ids.get(r["pred_task_id"])
        successor = ids.get(r["task_id"])
        if not predecessor or not successor:
            raise ValueError("Relationship references missing TASK ID")
        edges.add((predecessor, successor, r["pred_type"],
                   float(r.get("lag_hr_cnt") or 0)))
    return edges


def run(inputs, output):
    loaded = {}
    for label, filename in SCENARIOS.items():
        path = inputs / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing {path}; use original XER export")
        loaded[label] = load(path)
    finishes = {}
    summary = []
    activity_rows = []
    relationship_rows = []
    for label, tables in loaded.items():
        project = tables["PROJECT"][0]
        finish = datetime.fromisoformat(project["scd_end_date"])
        finishes[label] = finish
        statuses = Counter(x["status_code"] for x in tables["TASK"])
        if any(x not in STATUSES for x in statuses):
            raise ValueError(f"Unknown status in {label}: {statuses}")
        float_values = [float(x["total_float_hr_cnt"])
                        for x in tables["TASK"] if x.get("total_float_hr_cnt")]
        summary.append({
            "Scenario": label, "Project_ID": project.get("proj_short_name", ""),
            "Scheduled_Finish": finish.isoformat(sep=" "),
            "Activities": len(tables["TASK"]),
            "Relationships": len(tables["TASKPRED"]),
            "Completed": statuses["TK_Complete"],
            "In_Progress": statuses["TK_Active"],
            "Not_Started": statuses["TK_NotStart"],
            "Nonpositive_Float_Activities": sum(x <= 0 for x in float_values),
            "Delay_vs_Baseline_Calendar_Days": (finish - finishes["Baseline"]).days
                if "Baseline" in finishes else 0,
            "Recovery_vs_Update_Calendar_Days": "",
        })
        for row in tables["TASK"]:
            activity_rows.append({"Scenario": label, **row})
        for row in tables["TASKPRED"]:
            relationship_rows.append({"Scenario": label, **row})
    for row in summary:
        row["Delay_vs_Baseline_Calendar_Days"] = (
            finishes[row["Scenario"]] - finishes["Baseline"]).days
        row["Recovery_vs_Update_Calendar_Days"] = (
            finishes["Update 01"] - finishes[row["Scenario"]]).days if (
                row["Scenario"].startswith("Recovery")) else ""
    write_csv(output / "Scenario_Summary.csv", summary, list(summary[0]))
    for name, rows in (("Activities.csv", activity_rows),
                       ("Relationships.csv", relationship_rows)):
        fields = list(dict.fromkeys(key for row in rows for key in row))
        write_csv(output / name, rows, fields)
    baseline = {r["task_code"]: r for r in loaded["Update 01"]["TASK"]}
    base_edges = edge_set(loaded["Update 01"])
    changes, edges = [], []
    for label in ("Recovery A", "Recovery B"):
        tasks = {r["task_code"]: r for r in loaded[label]["TASK"]}
        if set(tasks) != set(baseline):
            raise ValueError(f"Activity code mismatch in {label}")
        for code in sorted(tasks):
            old, new = baseline[code], tasks[code]
            old_d = float(old.get("target_drtn_hr_cnt") or 0)
            new_d = float(new.get("target_drtn_hr_cnt") or 0)
            if old_d != new_d:
                changes.append({
                    "Scenario": label, "Activity_ID": code,
                    "Activity_Name": new.get("task_name", ""),
                    "Update_Duration_Hours": old_d,
                    "Recovery_Duration_Hours": new_d,
                    "Duration_Change_Hours": new_d - old_d})
        scenario_edges = edge_set(loaded[label])
        for action, values in (("Added", scenario_edges-base_edges),
                               ("Removed", base_edges-scenario_edges)):
            for pred, succ, rel, lag in sorted(values):
                edges.append({"Scenario": label, "Change": action,
                              "Predecessor_ID": pred, "Successor_ID": succ,
                              "Relationship_Type": rel, "Lag_Hours": lag})
    write_csv(output / "Duration_Changes.csv", changes, [
        "Scenario", "Activity_ID", "Activity_Name", "Update_Duration_Hours",
        "Recovery_Duration_Hours", "Duration_Change_Hours"])
    write_csv(output / "Logic_Changes.csv", edges, [
        "Scenario", "Change", "Predecessor_ID", "Successor_ID",
        "Relationship_Type", "Lag_Hours"])
    return summary, changes, edges


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary, durations, edges = run(args.input, args.output)
    for row in summary:
        print(f"{row['Scenario']}: {row['Activities']} activities, "
              f"{row['Relationships']} relationships, finish {row['Scheduled_Finish']}")
    print(f"Duration changes: {len(durations)}; logic changes: {len(edges)}")


if __name__ == "__main__":
    main()
