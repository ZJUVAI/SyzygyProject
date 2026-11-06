import unittest
from fractions import Fraction

from tasks.t080.baseline import run_code as baseline
from tasks.t080.check import objective_fraction, validate
from tasks.t080.human import run_code as human
from tasks.t080.init_program import run_code as initial
from tasks.t080.reference import run_code as reference

CONFIG = {"id": "T080-C01", "parameters": {"steps": 20, "support": ["-1/4", "1/4"], "nonnegative": True}}
EXPECTED = Fraction("108065664771600646574507764702/121527759800529249872686490775")


class TaskTests(unittest.TestCase):
    def test_seed_is_valid(self):
        self.assertEqual(validate(initial(), CONFIG)["verification_status"], "exact")

    def test_human_exact_value_and_provenance(self):
        self.assertEqual(validate(human(), CONFIG)["objective"], str(EXPECTED))
        self.assertEqual(reference(), human())

    def test_scale_invariance_and_claim_ignored(self):
        original = human()
        scaled = {"coefficients": [str(Fraction(x) * 7) for x in original["coefficients"]], "claimed_score": 1e99}
        self.assertEqual(validate(scaled, CONFIG)["objective"], str(EXPECTED))

    def test_invalid_inputs(self):
        for bad in ({}, {"coefficients": [1]*19}, {"coefficients": [1]*19+[True]},
                    {"coefficients": [1]*19+[-1]}, {"coefficients": [1]*19+[float("nan")]},
                    {"coefficients": [0]*20}):
            with self.assertRaises(ValueError):
                validate(bad, CONFIG)

    def test_exact_formula_independent_example(self):
        vals = [Fraction(i+1) for i in range(20)]
        j, b = objective_fraction(vals)
        self.assertEqual(len(b), 39)
        # Independent integer convolution and formula.
        conv = [sum(vals[k]*vals[i-k] for k in range(20) if 0 <= i-k < 20) for i in range(39)]
        expected = (2*sum(x*x for x in conv)+sum(conv[i]*conv[i+1] for i in range(38))) / (3*max(conv)*sum(vals)**2)
        self.assertEqual(j, expected)

    def test_search_baseline_valid(self):
        validate(baseline(), CONFIG)


if __name__ == "__main__":
    unittest.main()
