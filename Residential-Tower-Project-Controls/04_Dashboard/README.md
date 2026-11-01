# Looker Studio dashboard specification

**Status:** design specification; no deployed dashboard.

Data source: generated `03_Processed_Data/Activities.csv` and `Relationships.csv`, preferably staged in Google Sheets.

## Pages

1. **Executive Overview** — total activities, completion status, baseline/update forecast finish, schedule variance and scenario comparison.
2. **Schedule Performance** — activity status, milestones, float and critical activities (requires verified source fields and definitions).
3. **Recovery Analysis** — recovery A/B finish variance, recovered days, logic changes and duration changes.
4. **Risk & Management Decisions** — execution risks, resource feasibility gaps, cost/safety constraints and recommended follow-up.

## Important

The initial extractor preserves native XER TASK and TASKPRED field names. KPI transformation and date parsing must be validated against the actual files before charts are built. Do not count all four scenarios together as one project total; filter by scenario.
