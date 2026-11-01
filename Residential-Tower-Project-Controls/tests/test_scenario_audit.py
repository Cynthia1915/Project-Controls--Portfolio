"""Regression checks for the bundled four P6 scenarios.

Run from the project root:
 python -m unittest discover -s tests -v
"""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "02_Python_ETL" / "analyze_scenarios.py"
spec = importlib.util.spec_from_file_location("analyze_scenarios", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ScheduleAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loaded = {
            label: module.load(ROOT / "01_P6_Exports" / filename)
            for label, filename in module.SCENARIOS.items()
        }

    def test_activity_counts(self):
        for label, tables in self.loaded.items():
            with self.subTest(label=label):
                self.assertEqual(len(tables["TASK"]), 265)

    def test_relationship_counts(self):
        expected = {"Baseline": 362, "Update 01": 362,
                    "Recovery A": 362, "Recovery B": 363}
        for label, count in expected.items():
            self.assertEqual(len(self.loaded[label]["TASKPRED"]), count)

    def test_update_status_counts(self):
        from collections import Counter
        status = Counter(row["status_code"]
                         for row in self.loaded["Update 01"]["TASK"])
        self.assertEqual(status["TK_Complete"], 7)
        self.assertEqual(status["TK_Active"], 3)
        self.assertEqual(status["TK_NotStart"], 255)

    def test_finish_dates(self):
        expected = {"Baseline": "2028-05-13", "Update 01": "2028-05-31",
                    "Recovery A": "2028-05-16", "Recovery B": "2028-05-18"}
        for label, date in expected.items():
            self.assertTrue(
                self.loaded[label]["PROJECT"][0]["scd_end_date"].startswith(date),
                label)

    def test_recovery_logic_delta(self):
        update = module.edge_set(self.loaded["Update 01"])
        a = module.edge_set(self.loaded["Recovery A"])
        b = module.edge_set(self.loaded["Recovery B"])
        self.assertEqual(update, a)
        self.assertEqual(len(b-update), 4)
        self.assertEqual(len(update-b), 3)

    def test_recovery_a_compression(self):
        old = {r["task_code"]: r for r in self.loaded["Update 01"]["TASK"]}
        new = {r["task_code"]: r for r in self.loaded["Recovery A"]["TASK"]}
        delta = {
            code: float(new[code]["target_drtn_hr_cnt"] or 0)
                  - float(row["target_drtn_hr_cnt"] or 0)
            for code, row in old.items()
        }
        self.assertEqual({k: v for k, v in delta.items() if v}, {
            "TST-020": -24.0, "TST-050": -24.0,
            "EXC-030": -16.0, "EXC-040": -16.0})


if __name__ == "__main__":
    unittest.main()
