#!/usr/bin/env python3
"""Read-only EVM reconciliation for a normalized, single-period activity CSV.

Required columns: activity_id, data_date, bac, pv, ev, ac.
Inputs must be synthetic/modelled or separately validated. This does not
extract native P6 earned value and does not rewrite dashboard/workbooks.
"""
import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


def reconcile(rows, selected_date, expected_bac=120_000_000, tolerance=0.01):
    chosen = [r for r in rows if r["data_date"] == selected_date]
    if not chosen:
        raise ValueError(f"No rows for data date {selected_date}")
    seen = set()
    sums = defaultdict(float)
    for row in chosen:
        key = row["activity_id"]
        if key in seen:
            raise ValueError(f"Duplicate activity in reporting period: {key}")
        seen.add(key)
        for name in ("bac", "pv", "ev", "ac"):
            try:
                value = float(row[name])
            except (ValueError, KeyError, TypeError) as exc:
                raise ValueError(f"Invalid {name} for {key}") from exc
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"Non-finite or negative {name} for {key}")
            sums[name] += value
    bac, pv, ev, ac = (sums[x] for x in ("bac", "pv", "ev", "ac"))
    def ratio(a, b):
        return round(a / b, 6) if b else None
    cpi, spi = ratio(ev, ac), ratio(ev, pv)
    eac = bac / (ev / ac) if ev > 0 and ac > 0 else None
    return {
        "data_date": selected_date, "activity_count": len(chosen),
        "bac": round(bac, 2), "pv": round(pv, 2),
        "ev": round(ev, 2), "ac": round(ac, 2),
        "cpi": cpi, "spi": spi,
        "cost_variance": round(ev - ac, 2),
        "schedule_variance_value": round(ev - pv, 2),
        "eac_cpi_based": round(eac, 2) if eac is not None else None,
        "etc_cpi_based": round(eac - ac, 2) if eac is not None else None,
        "vac_cpi_based": round(bac - eac, 2) if eac is not None else None,
        "expected_bac": expected_bac,
        "bac_reconciles": abs(bac - expected_bac) <= tolerance,
        "assurance": "External modeled EVM only; does not verify native P6 AC or dashboard figures."
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv_file", help="Normalized per-activity EVM input CSV")
    p.add_argument("--date", required=True, help="YYYY-MM-DD data date")
    p.add_argument("--expected-bac", type=float, default=120_000_000)
    p.add_argument("--output", default="evm_reconciliation.json")
    args = p.parse_args()
    with open(args.csv_file, newline="", encoding="utf-8-sig") as f:
        result = reconcile(csv.DictReader(f), args.date, args.expected_bac)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["bac_reconciles"]:
        raise SystemExit("BAC check failed: inspect reporting-period data")


if __name__ == "__main__":
    main()
