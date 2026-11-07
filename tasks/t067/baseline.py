"""Seeded greedy packing search over all weight-five 17-bit words."""

from itertools import combinations
import os
import random
import time

from mathbench.search import search_steps


def _candidates():
    words = []
    for positions in combinations(range(17), 5):
        word = 0
        for position in positions:
            word |= 1 << position
        words.append(word)
    return words


def _greedy(order):
    selected = []
    for word in order:
        if all((word ^ old).bit_count() >= 4 for old in selected):
            selected.append(word)
    return selected


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T067-C01") != "T067-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    restarts = max(1, min(20, int(os.environ.get("MATHBENCH_RESTARTS", "8"))))
    candidates = _candidates()
    rng = random.Random(seed ^ 0x068B)
    best = [candidates[0]]
    start = time.monotonic()
    iterations = 0
    for _ in search_steps(restarts):
        order = list(candidates)
        rng.shuffle(order)
        candidate = _greedy(order)
        if len(candidate) > len(best):
            best = candidate
        iterations += 1
    return {
        "codewords": [format(word, "017b") for word in best],
        "search_metadata": {
            "algorithm": "random-order greedy independent-set packing on the fixed weight-five conflict graph",
            "seed": seed,
            "candidate_words": len(candidates),
            "restarts_requested": restarts,
            "restarts_run": iterations,
            "best_size": len(best),
            "generation_seconds": time.monotonic() - start,
            "budget": {
                "mode": "fixed restart count unless MATHBENCH_SEARCH_SECONDS is set",
                "runner_generation_limit_seconds": 300,
            },
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
