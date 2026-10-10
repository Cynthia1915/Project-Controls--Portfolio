# Project Controls Early Warning System | Prototype V01

**Progress Monitoring · Cost and Schedule Exceptions · Management Escalation**

[← Portfolio](../README.md)

## Management question

**Which activities should the project-controls team investigate before performance issues become major delivery problems?**

This independent portfolio prototype screens a modeled project-performance dataset and translates threshold breaches into **prioritized alerts and management actions**.

## Rule-based screening

| Indicator | Illustrative alert threshold |
| --- | --- |
| Schedule performance index (SPI) | Below 0.90 |
| Cost performance index (CPI) | Below 0.90 |
| Progress variance | Below −10 percentage points |
| Total float | 5 days or less |

The scoring demonstration assigns **one point** to each schedule, cost or progress flag and **two points** to low float, with green/yellow/orange/red alert levels.

**Important:** These are **heuristic screening thresholds**, not validated predictors of future delay, contractual defaults or a substitute for project-specific control limits.

## Management-oriented outputs

- Ranked activities and work packages for review.
- Rule-based alert levels and recommended follow-up actions.
- Executive KPI summaries and Excel reporting.
- A repeatable screening approach suitable for further validation.

## Evidence

See the [notebook](./notebook/), [outputs](./outputs/), [screenshots](./screenshots/) and [supporting documentation](./docs/).

## Example management actions

For high-priority alerts, confirm source-data quality, investigate critical/near-critical logic, review current forecast exposure, identify the responsible package owner and agree on a recovery or monitoring action.

## Boundaries

The prototype does not establish causal relationships, quantify probability of delay, forecast CPM finish dates or include a production real-time integration. Thresholds and weightings must be validated for each actual project.

**Status:** Independent simulated portfolio prototype V01.
