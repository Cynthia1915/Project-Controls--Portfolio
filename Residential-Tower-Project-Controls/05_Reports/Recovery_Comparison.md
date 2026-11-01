# Recovery comparison — verified from four uploaded XER exports

| Scenario | Stored scheduled finish | Activities | Relationships |
|---|---|---:|---:|
| Baseline | 2028-05-13 16:00 | 265 | 362 |
| Update 01 | 2028-05-31 16:00 | 265 | 362 |
| Recovery A | 2028-05-16 16:00 | 265 | 362 |
| Recovery B | 2028-05-18 16:00 | 265 | 363 |

The Update 01 schedule is 18 calendar days later than baseline. Recovery A reduces this delay by 15 calendar days, leaving 3 days; Recovery B reduces it by 13 days, leaving 5 days.

## Activity and logic comparisons

Comparisons were keyed by `TASK.task_code`, and relationship endpoints were normalized from internal `task_id` to activity codes before comparing `TASKPRED` rows.

- **Recovery A:** four target durations are shorter than Update 01: TST-020 (-24 hours), TST-050 (-24 hours), EXC-030 (-16 hours), EXC-040 (-16 hours). The relationship set is unchanged.
- **Recovery B:** no target duration changes; four relationships added and three removed relative to Update 01. Added relationships include TST-010 → TST-020 (SS +80h), TST-020 → TST-030 (SS +112h), TST-040 → TST-050 (SS +80h), and TST-040 → M-HANDOVER (FS +0h).
- **Update 01 status:** 7 complete, 3 in progress, 255 not started.

## Engineering qualifications

These are stored P6 fields and file-to-file comparisons, not an independently recalculated CPM network. Recovery B's logic overlaps must be checked for construction sequencing, site access, productivity and safety. Neither recovery option is resource-loaded or cost-validated by this comparison. A shorter forecast finish does not establish execution feasibility.
