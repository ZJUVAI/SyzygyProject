"""Seeded multi-start greedy packing with shuffled candidate batches."""

import os
import random
import time

from tasks.t052.baseline import _greedy


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T052-C01") != "T052-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "32"))))
    candidates = max(1, min(10000, int(os.environ.get("T052_CANDIDATES_PER_GENERATION", "750"))))
    from mathbench.search import search_steps

    rng = random.Random(seed ^ 0x7109)
    best = [[(symbol + shift) % 12 for symbol in range(12)] for shift in range(12)]
    started = time.monotonic()
    count = 0
    for _ in search_steps(generations):
        count += 1
        candidate = _greedy(rng, candidates)
        if len(candidate) > len(best):
            best = candidate
    return {
        "codewords": best,
        "search_metadata": {
            "algorithm": "seeded multi-start greedy packing; best valid batch retained",
            "seed": seed,
            "iterations_requested": generations,
            "iterations_run": count,
            "candidates_per_generation": candidates,
            "objective_recomputed": len(best),
            "generation_seconds": time.monotonic() - started,
            "budget": {"mode": "fixed iterations unless MATHBENCH_SEARCH_SECONDS is set", "runner_generation_seconds": 300},
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
