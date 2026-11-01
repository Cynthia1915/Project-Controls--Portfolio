# Earned Value Management & Cost Forecasting | EVM-CF-001

**Simulated construction case study | Budget at Completion (BAC): USD 50,000,000**

An evidence-driven cost-control portfolio project demonstrating earned-value measurement, monthly reporting, completion forecasting, reconciliation and management decision support. **All underlying data are synthetic and illustrative, not client/project records.**

## Business problem

A construction project reports an apparent expenditure underrun, but expenditure alone does not reveal whether sufficient work was earned. The controls team must separate planned work, earned work and actual cost, then estimate the likely final cost and explain corrective actions.

## Technical project plan

| Phase | Deliverable | Acceptance criterion |
| --- | --- | --- |
| 1. Define control baseline | Five control accounts with USD 50M BAC | Account budgets reconcile exactly to project BAC |
| 2. Generate monthly status | Deterministic synthetic period PV/EV/AC inputs | Monotonic cumulative series; no negative periods; earned value bounded by BAC |
| 3. Compute EVM metrics | Python CLI, CSV outputs | Standard CPI/SPI/CV/SV and EAC variants; no divide-by-zero |
| 4. Validate | Unit tests and automated CI | Formula tests, budget reconciliation and boundary cases pass |
| 5. Executive reporting | Browser dashboard and management memo | Cost exposure, scenario assumptions and corrective actions visible |
| 6. Governance | Document data provenance and limitations | No real-client, CPM, resource or physical quantity claims |

## Methods

- **PV** = budgeted cost of work scheduled; **EV** = budgeted cost of work performed; **AC** = actual cost of work performed.
- **CV** = EV − AC; **SV** = EV − PV (currency, **not days**).
- **CPI** = EV / AC; **SPI** = EV / PV, where denominators are positive.
- **EAC (CPI)** = BAC / CPI, assuming cumulative cost efficiency continues.
- **EAC (remaining work at budget rate)** = AC + (BAC − EV).
- **EAC (CPI × SPI)** = AC + (BAC − EV) / (CPI × SPI), a sensitivity scenario rather than a validated project forecast.
- **ETC** = EAC − AC; **VAC** = BAC − EAC.
- **TCPI to BAC** = (BAC − EV)/(BAC − AC), only when denominator is positive.
- A negative SV or SPI below 1 reflects **value of work behind plan**, not a calculated time delay or critical-path slippage.

## Reproduce

Requires Python 3.10+ and no third-party packages.

```bash
python EVM-Cost-Forecasting/src/evm.py --output EVM-Cost-Forecasting/outputs
python -m unittest discover -s EVM-Cost-Forecasting/tests -v
```

The generator is deterministic and produces `monthly_evm.csv`, `control_accounts.csv`, and `summary.json`. A static executive dashboard is in [dashboard/index.html](dashboard/index.html). The dashboard is a **self-contained HTML reporting artifact**, not a native Looker Studio or Power BI report.

## Case assumptions and limitations

Five simulated control accounts represent civil works, structure, MEP, envelope and commissioning. Twelve monthly periods model a plausible cost overrun emerging as work is earned more slowly than it is spent. Account-level budget is a planning allocation, **not** a validated quantity-based estimate or a P6 resource-loaded baseline. Forecast formulas assume no approved change orders, scope changes or revised BAC. CPI and SPI alone do not establish critical-path or schedule completion dates. Scenario EACs are conditional mathematical projections, not probabilistic confidence intervals.

## Portfolio deliverables

- [Python EVM engine](src/evm.py)
- [Tests](tests/test_evm.py)
- [Executive dashboard](dashboard/index.html)
- [Executive decision brief](reports/Executive_Decision_Brief.md)
- [GitHub Actions validation](../.github/workflows/evm-cost-forecasting.yml)
