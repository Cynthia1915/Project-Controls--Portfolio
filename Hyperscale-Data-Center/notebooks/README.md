# Data Processing and Automation | Schedule QA

[← Case study](../README.md)

The repository now includes a **read-only XER structural audit script**: [audit_xer.py](./audit_xer.py).

## Usage

Requires Python 3.9+ with no external packages:

```bash
python Hyperscale-Data-Center/notebooks/audit_xer.py \
  DC-HYP-FINAL-6_Update01_COST_LOADED.xer \
  --output-dir audit_outputs
```

Outputs: `schedule_audit_summary.json` and `schedule_audit_findings.csv`. The script checks dependency references and cycles, positive/negative lags, open ends, progress status consistency, and P6 expense cost data.

**Limitations:** This is not a P6 CPM scheduling engine, a DCMA 14-point certification, or a complete EVM pipeline. Positive lag requires engineering review, not automatic deletion. Schedule % Complete may be 100% while remaining duration is nonzero. Zero XER expense actual cost does not prove that externally modeled AC is zero. Reconcile external EVM and dashboard data separately.

## Reporting workflow (partially implemented)

```text
Primavera P6 baseline / update
             ↓
 Read-only XER structure audit  ← implemented
             ↓
 Data extraction and validation
             ↓
 EVM, schedule and forecast analysis
             ↓
      Reporting dataset
             ↓
 Google Sheets / Looker Studio
```

The complete, executable EVM/dashboard transformation pipeline is **not yet published**. For other evidence see the [reporting workbook](../data/), [schedule summaries](../primavera/) and [dashboard screenshots](../dashboard/).
