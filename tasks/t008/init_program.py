"""Deterministic finite covering constructions selected by config id."""
import os
from itertools import combinations


PARAMS = {
    "T008-C01": (24, 14, 4),
    "T008-C02": (20, 10, 4),
}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T008-C01")
    if config_id not in PARAMS:
        raise ValueError("unsupported configuration")
    if config_id != "T008-C01":
        v, k, t = PARAMS[config_id]
        points = tuple(range(v))
        blocks, covered = [], set()
        for subset in combinations(points, t):
            if subset in covered:
                continue
            extra = [x for x in points if x not in subset][:k-t]
            block = tuple(sorted(subset + tuple(extra)))
            blocks.append(list(block))
            covered.update(combinations(block, t))
        if int(os.environ.get("MATHBENCH_SEED", "0")) % 2:
            blocks.reverse()
        return {"blocks": blocks}
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
