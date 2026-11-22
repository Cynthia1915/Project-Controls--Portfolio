# Hyperscale Data Center — My Monte Carlo schedule-risk experiment

**Run date:** 22 November 2026  
**Source:** user-provided `DC-HYP-FINAL-tolooker(4).xer` (not committed to this public repository)  
**Project:** DC-HYP-FINAL-6  
**P6 data date:** 31 January 2026, 17:00  
**Milestone:** RFS-040 — Ready for Service

## What I modeled and why\n\nI used the exported Primavera activity network to test how duration uncertainty could affect the modeled Ready for Service milestone. I kept the first implementation intentionally reproducible, using the existing precedence engine and fixed assumptions. My focus was on translating the distribution into a management-facing risk signal without overstating confidence.\n\n## Model and run

- Parsed 808 TASK records and 1,406 TASKPRED relationships.
- Reproduced the existing repository's network topological forward-pass logic with FS/SS/FF/SF and lags.
- 10,000 iterations; fixed Python random seed 42.
- Independent triangular activity-duration multipliers: minimum 0.80, mode 1.00, maximum 1.30.
- Completed tasks zeroed; active tasks use remaining duration; other tasks use target duration.
- **All results are relative continuous-hour outputs, not calendar dates.**

## Experimental outputs

| Measure | Relative modeled hours |
| --- | ---: |
| Deterministic reference | 3,296.00 |
| P10 | 3,381.88 |
| P50 | 3,440.92 |
| P80 | 3,489.60 |
| P90 | 3,527.74 |
| P80 minus deterministic reference | +193.60 |
| Probability of exceeding deterministic reference | 99.96% |

**Interpretation:** Under the illustrative, independently sampled duration factors, the P80 modeled relative-hour finish exceeds the deterministic reference by 193.60 hours. This is **not** a contractual schedule contingency in P6 working hours and cannot be translated to a date without a validated calendar-aware engine. The 99.96% figure is not the probability of missing the contractual RFS date.

## My interpretation and next engineering steps\n\nThe P80 result is 193.60 relative hours above the deterministic reference. This suggests meaningful exposure within my **illustrative** model, but it does not establish that the contractual date will be missed. Before using the result for a mitigation or contingency decision, I would verify calendar and data-date behavior against Primavera, calibrate the uncertainty assumptions, and evaluate shared risks and driving-path sensitivity.\n\n## Engineering limitations and required next phase

1. XER source was provided in chat, but is not stored in this public repository. The repository's existing `network_monte_carlo.py` is the reference implementation; its outputs can be reproduced by running it against the same XER with `--runs 10000 --seed 42 --target RFS-040`.
2. The model uses continuous elapsed hours and does not reconstruct P6 working calendars, exceptions, data-date anchoring, constraints, scheduling options or resource leveling.
3. Independent triangular distributions are hypothetical and not empirically calibrated; shared procurement, design and commissioning risks may be correlated.
4. Completed activities are zero-duration but the full network is not reconstructed around actual dates and progress logic.
5. Deterministic P6 date reconciliation, activity risk drivers and criticality indices remain **unvalidated/not calculated**.
6. Before presenting contractual P50/P80/P90 dates: reconcile deterministic P6 logic and calendars, calibrate risk distributions, test correlated risks, and rerun with a calendar-aware scheduler.

**Release decision:** publish as a transparent *experimental schedule-risk analysis* only, not as a P6-validated probabilistic RFS forecast.
