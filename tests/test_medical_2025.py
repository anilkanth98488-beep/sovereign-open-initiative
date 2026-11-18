import unittest
from modules.us_tax.medical import calculate


class MedicalWorkpaperTests(unittest.TestCase):
    def test_results(self):
        for agi, paid, refunded, expected in [
            ("80000", "9000", "1000", "2000.00"),
            ("80000", "6000", "0", "0.00"),
            ("80000", "5999.99", "0", "0.00"),
            ("0", "25.25", "0", "25.25"),
            ("1.00", "1.00", "0", "0.93"),
        ]:
            with self.subTest(agi=agi, paid=paid):
                self.assertEqual(calculate(2025, agi, paid, refunded)["line_4_excess_usd"], expected)

    def test_unsupported(self):
        for args in [(2026,"0","0","0"), (2025,"-1","0","0"), (2025,"0","0","1"),
                     (2025,"NaN","1","0"), (2025,"0","1.001","0"), (2025,"","1","0")]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                calculate(*args)
