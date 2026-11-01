"""Regression tests for the EVM portfolio model."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from evm import ACCOUNTS, BAC, build_rows, calculate, safe_ratio

class TestEVM(unittest.TestCase):
    def test_account_reconciliation(self):
        self.assertEqual(sum(x[2] for x in ACCOUNTS), BAC)

    def test_formulas(self):
        r = calculate(1000, 500, 400, 500)
        self.assertEqual(r["cv"], -100)
        self.assertEqual(r["sv"], -100)
        self.assertAlmostEqual(r["cpi"], 0.8)
        self.assertAlmostEqual(r["spi"], 0.8)
        self.assertAlmostEqual(r["eac_cpi"], 1250)
        self.assertAlmostEqual(r["eac_remaining_at_budget"], 1100)
        self.assertAlmostEqual(r["eac_cpi_spi"], 1437.5)
        self.assertAlmostEqual(r["etc_cpi"], 750)
        self.assertAlmostEqual(r["vac_cpi"], -250)
        self.assertAlmostEqual(r["tcpi_bac"], 1.2)

    def test_undefined_denominators(self):
        r = calculate(100, 0, 0, 0)
        self.assertIsNone(r["cpi"])
        self.assertIsNone(r["spi"])
        self.assertIsNone(r["eac_cpi"])
        self.assertIsNone(r["eac_cpi_spi"])
        self.assertIsNone(safe_ratio(1, 0))

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            calculate(100, 20, 101, 30)
        with self.assertRaises(ValueError):
            calculate(100, -1, 0, 0)

    def test_series(self):
        rows = build_rows()
        self.assertEqual(len(rows), 12)
        self.assertEqual(rows[-1]["pv"], BAC)
        for field in ("pv", "ev", "ac"):
            self.assertEqual(sorted(row[field] for row in rows), [row[field] for row in rows])
        self.assertLess(rows[-1]["cpi"], 1)
        self.assertLess(rows[-1]["spi"], 1)

if __name__ == "__main__":
    unittest.main()
