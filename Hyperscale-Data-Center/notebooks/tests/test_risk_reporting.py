"""Independent checks for the relative-hour risk report."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from risk_reporting import percentile, report


class RiskReportingTests(unittest.TestCase):
    def setUp(self):
        self.summary = {
            "runs": 5, "seed": 42, "target_milestone": "RFS-040",
            "nominal_relative_work_hours": 10.0
        }
        self.samples = [8.0, 9.0, 10.0, 12.0, 16.0]

    def test_quantiles_and_probability(self):
        result = report(self.summary, self.samples, bins=4)
        self.assertEqual(result["p50_relative_work_hours"], 10)
        self.assertEqual(result["p80_relative_work_hours"], 11.6)
        self.assertEqual(result["p90_relative_work_hours"], 14.4)
        self.assertEqual(result["probability_exceeding_nominal"], 0.4)
        self.assertEqual(sum(b["samples"] for b in result["histogram"]), 5)
        self.assertEqual(result["validation_status"], "UNVALIDATED_P6_CALENDAR_EQUIVALENCE")

    def test_sample_count_mismatch_rejected(self):
        self.summary["runs"] = 6
        with self.assertRaises(ValueError):
            report(self.summary, self.samples)

    def test_invalid_samples_rejected(self):
        with self.assertRaises(ValueError):
            report(self.summary, [1.0, float("nan")])

    def test_constant_samples(self):
        self.summary["runs"] = 3
        result = report(self.summary, [5.0] * 3, bins=5)
        self.assertEqual(sum(b["samples"] for b in result["histogram"]), 3)

    def test_empty_percentile_rejected(self):
        with self.assertRaises(ValueError):
            percentile([], .5)


if __name__ == "__main__":
    unittest.main()
