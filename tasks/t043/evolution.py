"""Seeded local search over greedy packings; no comparison asset is read."""

import os
import random
import time


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T043-C01") != "T043-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    from mathbench.search import search_steps
    from tasks.t043.baseline import _basis, _spaces
    start = time.monotonic()
    requested = max(1, min(100, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "12"))))
    rng = random.Random(seed ^ 0x69A2)
    spaces, supports = _spaces()
    best = []
    best_pass = None
    attempts = 0
    for pass_index in search_steps(requested):
        order = list(range(len(spaces)))
        rng.shuffle(order)
        used_lines = 0
        chosen = []
        for index in order:
            line_mask = sum(1 << line_id for line_id in supports[index])
            if not (used_lines & line_mask):
                chosen.append(index)
                used_lines |= line_mask
        attempts += 1
        if len(chosen) > len(best):
            best = chosen
            best_pass = pass_index
    return {
        "codewords": [_basis(spaces[index]) for index in best],
        "search_metadata": {
            "algorithm": "seeded randomized greedy restarts over exact subspace enumeration",
            "seed": seed,
            "iterations_requested": requested,
            "iterations_run": attempts,
            "best_pass": best_pass,
            "generation_seconds": time.monotonic() - start,
            "budget": {"mode": "fixed_iterations unless MATHBENCH_SEARCH_SECONDS is set",
                       "runner_generation_limit_seconds": 300},
        },
    }


if __name__ == "__main__":
    print(run_code())
