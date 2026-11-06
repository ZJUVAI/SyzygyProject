"""Deterministic finite construction for a (24,14,4) covering."""
import os
from itertools import combinations


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T060-C01") != "T060-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    points = tuple(range(24))
    blocks = []
    covered = set()
    # Each uncovered four-set receives one deterministic 14-set containing it.
    # At most C(24,4)=10626 blocks are created, so this always terminates.
    for quad in combinations(points, 4):
        if quad in covered:
            continue
        extra = [x for x in points if x not in quad][:10]
        block = tuple(sorted(quad + tuple(extra)))
        blocks.append(list(block))
        covered.update(combinations(block, 4))
    if seed % 2:
        blocks.reverse()
    # EVOLVE-BLOCK-END
    return {"blocks": blocks}
