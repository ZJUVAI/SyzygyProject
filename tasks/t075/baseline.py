"""Fixed-seed random greedy edge additions; reads no human/reference witness."""
import os
import random

from mathbench.search import search_steps

try:
    from .greedy import all_triples, greedy_add
except ImportError:
    from greedy import all_triples, greedy_add

ITERATIONS = 5


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T075-C01") != "T075-C01":
        raise ValueError("unsupported T075 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    iterator = iter(search_steps(ITERATIONS))
    triples = all_triples()
    best = {"edges": []}
    best_count = 0
    trial_scores = []
    actual = 0
    for trial in range(ITERATIONS):
        if next(iterator, None) is None:
            break
        order = list(triples)
        rng.shuffle(order)
        candidate = greedy_add(order)
        count = len(candidate["edges"])
        actual += 1
        trial_scores.append(count)
        if count > best_count:
            best, best_count = candidate, count
    best["search_metadata"] = {
        "algorithm": "seeded random permutation greedy addition",
        "seed": seed,
        "iterations": actual,
        "iteration_limit": ITERATIONS,
        "trial_edge_counts": trial_scores,
        "best_edge_count": best_count,
        "comparison_data_read": False,
        "budget": {
            "mode": "fixed_iterations" if seconds is None else "wall_clock_cutoff",
            "requested_iterations": ITERATIONS,
            "actual_iterations": actual,
            "requested_wall_clock_seconds": seconds,
        },
    }
    return best
