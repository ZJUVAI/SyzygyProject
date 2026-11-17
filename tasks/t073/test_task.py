import unittest
from tasks.t073.baseline import run_code as baseline
from tasks.t073.check import aperiodic_autocorrelations, validate
from tasks.t073.human import run_code as human
from tasks.t073.init_program import run_code as initial
from tasks.t073.reference import run_code as reference

CONFIG = {"id": "T073-C01", "parameters": {"L": 100}, "direction": "minimize"}


class TaskTests(unittest.TestCase):
    def test_seed_is_feasible(self):
        result = validate(initial(), CONFIG)
        self.assertEqual(result["verification_status"], "exact")
        self.assertEqual(len(result["details"]["aperiodic_autocorrelations"]), 99)

    def test_human_witness_is_exact_and_pinned(self):
        sequence = human()["sequence"]
        result = validate({"sequence": sequence, "claimed_score": -1}, CONFIG)
        self.assertEqual(result["objective"], 578)
        self.assertEqual(reference()["sequence"], sequence)

    def test_invalid_entries_and_dimensions(self):
        with self.assertRaises(ValueError):
            validate({}, CONFIG)
        with self.assertRaises(ValueError):
            validate({"sequence": [1] * 99}, CONFIG)
        for bad in (True, 1.0, 0, -2):
            sequence = [1] * 100
            sequence[0] = bad
            with self.assertRaises(ValueError):
                validate({"sequence": sequence}, CONFIG)

    def test_baseline_search_changes_seed_energy(self):
        self.assertLess(validate(baseline(), CONFIG)["objective"],
                        validate(initial(), CONFIG)["objective"])

    def test_correlation_count(self):
        self.assertEqual(len(aperiodic_autocorrelations([1, -1, 1])), 2)

    def test_non_official_length_rejected(self):
        config = {"id": "T073-C01", "parameters": {"L": 80}}
        with self.assertRaises(ValueError):
            validate({"sequence": [1] * 100}, config)


if __name__ == "__main__":
    unittest.main()
