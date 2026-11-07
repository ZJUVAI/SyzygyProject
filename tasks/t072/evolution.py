"""Seeded evolutionary search over arbitrary 32-element positive-integer sets."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t072.search_utils import mutate, score, search_integer_limit


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T072-C01") != "T072-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(300, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "60"))))
    population_size = max(2, min(12, int(os.environ.get("MATHBENCH_POPULATION", "6"))))
    limit = search_integer_limit()
    rng = random.Random(seed ^ 0x055E701)
    start = time.monotonic()

    population = []
    seed_set = list(range(1, 33))
    population.append((score(seed_set), seed_set))
    while len(population) < population_size:
        candidate = mutate(seed_set, rng, limit)
        population.append((score(candidate), candidate))

    completed = 0
    for _ in search_steps(generations):
        parent_score, parent = rng.choice(population[:max(1, population_size // 2)])
        child = mutate(parent, rng, limit)
        population.append((score(child), child))
        population.sort(key=lambda item: (item[0], item[1]))
        population = population[:population_size]
        completed += 1
    best_score, best = population[0]
    return {
        "elements": best,
        "search_metadata": {
            "algorithm": "elitist evolutionary search with one/two-element replacement mutation",
            "seed": seed,
            "generations_requested": generations,
            "generations_run": completed,
            "population_size": population_size,
            "search_only_integer_proposal_limit": limit,
            "best_objective": best_score,
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed generations unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
