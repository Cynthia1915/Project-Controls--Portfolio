"""Read Primavera P6 XER tables and export raw activity/relationship CSVs.

No external dependencies. Keeps original column names and values, and does not
claim to calculate critical path or scheduling metrics.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_xer(path: Path):
    """Yield (table_name, record_dict) for XER %R rows.

    XER files are tab-delimited, with %T table markers and %F field markers.
    Empty field values are preserved; excess values cause an explicit error.
    """
    table = None
    fields = None
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as stream:
        for line_no, raw in enumerate(stream, 1):
            parts = raw.rstrip("\r\n").split("\t")
            marker = parts[0]
            if marker == "%T":
                if len(parts) < 2 or not parts[1]:
                    raise ValueError(f"{path}:{line_no}: missing table name")
                table, fields = parts[1], None
            elif marker == "%F":
                if table is None:
                    raise ValueError(f"{path}:{line_no}: field header without table")
                fields = parts[1:]
                if not fields or any(not x for x in fields):
                    raise ValueError(f"{path}:{line_no}: invalid field header")
            elif marker == "%R":
                if table is None or fields is None:
                    raise ValueError(f"{path}:{line_no}: record without table/header")
                values = parts[1:]
                if len(values) > len(fields):
                    raise ValueError(f"{path}:{line_no}: too many record values")
                values.extend([""] * (len(fields) - len(values)))
                yield table, dict(zip(fields, values))
            elif marker in ("%I", "%E", ""):
                continue


def export_records(paths: list[Path], output_dir: Path) -> dict[str, int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {"TASK": "Activities.csv", "TASKPRED": "Relationships.csv"}
    records = {key: [] for key in tables}
    for path in paths:
        for table, record in read_xer(path):
            if table in records:
                records[table].append({
                    "Scenario": path.stem,
                    "Source_File": path.name,
                    **record,
                })
    counts = {}
    for table, filename in tables.items():
        rows = records[table]
        headers = list(dict.fromkeys(key for row in rows for key in row))
        with (output_dir / filename).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        counts[table] = len(rows)
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Directory of XER files")
    parser.add_argument("--output", type=Path, required=True, help="CSV output directory")
    args = parser.parse_args()
    paths = sorted(args.input.glob("*.xer"))
    if not paths:
        parser.error(f"No .xer files found in {args.input}")
    counts = export_records(paths, args.output)
    for table, count in counts.items():
        print(f"{table}: {count} rows across {len(paths)} source files")


if __name__ == "__main__":
    main()
