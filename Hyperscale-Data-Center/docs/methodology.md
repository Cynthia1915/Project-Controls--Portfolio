# Methodology | Hyperscale Data Center Project Controls

[← Case study](../README.md)

## Purpose and boundaries

This is an **independent synthetic project-controls case study**, not an as-built project record, contractor programme, audited estimate or live client assignment. Its purpose is to demonstrate a structured planning-to-reporting workflow and management interpretation.

## 1. Schedule baseline

- Primavera P6 schedule with **808 activities and 1,406 relationships**.
- Engineering-based WBS and sequencing across design, procurement, construction, energization, commissioning and handover.
- Planned start: **05 January 2026**.
- Baseline RFS: **15 July 2027**.
- Multiple calendars and relationship types exist in the source schedule. Any simplified external calculation must not be described as fully reproducing the P6 scheduling engine.

**Evidence:** [Baseline schedule PDF](../primavera/baseline-schedule-summary.pdf).

## 2. Updates and forecast

- Update 01 data date: **31 January 2026**.
- Update 02 data date: **28 February 2026**.
- The reported updated RFS forecast is **19 July 2027**, four calendar days later than baseline.
- Period-specific performance comparisons must use one selected data date, not sum project-level metrics across historical updates.

**Evidence:** [Update 01](../primavera/update-01-schedule-summary.pdf) · [Update 02](../primavera/update-02-schedule-summary.pdf).

## 3. Synthetic cost baseline and EVM

**BAC: USD 120,000,000**, distributed across WBS/work packages as portfolio assumptions. Cost loading uses Primavera expense-style records rather than verified resource-loaded estimates.

Basic EVM definitions:

| Measure | Definition |
| --- | --- |
| PV | Planned value to the reporting date under the documented time-phasing assumption |
| EV | Budgeted value of modeled completed work |
| AC | Modeled actual cost to date |
| CPI | Total EV / Total AC, where AC is nonzero |
| SPI | Total EV / Total PV, where PV is nonzero |
| CV | EV − AC |
| SV | EV − PV |
| CPI-based EAC | BAC / CPI, where CPI is valid |
| ETC | EAC − AC |
| VAC | BAC − EAC |

**Important:** External EVM calculations and activity UDFs were used because native P6 EV did not reconcile as intended in the original workflow. Do not claim that the dashboard metrics are verified native P6 EV outputs.

Project/WBS CPI and SPI must be recomputed from summed monetary values, **never** by summing ratios. The dashboard must select a reporting period to avoid duplicate BAC and distorted CPI/SPI.

The modeled PV time-phasing and progress assumptions are simplifications; the case study does not establish a validated contractual performance measurement baseline.

## 4. Forecast and management interpretation

Forecast scenarios (including CPI-based and combined performance-index assumptions) are **illustrative**, not certified cost-to-complete estimates. Each scenario should state its formula and applicability. Schedule forecast movement should be checked against P6 update evidence rather than inferred from SPI alone.

Management focus includes design-release interfaces, long-lead transformer procurement, electrical energization, integrated systems testing and handover readiness.

## 5. Reporting architecture

```text
Primavera P6 baseline and updates
               ↓
    Structured project data
               ↓
   EVM / schedule / forecast logic
               ↓
    Reporting-period dataset
               ↓
  Looker Studio executive views
               ↓
 Management interpretation
```

The repository contains [reporting data](../data/), [dashboard images](../dashboard/) and [schedule PDFs](../primavera/). A fully executable Data Center processing notebook is **not currently committed**; workflow descriptions are not a substitute for runnable source.

## 6. Pre-publication QA checklist

- [ ] Select one data date consistently across KPI cards, charts and management narrative.
- [ ] Confirm BAC = USD 120M for a single update, not a sum of historical snapshots.
- [ ] Recompute CPI = EV/AC and SPI = EV/PV from aggregated values.
- [ ] Check EAC, ETC and VAC use matching formulas and update period.
- [ ] Verify critical/low-float classifications against the P6 schedule and handle missing float separately.
- [ ] Confirm milestone dates and dashboard labels match the update PDFs.
- [ ] Disclose synthetic data, assumptions and incomplete automation reproducibility.

**These checks are a release checklist, not a claim that all have already passed.**
