# Residential Tower — Schedule Recovery & Digital Project Controls

### Primavera P6 · Schedule Assurance · Recovery Strategy · Python Automation · Executive Decision Support

**Portfolio case study | Simulated 15-story residential tower with two basement levels**

> **Management question:** An updated schedule forecasts completion 18 calendar days later than baseline. Which recovery intervention offers the stronger finish-date improvement, and what must be validated before management can authorize it?

## Executive findings

| Metric | Baseline | Update 01 | Recovery A | Recovery B |
|---|---:|---:|---:|---:|
| Stored P6 forecast finish | 13 May 2028 | 31 May 2028 | 16 May 2028 | 18 May 2028 |
| Delay vs baseline (calendar days) | 0 | +18 | +3 | +5 |
| Days recovered vs Update 01 | — | — | 15 | 13 |
| Activities | 265 | 265 | 265 | 265 |
| Relationships | 362 | 362 | 362 | 363 |
| Completed / in progress / not started | 0 / 0 / 265 | 7 / 3 / 255 | 7 / 3 / 255 | 7 / 3 / 255 |
| Activities with nonpositive stored total float | 103 | 100 | 100 | 100 |

**Finding:** Recovery A closes 15 of 18 delayed calendar days (83.3% of the delay), while Recovery B closes 13 (72.2%). These are comparisons of **stored P6 scheduled-finish fields**, not independent CPM recalculations.

## Deep-dive engineering interpretation

The headline schedule result is only the beginning of the analysis. The [Detailed Engineering Analysis](./05_Reports/Detailed_Engineering_Analysis.md) explains the original 18-day delay, the four compressed activities in Recovery A, the FS-to-SS handoff changes in Recovery B, float and progress interpretation, and the governance checks needed before authorizing a recovery programme.

**Important diagnostic:** Although Recovery A changes only four planned durations, **255 activity early-finish dates move earlier** relative to Update 01 (217 by eight calendar days and 31 by nine days). This widespread movement is a **P6 schedule-integrity validation item**. It should not be credited entirely to duration compression without confirming data dates, calendars, constraints and rescheduling behavior. Recovery B has four shifted activity early finishes and 261 unchanged, consistent with a more localized downstream change.

**Read the analysis before relying on the modeled recovery:** [Full schedule diagnostics, risk evaluation and management action plan](./05_Reports/Detailed_Engineering_Analysis.md).

---

## Recovery option assessment

**Recovery A — selective duration compression.** Four activities have reduced planned durations relative to Update 01: TST-020 (−24 hours), TST-050 (−24 hours), EXC-030 (−16 hours) and EXC-040 (−16 hours). The normalized dependency set is unchanged. The management trade-off is stronger finish-date recovery versus the need to substantiate acceleration productivity, resources, cost and workface constraints.

**Recovery B — resequencing / overlap.** Planned activity durations are unchanged. The scenario adds four relationships and removes three. Three finish-to-start handoffs are replaced by start-to-start links with positive lags (TST-010→TST-020, TST-020→TST-030, TST-040→TST-050); one additional finish-to-start link connects TST-040→M-HANDOVER. The management trade-off is reduced reliance on direct duration compression versus heightened coordination, interface and handover risk.

### Decision recommendation

**Advance Recovery A to a controlled feasibility review**, because its modeled finish is two calendar days earlier than Recovery B and its dependency set is unchanged. **Do not approve implementation yet.** Require quantified crew/equipment loading, productivity assumptions, acceleration costs, site logistics, inspection/quality hold points and safety controls. Retain Recovery B as a conditional alternative if its overlaps can be justified through documented interface plans.

### Schedule health signal

The Update 01 export contains **100 activities with nonpositive stored total float** (baseline: 103). This is a **screening indicator**, not proof that every such activity belongs to a single validated driving path. Float interpretation depends on calendars, constraints and P6 settings. Critical-path and near-critical-path claims require a dedicated network and constraints review.

## Reproduce the analysis

The original four Primavera P6 XER exports are included under [01_P6_Exports](./01_P6_Exports/). They were sourced from the separate [schedule-source repository](https://github.com/Cynthia1915/Project-Controls-Portfolio). The extractor uses the Python standard library (Python 3.10+).

```bash
cd Residential-Tower-Project-Controls
python 02_Python_ETL/analyze_scenarios.py --input 01_P6_Exports --output 03_Processed_Data
python -m unittest discover -s tests -v
```

The script writes `Scenario_Summary.csv`, `Activities.csv`, `Relationships.csv`, `Duration_Changes.csv`, and `Logic_Changes.csv`. It fails explicitly when required source files are missing, or a relationship references an unknown activity. The source files remain unchanged.

**Method:** Parse XER `PROJECT`, `TASK` and `TASKPRED` tables; use `PROJECT.scd_end_date` for forecast finish, `TASK.status_code` for progress status, `TASK.total_float_hr_cnt` for float screening, `TASK.target_drtn_hr_cnt` for duration changes, and normalized predecessor/successor activity codes for logic comparisons. Calendar-day differences use date-time subtraction at equal 16:00 scheduled finish times.

## Portfolio deliverables

- [Executive management analysis](./05_Reports/Executive_Decision_Brief.md)
- [Detailed recovery comparison](./05_Reports/Recovery_Comparison.md)
- [Reproducible four-scenario Python analysis](./02_Python_ETL/analyze_scenarios.py)
- [Looker Studio dashboard specification](./04_Dashboard/README.md)
- [Original P6 XER exports](./01_P6_Exports/)

## Boundaries and integrity

This is an **independent simulated case study**, not a live construction engagement. The recovery scenarios were not validated for manpower, productivity, cost, construction safety, procurement or execution feasibility. No earned-value, CPI/SPI or resource-loaded claims are made without supporting data. The dashboard is specified but **not published as a live Looker Studio report**. Stored P6 dates and float values are reported as exported, not independently rescheduled.

**Professional takeaway:** Project controls is not simply identifying an 18-day delay; it is translating schedule alternatives into an evidence-based decision, exposing their implementation constraints and defining the next control actions.
