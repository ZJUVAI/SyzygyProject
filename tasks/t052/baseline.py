"""Fixed-seed greedy packing of random permutations at distance at least 9."""

import os
import random
import time


def _distance(left, right):
    return sum(a != b for a, b in zip(left, right))


def _greedy(rng, candidates):
    code = []
    for _ in range(candidates):
        word = list(range(12))
        rng.shuffle(word)
        if all(_distance(word, old) >= 9 for old in code):
            code.append(word)
    return code


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T052-C01") != "T052-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    restarts = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "24"))))
    candidates = max(1, min(10000, int(os.environ.get("T052_CANDIDATES_PER_RESTART", "500"))))
    from mathbench.search import search_steps

    rng = random.Random(seed)
    best = []
    started = time.monotonic()
    run_count = 0
    for _ in search_steps(restarts):
        run_count += 1
        code = _greedy(rng, candidates)
        if len(code) > len(best):
            best = code
    if not best:
        best = [[(symbol + shift) % 12 for symbol in range(12)] for shift in range(12)]
    return {
        "codewords": best,
        "search_metadata": {
            "algorithm": "seeded random permutation greedy packing with independent restarts",
            "seed": seed,
            "iterations_requested": restarts,
            "iterations_run": run_count,
            "candidates_per_restart": candidates,
            "objective_recomputed": len(best),
            "generation_seconds": time.monotonic() - started,
            "budget": {"mode": "fixed iterations unless MATHBENCH_SEARCH_SECONDS is set", "runner_generation_seconds": 300},
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
