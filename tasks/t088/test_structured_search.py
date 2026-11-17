"""Independent integer checks for generated structural proposals."""
import json
import math
import os
import random
import tempfile
import time
import unittest
from unittest.mock import patch

from tasks.t088.check import TARGET, validate
from tasks.t088.evolution import _prune, run_code
from tasks.t088.structured_search import (
    binary_chain, exponent_search, lift_exponents, quotient_chain,
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
        for target in [1, 2, 15, 27, 109]:
            for general in [False, True]:
                chain = exponent_search(target, random.Random(target),
                                        time.monotonic()+0.03, 1000, general)
                assert_chain(self, chain, target)

    def test_quotient_and_remainder_paths(self):
        paths = {n: binary_chain(n) for n in range(1, 100)}
        for target in [127, 192, 509, TARGET]:
            for divisor in [2, 3, 7, 31, target//3, math.isqrt(target)]:
                if divisor < target:
                    chain = quotient_chain(target, divisor, paths)
                    assert_chain(self, chain, target)
                    assert_chain(self, _prune(chain), target)

    def test_shared_sparse_defect_proposals_have_positive_dependencies(self):
        from tasks.t088 import evolution
        target = TARGET
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
                json.dump({'chain': [1, 2, 2, TARGET]}, stream)
            for warm in ['', path]:
                with patch.dict(os.environ, {'MATHBENCH_CONFIG_ID': 'T088-C01',
                                'MATHBENCH_EVOLUTION_SECONDS': '0.1',
                                'MATHBENCH_WARM_START': warm, 'MATHBENCH_SEED': '20'}):
                    solution = run_code()
                config = {'id': 'T088-C01', 'parameters': {'target': '2^192-2^64-3'}}
                validate(solution, config, strict=True)


if __name__ == '__main__':
    unittest.main()
