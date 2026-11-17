import unittest
from tasks.t088.baseline import run_code as baseline
from tasks.t088.check import TARGET, validate
from tasks.t088.human import run_code as human
from tasks.t088.init_program import run_code as initial
from tasks.t088.reference import run_code as reference

CONFIG = {"id": "T088-C01", "parameters": {"target": "2^192-2^64-3"}}


class TaskTests(unittest.TestCase):
    def test_seed_exact_binary_chain(self):
        result = validate(initial(), CONFIG)
        self.assertEqual(result["verification_status"], "exact")
        self.assertEqual(initial()["chain"][-1], TARGET)

    def test_human_witness_reproduced(self):
        result = validate(human(), CONFIG)
        self.assertEqual(result["objective"], 202)
        self.assertEqual(reference(), human())

    def test_claimed_score_is_ignored(self):
        solution = human()
        solution["claimed_score"] = -10**9
        self.assertEqual(validate(solution, CONFIG)["objective"], 202)

    def test_binary_and_search_baselines_are_valid(self):
        validate(baseline(), CONFIG)

    def test_small_valid_chain(self):
        small = {"chain": [1, 2, 3, 6, 12, 15]}
        # Feasibility rules are target-specific, so endpoint must be configured target.
        with self.assertRaises(ValueError):
            validate(small, CONFIG)

    def test_invalid_chain_shapes_and_steps(self):
        invalid = [
            {}, {"chain": [1]}, {"chain": [True, 2]}, {"chain": [1, 2.0]},
            {"chain": [1, 2, 2, TARGET]}, {"chain": [1, 3, TARGET]},
            {"chain": [2, TARGET]}, {"chain": [1, 2, TARGET-1]},
        ]
        for candidate in invalid:
            with self.subTest(candidate=candidate):
                with self.assertRaises(ValueError):
                    validate(candidate, CONFIG)

    def test_wrong_configuration(self):
        with self.assertRaises(ValueError):
            validate(human(), {"id": "T088-C01", "parameters": {"target": "other"}})

    def test_other_configuration_is_rejected(self):
        with self.assertRaises(ValueError):
            validate(human(), {"id": "T088-C99", "parameters": {"target": "other"}})


if __name__ == "__main__":
    unittest.main()
