"""Deterministic synthetic construction EVM case study. Python standard library only."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

BAC = 50_000_000
ACCOUNTS = [
    ("CA-01", "Civil and foundations", 9_000_000),
    ("CA-02", "Superstructure", 16_000_000),
    ("CA-03", "MEP systems", 13_000_000),
    ("CA-04", "Envelope and finishes", 9_000_000),
    ("CA-05", "Testing and commissioning", 3_000_000),
]
# Each tuple: monthly incremental planned, earned, actual value in USD millions.
PERIODS = [
    (1.2, 1.1, 1.2), (1.8, 1.6, 1.9), (2.5, 2.2, 2.6),
    (3.2, 2.8, 3.3), (3.8, 3.4, 4.0), (4.4, 3.9, 4.6),
    (4.8, 4.1, 4.9), (5.0, 4.5, 5.4), (5.2, 4.7, 5.6),
    (5.2, 4.5, 5.5), (6.0, 5.1, 6.3), (6.9, 5.8, 7.2),
]

def safe_ratio(numerator: float, denominator: float) -> float | None:
    return numerator / denominator if denominator > 0 else None

def calculate(bac: float, pv: float, ev: float, ac: float) -> dict:
    if bac <= 0 or min(pv, ev, ac) < 0 or ev > bac or pv > bac:
        raise ValueError("Invalid BAC or cumulative values")
    cpi = safe_ratio(ev, ac)
    spi = safe_ratio(ev, pv)
    eac_cpi = bac / cpi if cpi else None
    eac_budget = ac + (bac - ev)
    eac_joint = ac + (bac - ev) / (cpi * spi) if cpi and spi else None
    tcpi = safe_ratio(bac - ev, bac - ac)
    return {
        "bac": bac, "pv": pv, "ev": ev, "ac": ac,
        "cv": ev - ac, "sv": ev - pv, "cpi": cpi, "spi": spi,
        "eac_cpi": eac_cpi, "eac_remaining_at_budget": eac_budget,
        "eac_cpi_spi": eac_joint,
        "etc_cpi": eac_cpi - ac if eac_cpi is not None else None,
        "vac_cpi": bac - eac_cpi if eac_cpi is not None else None,
        "tcpi_bac": tcpi,
    }

def build_rows() -> list[dict]:
    if sum(b for _, _, b in ACCOUNTS) != BAC:
        raise ValueError("Control account budgets do not reconcile to BAC")
    if abs(sum(p[0] for p in PERIODS) - BAC / 1_000_000) > 1e-9:
        raise ValueError("Final planned value must reconcile to BAC")
    rows = []
    pv = ev = ac = 0.0
    for month, (p, e, a) in enumerate(PERIODS, start=1):
        pv += round(p * 1_000_000)
        ev += round(e * 1_000_000)
        ac += round(a * 1_000_000)
        row = calculate(BAC, pv, ev, ac)
        row.update({"month": month, "period_pv": round(p * 1_000_000),
                    "period_ev": round(e * 1_000_000), "period_ac": round(a * 1_000_000)})
        rows.append(row)
    return rows

def write_outputs(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    with (destination / "monthly_evm.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["month", "period_pv", "period_ev", "period_ac"] +
                                list(calculate(BAC, 0, 0, 0).keys()))
        writer.writeheader()
        writer.writerows(rows)
    with (destination / "control_accounts.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["account_id", "work_package", "bac_usd"])
        writer.writerows(ACCOUNTS)
    with (destination / "summary.json").open("w", encoding="utf-8") as f:
        json.dump({"case_id": "EVM-CF-001", "synthetic": True, "latest": rows[-1],
                   "months": len(rows), "accounts": len(ACCOUNTS)}, f, indent=2)
        f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic EVM scenario outputs")
    parser.add_argument("--output", default=str(Path(__file__).resolve().parents[1] / "outputs"))
    args = parser.parse_args()
    write_outputs(Path(args.output))
    print(f"EVM outputs written to {args.output}")
