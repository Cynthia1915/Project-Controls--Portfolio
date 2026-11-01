# Residential Tower | Project Controls & Digital PMO

**Status:** Work in progress — simulated construction scheduling case study.

This case study studies a 15-story residential tower with two basement levels using Primavera P6 XER exports, reproducible Python extraction, schedule recovery comparisons and dashboard-ready reporting.

## Schedule scenarios

| Scenario | XER source | Reported finish (unverified) |
|---|---|---|
| Baseline | RES-TWR-BL01.xer | 2028-05-13 |
| Update 01 | RES-TWR-UPD01.xer | 2028-05-31 |
| Recovery A | RES-TWR-REC-A.xer | 2028-05-16 |
| Recovery B | RES-TWR-REC-B.xer | 2028-05-18 |

Reported dates are prior working assumptions, **not verified outputs of this repository's pipeline**. The update was previously described as 7 completed, 3 in progress and 255 not started out of 265 activities; these counts require verification against the XER files.

## Data provenance

The four source exports currently live in [the source repository](https://github.com/Cynthia1915/Project-Controls-Portfolio). They have **not yet been copied** into this destination folder. Download them into `01_P6_Exports/` locally (see that folder's README) before running the ETL. Never change the original exports.

## Quick start

```bash
python 02_Python_ETL/extract_xer.py --input 01_P6_Exports --output 03_Processed_Data
python -m unittest discover -s tests -v
```

Python 3.10+; standard library only. Extraction writes one row per TASK and TASKPRED record, with scenario and source-file provenance. This is an initial raw-data pipeline, **not** a CPM scheduling engine or independently validated critical-path computation.

## Repository structure

- `01_P6_Exports/`: original XER input files (not committed here)
- `02_Python_ETL/`: reusable XER reader and CSV exporter
- `03_Processed_Data/`: generated output (not committed)
- `04_Dashboard/`: dashboard specification and field mapping
- `05_Reports/`: engineering interpretation and limitations
- `tests/`: automated parser tests

## Intended reporting

1. Executive overview
2. Schedule performance
3. Recovery analysis
4. Risk and management decisions

**Engineering limitations:** Recovery A/B are simulated. No verified resource loading, construction productivity, cost or site feasibility assessment is included. Do not present recovered days as an approved recovery plan.

## Next steps

1. Place the original four XER files in the input folder.
2. Run the extractor and verify activity counts, project finish fields and relationship counts.
3. Build a validated baseline-to-update comparison using actual schedule date fields and documented calendar conventions.
4. Evaluate changed logic and duration compression in recovery cases.
5. Publish Looker Studio dashboard only after reconciling all metrics.
