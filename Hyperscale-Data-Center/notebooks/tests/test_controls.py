"""Unit tests: python -m unittest discover -s Hyperscale-Data-Center/notebooks/tests -v"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from network_monte_carlo import network, forward, simulate
from reconcile_evm import reconcile
from audit_xer import audit


def sample(rel="PR_FS", lag="0"):
    return {"PROJECT": [{"proj_short_name": "TEST", "last_recalc_date": "2026-01-31 17:00"}],
            "TASK": [
                {"task_id": "1", "task_code": "A", "target_drtn_hr_cnt": "10", "status_code": "TK_NotStart"},
                {"task_id": "2", "task_code": "RFS-040", "target_drtn_hr_cnt": "0", "status_code": "TK_NotStart"}],
            "TASKPRED": [{"pred_task_id": "1", "task_id": "2", "pred_type": rel, "lag_hr_cnt": lag}],
            "PROJCOST": [], "PROJWBS": []}


class NetworkTests(unittest.TestCase):
    def test_fs_forward(self):
        t = sample()
        order, _, inc, dur = network(t)
        starts, ends = forward(order, inc, dur)
        self.assertEqual(ends["2"], 10)
        self.assertEqual(starts["2"], 10)

    def test_ff_forward(self):
        t = sample("PR_FF", "3")
        order, _, inc, dur = network(t)
        starts, ends = forward(order, inc, dur)
        self.assertEqual(ends["2"], 13)

    def test_ss_forward(self):
        t = sample("PR_SS", "4")
        order, _, inc, dur = network(t)
        starts, _ = forward(order, inc, dur)
        self.assertEqual(starts["2"], 4)

    def test_cycle_rejected(self):
        t = sample()
        t["TASKPRED"].append({"pred_task_id": "2", "task_id": "1", "pred_type": "PR_FS", "lag_hr_cnt": "0"})
        with self.assertRaisesRegex(ValueError, "Cycle"):
            network(t)

    def test_missing_reference_rejected(self):
        t = sample()
        t["TASKPRED"][0]["pred_task_id"] = "999"
        with self.assertRaisesRegex(ValueError, "Unknown"):
            network(t)

    def test_reproducible_seed(self):
        t = sample()
        a, samples_a = simulate(t, runs=50, seed=12)
        b, samples_b = simulate(t, runs=50, seed=12)
        self.assertEqual(a, b)
        self.assertEqual(samples_a, samples_b)
        self.assertLessEqual(a["p50_relative_work_hours"], a["p80_relative_work_hours"])
        self.assertLessEqual(a["p80_relative_work_hours"], a["p90_relative_work_hours"])


class EvmTests(unittest.TestCase):
    def test_ratios_and_forecast(self):
        rows = [{"activity_id": "A", "data_date": "2026-01-31", "bac": "100", "pv": "60", "ev": "40", "ac": "50"},
                {"activity_id": "A", "data_date": "2026-02-28", "bac": "100", "pv": "70", "ev": "60", "ac": "65"}]
        r = reconcile(rows, "2026-01-31", expected_bac=100)
        self.assertTrue(r["bac_reconciles"])
        self.assertEqual(r["cpi"], 0.8)
        self.assertEqual(r["eac_cpi_based"], 125)
        self.assertEqual(r["spi"], round(40/60, 6))

    def test_duplicate_period_activity_rejected(self):
        row = {"activity_id": "A", "data_date": "2026-01-31", "bac": "100", "pv": "20", "ev": "10", "ac": "10"}
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            reconcile([row, row], "2026-01-31")

    def test_zero_denominators(self):
        row = {"activity_id": "A", "data_date": "2026-01-31", "bac": "100", "pv": "0", "ev": "0", "ac": "0"}
        r = reconcile([row], "2026-01-31", expected_bac=100)
        self.assertIsNone(r["cpi"])
        self.assertIsNone(r["spi"])
        self.assertIsNone(r["eac_cpi_based"])


if __name__ == "__main__":
    unittest.main()
