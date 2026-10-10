# Baseline, Schedule & Progress Updates
## Hyperscale Data Center — Integrated Project Controls

**Case study:** DC-HYP-FINAL-6 · **Nature:** independent synthetic simulation · **Change control:** original Primavera schedule and published reporting artifacts preserved.

> **Management question:** How do we turn an approved schedule baseline into reliable progress reporting, forecast comparisons and management decisions?

## 1. Integrated project schedule — the planning model

The Primavera P6 schedule represents the planned sequence of engineering, procurement, construction, electrical/mechanical systems, energization, integrated testing, commissioning and readiness for service. It provides a common time-based structure for coordination and reporting.

| Schedule characteristic | Recorded basis |
|---|---|
| Activities | 808 |
| Relationships | 1,406 |
| WBS elements | 131 |
| Calendars | 5 |
| Synthetic cost baseline | USD 120 million |
| Planned project start | 05 January 2026 |
| Baseline Ready for Service (RFS) | 15 July 2027 |

**What is a schedule?** A schedule is the time-phased model of work: activities, logic relationships, durations, calendars and milestones. When progress is recorded, its forecast dates can move.

**What is a baseline?** The baseline is the approved reference snapshot against which current progress and forecast dates are measured. The baseline is **not overwritten** whenever the working schedule is updated.

## 2. Baseline B1 — establishing the control reference

Baseline B1 freezes the original planning assumptions for variance analysis. The milestone of interest is **RFS-040 — Ready for Service**, targeted for **15 July 2027**.

**Control purpose:** preserve a stable reference for planned versus forecast milestone dates, identify schedule variance, and communicate whether subsequent updates are moving away from the agreed plan.

The baseline is retained as the comparison point; it is not retrospectively revised to make later performance look better.

**Evidence:** [Baseline schedule summary](../primavera/baseline-schedule-summary.pdf).

## 3. Update 01 — January 2026 status and forecast

**Data date:** 31 January 2026 at 17:00. This is the schedule cut-off used to distinguish actual progress from remaining work.

| Update 01 measure | Recorded value |
|---|---:|
| Completed activities | 44 |
| In-progress activities | 21 |
| Not-started activities | 743 |
| Baseline RFS | 15 July 2027 |
| Forecast RFS | 19 July 2027 |
| Milestone variance | +4 calendar days |

**Interpretation:** The Update 01 forecast is four calendar days later than the frozen baseline target. This is a reported schedule variance, **not by itself a validated causal delay analysis**. A driving-path trace and review of changed activity assumptions would be needed before attributing the movement to specific work packages.

**Schedule logic assurance:** File-level checks on the Update 01 XER identified no directed cycles, invalid task references, negative lags or date constraints. The two boundary activities without predecessor/successor are the expected project start and finish. There are **107 positive-lag relationships** requiring explanation, not automatic removal. The RFS finish milestone is linked to three acceptance gates. These checks do not constitute an independent P6 recalculation or comprehensive schedule certification.

**Evidence:** [Update 01 schedule summary](../primavera/update-01-schedule-summary.pdf) · [Technical audit and qualifications](./update-01-technical-audit.md).

## 4. Update 02 — February 2026 reporting cycle

**Data date:** 28 February 2026.

Update 02 demonstrates the next reporting cycle: record additional actual progress, reschedule remaining work, compare the new forecast with **both Baseline B1 and Update 01**, and review critical/near-critical activities and milestone exposure.

The specific Update 02 activity counts, milestone movement and KPI values should be read from its own reporting snapshot; **Update 01 figures must not be copied into Update 02** without reconciliation.

**Evidence:** [Update 02 schedule summary](../primavera/update-02-schedule-summary.pdf).

## 5. From schedule update to management reporting

| Control step | Purpose | Typical output |
|---|---|---|
| Plan | Structure WBS, activities, calendars and logic | Integrated P6 schedule |
| Baseline | Freeze the approved reference | Baseline B1 and RFS target |
| Status | Record actual starts/finishes and remaining work at a data date | Update 01 / Update 02 |
| Recalculate | Apply consistent scheduling settings and inspect driving paths | Forecast milestone dates |
| Compare | Explain variance against baseline and prior update | Schedule movement and exception log |
| Report | Present schedule exposure with modeled cost and EVM measures | Executive dashboard and management narrative |

**Cost-data qualification:** USD 120 million is a synthetic budget. Update 01's XER expense records contain **zero native actual expense cost**, while the portfolio's PV, EV, AC and forecast measures are externally modeled. The external cost model must be described and reconciled separately; it is not validated native P6 EVM output.

## 6. Schedule governance and limitations

- **No retrospective editing:** Baseline B1, the original XER updates and published dashboards remain unchanged for this portfolio explanation.
- **Exceptions are documented:** A positive lag or non-FS milestone link is not automatically a defect. A substantive change would require evidence, impact review and version control.
- **Reproducibility matters:** The schedule QA script and reporting methodology should be tested and clearly scoped before describing the analysis as independently validated.
- **Synthetic disclosure:** This is a portfolio demonstration, not a live client's approved project or a certified forensic delay analysis.

**Key project-controls takeaway:** A useful baseline is stable; a useful update is transparent about what changed; a useful report separates observed variance from assumptions and causal conclusions.

[← Case study overview](../README.md) · [Methodology](./methodology.md) · [Executive dashboard](../dashboard/)
