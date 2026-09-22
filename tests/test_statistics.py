import copy
import json
import unittest
from pathlib import Path

from litec_wam_public.metrics import exact_paired_test, task_macro_rate, wilson_interval
from litec_wam_public.report import compute_report
from litec_wam_public.interface import SPECS


class StatisticsTests(unittest.TestCase):
    def test_wilson_boundary_counts(self):
        self.assertAlmostEqual(wilson_interval(0, 10)[0], 0)
        self.assertAlmostEqual(wilson_interval(10, 10)[1], 1)
        self.assertAlmostEqual(wilson_interval(18, 20)[0], 0.6989663548)
        self.assertAlmostEqual(wilson_interval(18, 20)[1], 0.9721335188)

    def test_exact_paired_test(self):
        self.assertEqual(exact_paired_test(0, 0), 1)
        self.assertEqual(exact_paired_test(3, 0), 0.25)
        self.assertEqual(exact_paired_test(5, 1), 0.21875)
        self.assertEqual(exact_paired_test(64, 30), exact_paired_test(30, 64))

    def test_macro_is_not_pooled(self):
        self.assertEqual(task_macro_rate([(1, 1), (0, 99)]), 0.5)

    def test_invalid_counts(self):
        for successes, trials in [(3, 2), (-1, 10), (0, 0), (True, 10), (1.5, 10)]:
            with self.assertRaises(ValueError):
                wilson_interval(successes, trials)

    def test_reported_results_and_pair_integrity(self):
        data = json.loads((Path(__file__).resolve().parents[1] / "data/paper_results.json").read_text())
        report = compute_report(data)
        self.assertAlmostEqual(report["arx5_macro_percent"], 91.8629685176)
        self.assertAlmostEqual(report["feedback"]["gain_percentage_points"], 7.0833333333)
        self.assertAlmostEqual(report["feedback"]["seed_sign_test_p"], 0.21875)
        altered = copy.deepcopy(data)
        altered["feedback"]["feedback_only"] = 65
        with self.assertRaises(ValueError):
            compute_report(altered)

    def test_action_contract_rejects_wrong_shape_and_nan(self):
        spec = SPECS["so_arm101"]
        spec.validate_chunk([[0.0] * 12 for _ in range(8)])
        for chunk in [[[0.0] * 7 for _ in range(8)], [[float("nan")] * 12 for _ in range(8)]]:
            with self.assertRaises(ValueError):
                spec.validate_chunk(chunk)


if __name__ == "__main__":
    unittest.main()
