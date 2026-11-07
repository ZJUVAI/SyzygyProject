"""Independent integer checks for generated structural proposals."""
import json
import math
import os
import random
import tempfile
import time
import unittest
from unittest.mock import patch

from tasks.t020.check import TARGETS, validate
from tasks.t020.evolution import _prune, run_code
from tasks.t020.structured_search import (
    binary_chain, exponent_search, lift_exponents, quotient_chain, tail_candidate,
)


def assert_chain(test, chain, target):
    test.assertEqual(chain[0], 1)
    test.assertEqual(chain[-1], target)
    old = {1}
    for previous, value in zip(chain, chain[1:]):
        test.assertGreater(value, previous)
        test.assertTrue(any(value-x in old for x in old), value)
        old.add(value)


class StructuredSearchTests(unittest.TestCase):
    def test_non_star_lift_and_all_orientations(self):
        # 8=4+4 uses neither operand equal to the previous exponent 7.
        path = [1, 2, 3, 4, 7, 8, 15]
        for seed in range(8):
            chain = lift_exponents(path, random.Random(seed))
            assert_chain(self, chain, (1 << 15)-1)
            assert_chain(self, _prune(chain), (1 << 15)-1)
        with self.assertRaises(ValueError):
            lift_exponents([1, 2, 5])

    def test_small_exponent_search_is_an_exact_chain(self):
        for target in [1, 2, 15, 27, 109, 218, 519]:
            for general in [False, True]:
                chain = exponent_search(target, random.Random(target),
                                        time.monotonic()+0.03, 1000, general)
                assert_chain(self, chain, target)

    def test_tail_splits_for_both_fixed_targets(self):
        for cid, bits, defect in [('T020-C02', 221, 5), ('T020-C03', 521, 3)]:
            config = {'id': cid, 'parameters': {'target': TARGETS[cid][0]}}
            for trailing in [defect.bit_length(), 5, 13, 32, 64, bits-2]:
                chain = _prune(tail_candidate(bits, defect, trailing,
                                             binary_chain(bits-trailing)))
                checked = validate({'chain': chain, 'claimed_score': -999}, config, strict=True)
                self.assertEqual(checked['objective'], len(chain)-1)
                damaged = chain.copy()
                damaged[-1] -= 1
                with self.assertRaises(ValueError):
                    validate({'chain': damaged}, config, strict=True)

    def test_quotient_and_remainder_paths(self):
        paths = {n: binary_chain(n) for n in range(1, 100)}
        for target in [127, 221, 509, (1 << 221)-5, (1 << 521)-3]:
            for divisor in [2, 3, 7, 31, target//3, math.isqrt(target)]:
                if divisor < target:
                    chain = quotient_chain(target, divisor, paths)
                    assert_chain(self, chain, target)
                    assert_chain(self, _prune(chain), target)

    def test_shared_sparse_defect_proposals_have_positive_dependencies(self):
        from tasks.t020 import evolution
        target = TARGETS['T020-C01'][1]
        prune = evolution._prune
        def checked_prune(chain):
            assert_chain(self, chain, target)
            return prune(chain)
        with patch.object(evolution, '_prune', side_effect=checked_prune):
            chain, counts = evolution._shared_target_search(
                binary_chain(target), random.Random(101), time.monotonic()+2)
        assert_chain(self, chain, target)
        self.assertGreater(counts['shared_exponent_proposals'], 0)

    def test_cold_and_damaged_warm_start_remain_valid(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, 'damaged.json')
            with open(path, 'w') as stream:
                json.dump({'chain': [1, 2, 2, TARGETS['T020-C02'][1]]}, stream)
            for warm in ['', path]:
                for cid in ['T020-C02', 'T020-C03']:
                    with patch.dict(os.environ, {'MATHBENCH_CONFIG_ID': cid,
                                    'MATHBENCH_EVOLUTION_SECONDS': '0.1',
                                    'MATHBENCH_WARM_START': warm, 'MATHBENCH_SEED': '20'}):
                        solution = run_code()
                    config = {'id': cid, 'parameters': {'target': TARGETS[cid][0]}}
                    validate(solution, config, strict=True)


if __name__ == '__main__':
    unittest.main()
