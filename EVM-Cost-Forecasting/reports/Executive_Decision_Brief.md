# Executive decision brief — EVM-CF-001

**Scenario:** Simulated USD 50M construction program. **Purpose:** illustrate a monthly earned-value control decision, not report actual project performance.

## Executive question

Is the apparent spend level consistent with earned progress, and what completion-cost exposure should management consider?

## Management interpretation

The synthetic monthly dataset intentionally creates a persistent gap between budgeted work scheduled (PV), budgeted work performed (EV), and actual cost (AC). A CPI below 1 indicates cost inefficiency: the project earns less budgeted value than it spends. An SPI below 1 indicates less work earned than planned in monetary units; **it is not a number of days late**.

The model reports three **conditional**, not probabilistic, estimates at completion:

1. **CPI continuation:** BAC/CPI. Appropriate only if historical cumulative cost efficiency is a credible predictor.
2. **Remaining work at budget rate:** AC + (BAC − EV). Assumes all remaining work is completed at planned cost.
3. **Combined CPI × SPI sensitivity:** AC + (BAC − EV)/(CPI × SPI). Illustrates a downside scenario but must not be interpreted as a statistically calibrated P80 forecast.

The spread between these methods is **assumption sensitivity**, not a confidence interval.

## Decision gates

- **Controls lead:** verify source quantities, physical percent complete, actual costs, accruals, cut-off and account mappings.
- **Construction manager:** diagnose productivity losses, rework, procurement interfaces and constrained work fronts.
- **Commercial lead:** identify approved changes, commitments and cost-to-complete obligations; update BAC only with change control.
- **Planning lead:** independently assess the P6 driving path; do not convert SPI into calendar delay.
- **Project director:** authorize a recovery plan after cost-to-complete and schedule feasibility reviews.

## Reporting controls

- Freeze monthly cut-off, baseline revision and control-account coding.
- Reconcile AC to the ledger, EV to approved quantity/progress measurement and PV to time-phased baseline.
- Investigate exceptions for negative variances, anomalous period movements and missing source records.
- Record forecast assumptions, ownership, action due dates and approval status.

## Limitations

This is a deterministic synthetic training model. There are no actual invoices, purchase orders, resource histograms, measured construction quantities, critical-path calculation or risk probability distributions. The final modeled month reaches planned PV = BAC but does not imply project completion because EV remains below BAC.
