import unittest
from tasks.t089.check import determinant_bareiss, validate
from tasks.t089.human import run_code as human
from tasks.t089.init_program import run_code as initial
from tasks.t089.reference import run_code as reference

CONFIG = {"id": "T089-C01", "parameters": {"n": 29, "entries": "±1"}, "direction": "maximize"}


class TaskTests(unittest.TestCase):
    def test_seed_boundary_and_exact_value(self):
        result = validate(initial(), CONFIG)
        self.assertEqual(result["objective"], 27 * 2**28)
        self.assertEqual(result["verification_status"], "exact")

    def test_published_witness_and_independent_formula(self):
        a = human()["matrix"]
        result = validate({"matrix": a, "claimed_score": -1}, CONFIG)
        expected = 320 * 7**12 * 2**28
        self.assertEqual(result["objective"], expected)
        self.assertEqual(result["details"]["signed_determinant"], -expected)
        self.assertEqual(reference()["matrix"], a)

    def test_invalid_dimensions_entries_and_bool(self):
        for sol in ({}, {"matrix": [[1] * 29 for _ in range(28)]}):
            with self.assertRaises(ValueError): validate(sol, CONFIG)
        bad = initial()
        bad["matrix"][0][0] = True
        with self.assertRaises(ValueError): validate(bad, CONFIG)
        bad = initial()
        bad["matrix"][0][0] = 0
        with self.assertRaises(ValueError): validate(bad, CONFIG)

    def test_bareiss_pivot_swap(self):
        self.assertEqual(determinant_bareiss([[0, 1], [1, 0]]), -1)


if __name__ == "__main__":
    unittest.main()
