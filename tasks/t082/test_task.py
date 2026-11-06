import unittest
from fractions import Fraction

from tasks.t082.baseline import run_code as baseline
from tasks.t082.check import EXPECTED, objective_fraction, validate
from tasks.t082.human import run_code as human
from tasks.t082.init_program import run_code as initial
from tasks.t082.reference import run_code as reference

CONFIG = {"id": "T082-C01", "parameters": EXPECTED}
EXPECTED_SCORE = Fraction("64757565083624785688821235069923/170000000000000000000000000000000")


class TaskTests(unittest.TestCase):
    def test_seed_valid(self):
        self.assertEqual(validate(initial(), CONFIG)["verification_status"], "exact")

    def test_human_exact_value_and_source_artifact(self):
        result = validate(human(), CONFIG)
        self.assertEqual(result["objective"], str(EXPECTED_SCORE))
        self.assertEqual(reference(), human())
        self.assertEqual(result["details"]["integral"], "1")

    def test_scale_is_not_admissible_and_claim_ignored(self):
        candidate = human()
        candidate["claimed_score"] = 0
        self.assertEqual(validate(candidate, CONFIG)["objective"], str(EXPECTED_SCORE))
        scaled = {"heights": [str(Fraction(x) * 2) for x in initial()["heights"]]}
        with self.assertRaises(ValueError):
            validate(scaled, CONFIG)

    def test_reject_invalid_constraints(self):
        for bad in ({}, {"heights": [Fraction(1, 2)] * 50},
                    {"heights": [Fraction(1, 2)] * 50 + [True]},
                    {"heights": [Fraction(1, 2)] * 50 + [Fraction(-1, 2)]},
                    {"heights": [Fraction(1, 2)] * 50 + [float("nan")]},
                    {"heights": [Fraction(1, 2)] * 50 + [Fraction(3, 2)]}):
            with self.assertRaises(ValueError):
                validate(bad, CONFIG)

    def test_both_shift_signs_and_zero_extension(self):
        vals = [Fraction(1, 2)] * 51
        value, lag, profile = objective_fraction(vals)
        self.assertEqual(value, Fraction(1, 2))
        self.assertIn(lag, range(-50, 51))
        self.assertEqual(len(profile), 101)
        self.assertEqual(profile[0][1], Fraction(1, 102))
        self.assertEqual(profile[-1][1], Fraction(1, 102))
        self.assertEqual([v for _, v in profile], [v for _, v in reversed(profile)])

    def test_independent_lag_calculation(self):
        vals = [Fraction(1, 2)] * 51
        vals[0] += Fraction(1, 6)
        vals[1] -= Fraction(1, 6)
        value, lag, _ = objective_fraction(vals)
        direct = max(Fraction(2, 51) * sum(
            (vals[i] * (1-vals[i+k]) for i in range(51) if 0 <= i+k < 51), Fraction(0))
            for k in range(-50, 51))
        self.assertEqual(value, direct)

    def test_search_valid(self):
        self.assertEqual(validate(baseline(), CONFIG)["verification_status"], "exact")


if __name__ == "__main__":
    unittest.main()
