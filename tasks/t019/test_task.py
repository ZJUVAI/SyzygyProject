import unittest

from tasks.t019.check import validate
from tasks.t019.human import run_code as human
from tasks.t019.init_program import run_code as initial

CONFIG = {"id": "T019-C01", "parameters": {"k": 343}, "direction": "minimize"}


class TaskTests(unittest.TestCase):
    def test_seed_feasible_and_objective(self):
        result = validate(initial(), CONFIG)
        self.assertEqual(result["objective"], 342 * initial()["tuple"][1])
        self.assertEqual(result["verification_status"], "exact")

    def test_human_witness_exact_diameter_and_claim_ignored(self):
        result = validate({**human(), "claimed_score": -1}, CONFIG)
        self.assertEqual(result["objective"], 2340)
        self.assertEqual(result["details"]["prime_count_checked"], 68)

    def test_translation_and_negative_values(self):
        values = [x - 5000 for x in human()["tuple"]]
        self.assertEqual(validate({"tuple": values}, CONFIG)["objective"], 2340)

    def test_rejects_bad_size_bool_noninteger_and_duplicates(self):
        good = human()["tuple"]
        for values in (good[:-1], good[:-1] + [True], good[:-1] + [1.5], good[:-1] + [good[0]]):
            with self.assertRaises(ValueError):
                validate({"tuple": values}, CONFIG)

    def test_rejects_covered_prime_residues(self):
        # Every residue modulo 2 is present; duplicate padding keeps the length.
        bad = list(range(343))
        with self.assertRaisesRegex(ValueError, "prime 2"):
            validate({"tuple": bad}, CONFIG)

    def test_config_parameters_match_id(self):
        with self.assertRaises(ValueError):
            validate({"tuple": human()["tuple"]}, {"id": "T019-C01", "parameters": {"k": 342}})

    def test_unknown_configuration_is_rejected(self):
        with self.assertRaises(ValueError):
            validate({"tuple": human()["tuple"]}, {"id": "T019-UNKNOWN", "parameters": {"k": 343}})


if __name__ == "__main__":
    unittest.main()
