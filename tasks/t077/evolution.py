"""Seeded evolutionary search over finite integer sets."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t077.search_utils import heuristic_score, mutate


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T077-C01") != "T077-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(300, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "60"))))
    population_size = max(2, min(12, int(os.environ.get("MATHBENCH_POPULATION", "6"))))
    rng = random.Random(seed ^ 0x058E701)
    start = time.monotonic()

    seed_set = [0, 1, 3]
    population = [(heuristic_score(seed_set), seed_set)]
    while len(population) < population_size:
        candidate = mutate(seed_set, rng)
        population.append((heuristic_score(candidate), candidate))
    completed = 0
    for _ in search_steps(generations):
        parent = rng.choice(population[:max(1, population_size // 2)])[1]
        candidate = mutate(parent, rng)
        population.append((heuristic_score(candidate), candidate))
        population.sort(key=lambda item: (-item[0], item[1]))
        population = population[:population_size]
        completed += 1
    best_score, best = population[0]
    return {
        "set": best,
        "search_metadata": {
            "algorithm": "elitist evolutionary search with integer-set add/remove/replacement mutation",
            "seed": seed,
            "generations_requested": generations,
            "generations_run": completed,
            "population_size": population_size,
            "heuristic_score": best_score,
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed generations unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
