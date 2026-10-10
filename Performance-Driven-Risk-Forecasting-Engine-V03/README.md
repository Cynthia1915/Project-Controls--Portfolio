# Performance-Driven Risk & Forecasting | Research Prototype V03

**EVM · Performance Exceptions · Exploratory Forecasting · Management Reporting**

[← Portfolio](../README.md)

## Management question

**How can progress, cost and float indicators be combined to prioritize emerging project-control issues?**

This independent portfolio prototype combines modeled progress, earned value and schedule indicators to generate **rule-based risk scores, exception lists and illustrative forecast scenarios**.

## Analytical workflow

1. Review planned/actual progress, budget, float, PV, EV and AC.
2. Compute and interpret CPI, SPI and progress variances.
3. Screen schedule/cost issues and prioritize activities using documented heuristic rules.
4. Generate management-oriented findings and **illustrative** forecasting outputs.

## What is demonstrated

- Project-controls KPI processing and exception screening.
- Dynamic risk scoring and escalation prioritization.
- Exploratory cost/schedule forecasting and summary reporting.
- Python-based transformation of a modeled performance dataset.

## Critical modeling limitation

**The Monte Carlo component uses the maximum sampled activity duration as a simplified proxy for project completion.** It **does not** recalculate a Primavera P6 CPM network, relationships, lags, calendars or a changing critical path.

Therefore, any P50/P80/P90 values or forecast delay distributions in this prototype are **not valid network-based project completion confidence estimates** and should **not** be used as commercial schedule-risk results.

For the dedicated schedule-risk project and its validation roadmap, see [Monte Carlo Schedule Risk](../Monte-Carlo-Schedule-Risk-Simulator/).

## Appropriate management interpretation

Use the prototype to demonstrate **how performance data can support exception-based reporting**. Any operational deployment would require data reconciliation, formula validation, risk calibration and integration with an actual P6 schedule.

**Tools:** Python, Pandas, NumPy, Matplotlib, EVM and Primavera P6 schedule concepts.

**Status:** Research prototype V03 with simulated inputs and simplified forecasting; not a live client delivery.
