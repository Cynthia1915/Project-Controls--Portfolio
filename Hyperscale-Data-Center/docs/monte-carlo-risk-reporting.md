# Monte Carlo schedule-risk reporting — Data Center

This module **extends** the existing `network_monte_carlo.py` prototype with a
reproducible, machine-readable **relative-hour risk report**. It does not claim
Primavera P6 calendar equivalence.

## Run (with your single-project Data Center XER)

From the repository root:

```bash
python Hyperscale-Data-Center/notebooks/audit_xer.py /path/to/DC_Update01.xer --output-dir risk_outputs/audit
python Hyperscale-Data-Center/notebooks/network_monte_carlo.py /path/to/DC_Update01.xer --runs 10000 --seed 42 --target RFS-040 --output-dir risk_outputs
python Hyperscale-Data-Center/notebooks/risk_reporting.py --summary risk_outputs/network_risk_summary.json --samples risk_outputs/network_risk_samples.csv --output risk_outputs/relative_risk_report.json
python -m unittest discover -s Hyperscale-Data-Center/notebooks/tests -v
```

Outputs include P10/P50/P80/P90 **relative continuous hours**, a binned histogram,
probability of exceeding the model's deterministic relative-hour reference,
and P80 contingency in relative hours. These are **not** calendar completion
dates, contractual confidence levels, or verified P6 forecast values.

## Engineering acceptance gates

1. Obtain the authoritative single-project P6 XER and capture data date,
   target milestone, calendars, constraints and scheduling options.
2. Resolve high-severity structural audit findings.
3. Reconcile deterministic forward-pass dates against P6; current
   continuous-hour model cannot satisfy this gate for multi-calendar projects.
4. Calibrate duration distributions using evidence and model correlated
   project risks. Current independent triangular multipliers are illustrative.
5. Validate progress anchoring, out-of-sequence logic, lags and resource impacts.
6. Only then implement and publish calendar-based contractual milestone
   confidence. Do not relabel the current relative-hour P80 as a finish date.

**Data availability:** The repository currently contains schedule-summary PDFs
but not the original source XER. Therefore no Data Center-specific simulation
has been executed or validated as part of this addition.
