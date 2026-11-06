import unittest
from unittest.mock import patch
from tasks.t097.baseline import run_code as baseline
from tasks.t097.check import TARGET, validate
from tasks.t097.human import run_code as human
from tasks.t097.init_program import run_code as initial
from tasks.t097.reference import run_code as reference

CONFIG = {"id": "T097-C01", "parameters": {"target": "2^192-2^64-3"}}


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
            validate(human(), {"id": "T097-C01", "parameters": {"target": "other"}})

    def test_staged_public_witnesses_and_config_aware_programs(self):
        cases = [
            ("T097-C02", "2^221-5", 230),
            ("T097-C03", "2^521-3", 532),
        ]
        for cid, target, length in cases:
            config = {"id": cid, "parameters": {"target": target}}
            with patch.dict("os.environ", {"MATHBENCH_CONFIG_ID": cid}):
                public = human()
                reference_result = reference()
                seed = initial()
                search = baseline()
            self.assertEqual(public, reference_result)
            checked = validate(public, config)
            self.assertEqual(checked["objective"], length)
            self.assertEqual(checked["verification_status"], "exact")
            validate(seed, config)
            validate(search, config)
            tampered = dict(public, claimed_score=-999999)
            self.assertEqual(validate(tampered, config)["objective"], length)

    def test_wrong_staged_endpoint_is_rejected(self):
        config = {"id": "T097-C02", "parameters": {"target": "2^221-5"}}
        with patch.dict("os.environ", {"MATHBENCH_CONFIG_ID": "T097-C02"}):
            chain = human()
        chain["chain"][-1] -= 1
        with self.assertRaises(ValueError):
            validate(chain, config)


if __name__ == "__main__":
    unittest.main()
