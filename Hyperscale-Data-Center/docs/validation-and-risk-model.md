# Reproducible validation and schedule-risk prototype

This folder contains three **separate** read-only tools:

| Tool | Input | Output | Status |
| --- | --- | --- | --- |
| `audit_xer.py` | Single-project P6 XER | Structural QA JSON/CSV | Source provided; P6 equivalence not claimed |
| `reconcile_evm.py` | Normalized activity-level CSV with `activity_id,data_date,bac,pv,ev,ac` | Period-specific KPI reconciliation JSON | Independent EVM calculator; **not yet reconciled to the published workbook** |
| `network_monte_carlo.py` | Single-project P6 XER | CPM-like finish distribution JSON/CSV | Network-aware **continuous-hour prototype**, not a calendar-aware P6 model |

## Reproduce the checks

Requires Python 3.9+; standard library only.

```bash
python -m unittest discover -s Hyperscale-Data-Center/notebooks/tests -v
python Hyperscale-Data-Center/notebooks/audit_xer.py /path/to/Update01.xer --output-dir audit_outputs
python Hyperscale-Data-Center/notebooks/network_monte_carlo.py /path/to/Update01.xer --runs 1000 --seed 42 --target RFS-040 --output-dir risk_outputs
python Hyperscale-Data-Center/notebooks/reconcile_evm.py /path/to/normalized_evm.csv --date 2026-01-31 --expected-bac 120000000 --output evm_reconciliation.json
```

The automated unit tests cover FS/FF/SS precedence, cycles, missing references, fixed-seed reproducibility, period filtering, EVM ratios, duplicates and zero denominators. GitHub Actions runs them on relevant changes. **A passing unit test does not establish that a published workbook/dashboard reconciles.**

## EVM validation requirements

The reporting workbook must be exported or mapped into the normalized CSV schema. For each data date, the activity-level BAC should sum to USD 120M **only if the source uses a full-budget per-activity allocation**; otherwise map the authoritative budget register. Calculate project CPI from `sum(EV)/sum(AC)` and SPI from `sum(EV)/sum(PV)`, never averages of activity ratios. Compare resulting values against each dashboard KPI with explicit tolerances, record differences, and explain source assumptions. Do not substitute P6 PROJCOST zero actuals for modeled external AC. **The existing workbook and dashboards have not been automatically validated by this change.**

## Schedule-risk interpretation

The Monte Carlo tool uses the XER TASK/TASKPRED graph and supports FS, SS, FF and SF relationships with lags. It performs a topological forward pass for each independent triangular duration sample. The FF zero-duration RFS finish milestone is supported. A fixed random seed produces repeatable results.

**Material limitations:** It treats P6 hour quantities as continuous hours without multiple calendars, weekends, holidays, time-of-day rules, constraints, actual-date anchoring, progress override/retained logic, resource leveling or full P6 scheduling behavior. Completed activities are zeroed and active activities use remaining hours, but the graph is **not** anchored to the P6 data date. Thus the output is *relative modeled working-hour exposure*, not validated calendar finish dates, P6 RFS forecast, or contractual P50/P80/P90. Duration multiplier bounds (0.8/1.0/1.3) are illustrative, uncalibrated and independent. Before presenting contractual confidence dates, calibrate activity uncertainty, model calendars/progress, independently compare deterministic results with P6, and validate risk dependencies.

## Release status

- Unit tests: automated on PR; inspect GitHub Actions run before describing as passing.
- XER audit: run against the exact source export and retain JSON/CSV evidence.
- Workbook-to-EVM mapping: pending original workbook data extraction and KPI comparison.
- P6-calibrated calendar-aware Monte Carlo: not implemented. Do not claim P6-equivalent probabilistic completion dates.

No original XER, frozen baseline, update, workbook or dashboard is modified by these scripts.
