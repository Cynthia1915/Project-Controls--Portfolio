"""Unit tests for the raw XER parser."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "02_Python_ETL" / "extract_xer.py"
spec = importlib.util.spec_from_file_location("extract_xer", MODULE)
xer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xer)


class XerTests(unittest.TestCase):
    def test_parses_tables_and_preserves_empty_values(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "sample.xer"
            p.write_text("%ERMHDR\t8.4\n%T\tTASK\n%F\ttask_id\ttask_name\n%R\t10\t\n%T\tTASKPRED\n%F\ttask_pred_id\n%R\t1\n%E\n", encoding="utf-8")
            rows = list(xer.read_xer(p))
            self.assertEqual(rows, [
                ("TASK", {"task_id": "10", "task_name": ""}),
                ("TASKPRED", {"task_pred_id": "1"}),
            ])

    def test_rejects_extra_values(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.xer"
            p.write_text("%T\tTASK\n%F\tid\n%R\t1\t2\n")
            with self.assertRaisesRegex(ValueError, "too many"):
                list(xer.read_xer(p))

    def test_exports_scenario_and_source(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "RES-TWR-BL01.xer"
            p.write_text("%T\tTASK\n%F\ttask_id\n%R\t42\n")
            out = Path(d) / "output"
            self.assertEqual(xer.export_records([p], out)["TASK"], 1)
            self.assertIn("RES-TWR-BL01", (out / "Activities.csv").read_text())


if __name__ == "__main__":
    unittest.main()
