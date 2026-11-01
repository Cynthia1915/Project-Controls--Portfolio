# Original Primavera P6 XER exports

These four unmodified source exports are included to make the schedule case study reproducible:

- `RES-TWR-BL01.xer` — baseline
- `RES-TWR-UPD01.xer` — Update 01
- `RES-TWR-REC-A.xer` — duration-compression recovery
- `RES-TWR-REC-B.xer` — logic-resequencing recovery

They were copied from the separate [source repository](https://github.com/Cynthia1915/Project-Controls-Portfolio) on 1 November 2026. They should not be edited by the ETL scripts.

To regenerate outputs from the project root:

```bash
python 02_Python_ETL/analyze_scenarios.py --input 01_P6_Exports --output 03_Processed_Data
```

These are simulated project schedules, not confidential live client records.
