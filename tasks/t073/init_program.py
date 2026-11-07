"""Standalone 96-point signed-permutation 5-design seed on S^3."""

import os
from itertools import permutations, product


def _rational_text(numerator, denominator):
    if numerator == 0:
        return "0"
    from math import gcd
    common = gcd(abs(numerator), denominator)
    numerator //= common
    denominator //= common
    return str(numerator) if denominator == 1 else f"{numerator}/{denominator}"


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T073-C01")
    if chosen != "T073-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    orbit = set()
    for permuted in set(permutations((1, 1, 2, 0))):
        active = [i for i, value in enumerate(permuted) if value]
        for signs in product((-1, 1), repeat=3):
            point = list(permuted)
            for axis, sign in zip(active, signs):
                point[axis] *= sign
            orbit.add(tuple(point))
    return {
        "minimal_polynomial": [-6, 0, 1],
        "isolating_interval": ["2", "3"],
        "points": [
            [["0", _rational_text(value, 6)] for value in point]
            for point in sorted(orbit)
        ],
    }
    # EVOLVE-BLOCK-END
