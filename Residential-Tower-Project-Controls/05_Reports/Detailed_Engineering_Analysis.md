# Detailed Engineering Analysis — Residential Tower Schedule Recovery

**Project type:** Independent simulated construction case study  
**Asset:** 15-story residential building, two basement levels  
**Primary system:** Primavera P6 XER exports  
**Scope of this report:** schedule position, forensic-style file comparison, recovery option evaluation, schedule-integrity observations, risk treatment, and management decision gates.

> **Executive conclusion:** The update forecasts an 18-calendar-day delay against the baseline. Recovery A's exported finish is 15 days earlier than Update 01, versus 13 days for Recovery B. **Recovery A is a candidate for feasibility review, not an approved plan.** A major date-shift anomaly requires independent P6 recalculation before attributing the forecast improvement to the four compressed durations.

## 1. The project-controls problem

A baseline programme establishes the intended completion date and the activity logic required to reach it. At a progress update, management must distinguish **reported progress**, **forecast impact**, and **available corrective action**. Simply reporting a late finish is insufficient: the decision depends on what caused the variance, which activities govern completion, and whether a proposed recovery schedule is buildable.

The simulated project contains 265 activities in each scenario, spanning preparatory work, excavation, basement structure, superstructure and downstream testing/handover. The four XER exports represent a baseline, a delayed update, and two alternative recovery models. They are useful for a controlled *scenario comparison*, but they are not evidence of actual site progress, incurred cost, or resource availability.

The central management question is:

**Can the 18-day completion variance be reduced through targeted activity compression or revised sequencing without creating unacceptable resource, safety, quality, or interface risks?**

## 2. Evidence and audit methodology

The assessment uses native XER tables, not manually typed dashboard values:

| XER data | Analytical use | Limitation |
|---|---|---|
| `PROJECT.scd_end_date` | Stored project forecast finish | Not an independently recomputed CPM finish |
| `TASK.task_code`, `task_name` | Stable activity identity and description | Codes must be checked for uniqueness |
| `TASK.status_code` | Completed / in-progress / not-started counts | Status is not physical percent complete |
| `TASK.target_drtn_hr_cnt` | Planned-duration comparison | Does not reveal crew levels or productivity assumptions |
| `TASK.early_finish_date` | Activity-level early-finish movement | Exported dates may reflect scenario construction and scheduling settings |
| `TASK.total_float_hr_cnt` | Nonpositive-float screening | Not sufficient alone to establish a valid driving path |
| `TASKPRED` predecessor, successor, type and lag | Logic added/removed across scenarios | Relationship counts alone cannot establish network quality |

Relationships were compared after mapping internal P6 task IDs to activity codes. This avoids treating changed internal IDs as changed engineering logic. The source XER files are retained unchanged. The analysis script in this repository regenerates scenario summaries and duration/relationship deltas; the activity-level date-movement diagnostics in this report should also be independently reproduced and reviewed in P6.

### Verified high-level schedule snapshot

| Indicator | Baseline | Update 01 | Recovery A | Recovery B |
|---|---:|---:|---:|---:|
| Exported finish | 13 May 2028 | 31 May 2028 | 16 May 2028 | 18 May 2028 |
| Variance vs baseline | 0 d | +18 d | +3 d | +5 d |
| Improvement vs Update 01 | — | — | 15 d | 13 d |
| Activities | 265 | 265 | 265 | 265 |
| Relationships | 362 | 362 | 362 | 363 |
| Completed | 0 | 7 | 7 | 7 |
| In progress | 0 | 3 | 3 | 3 |
| Not started | 265 | 255 | 255 | 255 |
| Activities with nonpositive exported total float | 103 | 100 | 100 | 100 |

**Calendar-day arithmetic:** 31 May minus 13 May = 18 days; 31 May minus 16 May = 15 days; 31 May minus 18 May = 13 days. These dates are exported project-level values. They should not be interpreted as resource-feasible completion commitments.

### Interpretation of progress

Update 01 records **7 completed (2.6%)**, **3 in progress (1.1%)** and **255 not started (96.2%)** activities by *activity count*. These are proportions of schedule activities, **not earned physical progress**. An activity count weights a one-day task and a major structural work package equally. Weighted progress requires approved quantities, earned rules or budgeted values, none of which are evidenced here.

## 3. Recovery A — targeted duration compression

Relative to Update 01, four planned durations decrease:

| Activity | Description | Duration change |
|---|---|---:|
| EXC-030 | Excavation to basement 1 | −16 hours |
| EXC-040 | Excavation to basement 2 and dewatering | −16 hours |
| TST-020 | Integrated MEP functional testing | −24 hours |
| TST-050 | Final snag closeout, O&M manuals and training | −24 hours |

The total of the four *individual* duration reductions is **80 hours**. **Do not equate that sum with a project finish improvement:** durations may lie on parallel or non-driving paths, use different calendars, or be separated by logic and constraints. The exported finish improves by 15 calendar days, but that outcome must be reconciled to the actual network.

The unchanged relationship set means the modeled strategy does not rely on newly inserted overlap links. That reduces one category of logic-change risk, but does **not** establish constructability. Excavation compression may require more excavation capacity, trucking, dewatering or extended shifts; testing and closeout compression may require parallel inspection teams, faster defect resolution, earlier documentation readiness and protected quality gates.

### Critical validation finding: widespread date shifts

In the exported activity-level comparison against Update 01:

- **255 of 265 activities** have an earlier exported early-finish date under Recovery A.
- **217 activities** move earlier by **8 calendar days**.
- **31 activities** move earlier by **9 calendar days**.
- The final handover milestone moves earlier by **15 calendar days**.
- Only **four activities** have reduced planned durations.

This is a **schedule-integrity question**, not automatically a defect and not proof of valid acceleration. It suggests the scenario contains widespread date movement that cannot be explained solely by listing four duration changes. Possible explanations to investigate include scheduling/recalculation behavior, altered calendar or constraint settings, different start-date assumptions, or the way the simulated scenario was generated. These are **hypotheses**, not verified causes.

**Required test:** Open Update 01 and Recovery A in P6; compare project data dates, calendars, constraints, activity early starts/finishes, remaining durations and the scheduling log. Recalculate both using equivalent settings. Trace the longest path to handover and reconcile each material date shift. Until then, the 15-day recovery remains a **stored-schedule forecast comparison**, not a causally validated acceleration result.

## 4. Recovery B — resequencing and controlled overlap

Recovery B keeps all activity planned durations unchanged and modifies the relationship set: **four added, three removed**.

| Removed relationship | Replacement / addition | Management interpretation |
|---|---|---|
| TST-010 → TST-020, FS +0h | TST-010 → TST-020, SS +80h | Begin MEP functional testing after a defined amount of predecessor progress, rather than after full predecessor finish |
| TST-020 → TST-030, FS +0h | TST-020 → TST-030, SS +112h | Allow fire/life-safety testing preparation or execution to overlap MEP testing, subject to prerequisites |
| TST-040 → TST-050, FS +0h | TST-040 → TST-050, SS +80h | Allow snag/closeout work to begin before authority inspection/approval is entirely complete |
| — | TST-040 → M-HANDOVER, FS +0h | Preserve an explicit authority-inspection-to-handover completion gate |

**FS** means finish-to-start; **SS** means start-to-start. Positive lag is expressed in hours in the XER; the equivalent elapsed calendar time depends on the relevant scheduling calendars. An SS link with lag is not proof that work can safely overlap.

### Why the logic change matters

A dependency is a model of a real construction or commissioning interface. Replacing FS with SS can shorten the modeled network while increasing the need for:

- Defined handover packages and test prerequisites.
- Safe access to concurrent work areas.
- Verified test-system readiness and isolation.
- Documented hold points for fire/life-safety and authority approval.
- Clear ownership of partial completion and rework.

**Activity-level movement:** Recovery B changes exported early-finish dates for **four activities**; 261 are unchanged. The handover and final closeout activities move 13 calendar days earlier, and two other downstream testing/inspection activities move 7 days earlier. This more localized movement is consistent with a downstream sequencing intervention, but still requires a P6 recalculation and interface review.

## 5. Schedule health, float and confidence

The exported Update 01 has **100 activities with nonpositive total float**; the baseline has 103. This may indicate a constrained or tightly linked network, but the number alone does not establish the *critical path*. Nonpositive float can arise from project completion targets, constraints, calendars and schedule calculation settings.

A senior-level schedule assurance review should check:

1. **Open ends and dangling logic:** Are all non-start/non-finish activities logically connected?
2. **Constraint discipline:** Do imposed finish dates or mandatory constraints mask realistic network behavior?
3. **Calendar consistency:** Are different working calendars understood before comparing hours and calendar days?
4. **Lag quality:** Does each positive lag represent a defensible real-world dependency?
5. **Driving-path trace:** Which activity chain actually governs the handover milestone after rescheduling?
6. **Progress quality:** Are actual dates, remaining durations and data dates consistent across update/recovery files?
7. **Sensitivity:** Does a small change to a few critical activities alter the completion forecast as expected?

This report deliberately does not claim a validated critical path or quantitative schedule-risk distribution.

## 6. Decision matrix — qualitative, evidence-aware

| Criterion | Recovery A | Recovery B | Confidence |
|---|---|---|---|
| Stored finish improvement | 15 days | 13 days | High: directly in exported project fields |
| Logic stability | No normalized dependency changes | 4 added / 3 removed | High: XER relationship comparison |
| Duration changes | 4 shorter durations | None | High: XER task comparison |
| Productivity/resources | Unverified | Unverified | Insufficient evidence |
| Construction interface risk | Compression/crew congestion possible | Overlap/commissioning interfaces prominent | Engineering assessment only |
| Cost premium | Unknown | Unknown | Insufficient evidence |
| Causal schedule integrity | Broad date shifts require reconciliation | Localized downstream date shifts | Requires P6 review |

**Recommendation:** Select Recovery A for the *first feasibility investigation*, not for immediate implementation. It provides the earlier stored finish and leaves dependency links unchanged, but its unusually broad activity date shifts are a material verification issue. Recovery B should remain a viable alternative for a structured commissioning/inspection interface workshop.

**Decision rule:** If Recovery A cannot be reproduced under controlled P6 settings, or if resource/cost/safety impacts are unacceptable, reassess both options using a common validated schedule model. Do not rank them on finish date alone.

## 7. Recommended control actions and owners

| Priority | Action | Suggested accountable role | Evidence required |
|---|---|---|---|
| P1 | Recalculate Update 01 and both recovery scenarios with controlled calendars/settings | Planning Engineer / Scheduler | P6 logs, date comparison, driving path |
| P1 | Reconcile Recovery A's 255 shifted early finishes | Schedule Assurance Lead | Exception report and explanation |
| P1 | Confirm excavation and commissioning workface feasibility | Construction / MEP Leads | Method statements, access plan |
| P2 | Quantify resources, shift patterns and acceleration cost | Project Controls / Commercial | Resource histograms, cost comparison |
| P2 | Validate authority, testing and handover hold points | QA/QC / Commissioning | Approved test and inspection sequence |
| P2 | Define weekly recovery monitoring | Project Controls Manager | Milestone trend, float/logic exceptions |
| P3 | Issue management-approved recovery baseline after gates pass | Project Manager | Approved programme and assumptions register |

These are **proposed governance roles**, not actual assignments made on a real project.

## 8. Executive reporting design

A four-page dashboard should separate *facts* from *decisions*:

- **Executive overview:** baseline/update/recovery finish dates, 18-day variance, 15-day and 13-day modeled recoveries, and explicit verification status.
- **Schedule performance:** status counts and percentages by activity count, milestone forecast, float screening and schedule-quality exceptions.
- **Recovery alternatives:** duration-change table, logic-delta table, forecast comparison, and the Recovery A widespread-date-shift flag.
- **Risk and decisions:** qualitative risk register, missing resource/cost evidence, verification gates and conditional recommendation.

A published Looker Studio dashboard is **not** part of this GitHub deliverable; the repository includes the source data and design specification.

## 9. Lessons learned

1. **A finish-date improvement is not the same as a verified recovery mechanism.** Always reconcile scenario changes to the driving network.
2. **Schedule logic is an engineering assumption.** FS-to-SS changes must reflect actual workface and test readiness.
3. **Float is a diagnostic, not a substitute for network assurance.** A count of nonpositive-float tasks does not establish the driving path.
4. **Progress measurement must be weighted appropriately.** Activity-count percentages cannot be presented as earned progress.
5. **An executive recommendation should specify conditions.** Recovery alternatives should move through schedule, resource, commercial and safety gates before authorization.

---

### Evidence classification

- **Observed from XER exports:** dates, counts, activity status, planned duration changes, relationship changes, exported early-finish movement and total-float screening.
- **Calculated from observed values:** calendar-day variances, proportions and recovery percentages.
- **Engineering inference:** interface and compression risks, candidate recommendation, decision gates and possible causes of date movement.
- **Not established:** actual productivity, cost, resource sufficiency, independent CPM recalculation, schedule-risk confidence levels, live project performance or approval to implement.

*This case study is simulated and intended to demonstrate Project Controls reasoning and reproducible schedule-data analysis.*
