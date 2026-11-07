import unittest
from unittest.mock import patch

from tasks.t013.baseline import run_code as baseline
from tasks.t013.check import aperiodic_autocorrelations, validate
from tasks.t013.human import run_code as human
from tasks.t013.init_program import run_code as initial
from tasks.t013.reference import run_code as reference

CONFIG = {"id": "T013-C01", "parameters": {"L": 100}, "direction": "minimize"}


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

    def test_staged_human_witnesses_and_exact_scores(self):
        for config_id, length, energy in (("T013-C02", 80, 352),
                                          ("T013-C03", 120, 872)):
            config = {"id": config_id, "parameters": {"L": length},
                      "direction": "minimize"}
            with patch.dict("os.environ", {"MATHBENCH_CONFIG_ID": config_id}):
                witness = human()
                self.assertEqual(len(witness["sequence"]), length)
                scored = validate({**witness, "claimed_score": -999999}, config)
                self.assertEqual(scored["objective"], energy)
                self.assertEqual(reference(), witness)
                self.assertEqual(len(initial()["sequence"]), length)
                self.assertEqual(len(baseline()["sequence"]), length)
                broken = witness["sequence"][:-1]
                with self.assertRaises(ValueError):
                    validate({"sequence": broken, "claimed_score": energy}, config)

    def test_staged_length_mismatch_rejected(self):
        config = {"id": "T013-C02", "parameters": {"L": 80}}
        with self.assertRaises(ValueError):
            validate({"sequence": [1] * 100}, config)

    def test_environment_switches_between_live_and_staged_configs(self):
        for config_id, length in (("T013-C01", 100), ("T013-C02", 80),
                                  ("T013-C03", 120)):
            with patch.dict("os.environ", {"MATHBENCH_CONFIG_ID": config_id}):
                self.assertEqual(len(initial()["sequence"]), length)
                self.assertEqual(len(human()["sequence"]), length)


if __name__ == "__main__":
    unittest.main()
