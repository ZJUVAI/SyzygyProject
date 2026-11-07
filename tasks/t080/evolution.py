"""Seeded elitist evolutionary search over U containing zero."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t080.search_utils import heuristic_score, mutate


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T080-C01") != "T080-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(300, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "60"))))
    population_size = max(2, min(12, int(os.environ.get("MATHBENCH_POPULATION", "6"))))
    rng = random.Random(seed ^ 0x059E701)
    start = time.monotonic()
    initial = [0, 1, 4]
    population = [(heuristic_score(initial), initial)]
    attempts = 0
    while len(population) < population_size and attempts < population_size * 100:
        candidate = mutate(initial, rng)
        score = heuristic_score(candidate)
        if score is not None:
            population.append((score, candidate))
        attempts += 1
    while len(population) < population_size:
        population.append(population[0])
    completed = invalid = 0
    for _ in search_steps(generations):
        parent = rng.choice(population[:max(1, population_size // 2)])[1]
        candidate = mutate(parent, rng)
        score = heuristic_score(candidate)
        if score is None:
            invalid += 1
            completed += 1
            continue
        population.append((score, candidate))
        population.sort(key=lambda item: (-item[0], item[1]))
        population = population[:population_size]
        completed += 1
    best_score, best = population[0]
    return {
        "set": best,
        "search_metadata": {
            "algorithm": "elitist evolutionary search with integer-set addition, removal, and replacement mutations",
            "seed": seed,
            "generations_requested": generations,
            "generations_run": completed,
            "population_size": population_size,
            "invalid_strict_bound_trials": invalid,
            "heuristic_score": best_score,
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed generations unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
