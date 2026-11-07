"""Finite scan of uniform guillotine grids with one coprime refinement."""

import os
import time

from mathbench.search import search_steps
from tasks.t070.construction import OUTER_SIDE


def _candidate(blocks_per_side):
    side = OUTER_SIDE // blocks_per_side
    squares = [
        [x * side, y * side, side]
        for y in range(blocks_per_side)
        for x in range(blocks_per_side)
    ]
    # Replace one block by a (side-1) square and two unit-width strips.
    squares.pop(0)
    squares.append([0, 0, side - 1])
    squares.extend([[x, side - 1, 1] for x in range(side)])
    squares.extend([[side - 1, y, 1] for y in range(side - 1)])
    return {"squares": squares}


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T070-C01") != "T070-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    del seed  # This exhaustive finite scan has no random choices.
    divisors = [q for q in range(1, OUTER_SIDE) if OUTER_SIDE % q == 0 and OUTER_SIDE // q >= 2]
    start = time.monotonic()
    best = _candidate(divisors[0])
    checked = 0
    for index in search_steps(len(divisors)):
        q = divisors[index]
        candidate = _candidate(q)
        if len(candidate["squares"]) < len(best["squares"]):
            best = candidate
        checked += 1
    best["search_metadata"] = {
        "algorithm": "exhaustive scan of equal-block guillotine grids; replace one block by a coprime Euclidean strip dissection",
        "seed": 0,
        "candidate_block_counts": divisors,
        "candidates_checked": checked,
        "best_size": len(best["squares"]),
        "generation_seconds": time.monotonic() - start,
        "budget": {
            "mode": "fixed exhaustive candidate count unless MATHBENCH_SEARCH_SECONDS is set",
            "runner_generation_limit_seconds": 300,
        },
    }
    return best


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
