import unittest
from unittest.mock import patch
import os
import random
import numpy as np
from tasks.t018.check import determinant_bareiss, validate
from tasks.t018.evolution import _gf27_hadamard, _paley_extension
from tasks.t018.human import run_code as human
from tasks.t018.init_program import run_code as initial
from tasks.t018.reference import run_code as reference

CONFIG = {"id": "T018-C01", "parameters": {"n": 29, "entries": "±1"}, "direction": "maximize"}


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

    def test_order27_human_and_public_witness_exact(self):
        from tasks.t018 import human, reference
        config = {"id": "T018-C02", "parameters": {"n": 27, "entries": "±1"}, "direction": "maximize"}
        with patch.dict(os.environ, {"MATHBENCH_CONFIG_ID": "T018-C02"}):
            h = human.run_code()
            public = reference.run_code()
        self.assertEqual(validate(h, config)["objective"], 12611693314584870912)
        self.assertEqual(validate(public, config)["objective"], 13293406466724593664)
        broken = {"matrix": [r[:] for r in public["matrix"]]}
        broken["matrix"][0][0] *= -1
        with self.assertRaises(ValueError):
            # Wrong dimensions and Boolean damage are both rejected.
            validate({"matrix": broken["matrix"][:-1]}, config)
        claimed = validate({**public, "claimed_score": 0}, config)
        self.assertEqual(claimed["objective"], 13293406466724593664)

    def test_unknown_config_id_rejected(self):
        from tasks.t018.human import run_code
        with patch.dict(os.environ, {"MATHBENCH_CONFIG_ID": "T018-C99"}):
            with self.assertRaises(ValueError): run_code()

    def test_paley_hadamard_seed_and_bordered_determinant(self):
        hadamard = _gf27_hadamard()
        self.assertTrue(np.array_equal(hadamard @ hadamard.T, 28 * np.eye(28, dtype=int)))
        matrix, border_l1 = _paley_extension(random.Random(89), hadamard)
        self.assertEqual(border_l1, 140)
        result = validate({"matrix": matrix.tolist()}, CONFIG)
        self.assertEqual(result["objective"], 6 * 28**14)


if __name__ == "__main__":
    unittest.main()
