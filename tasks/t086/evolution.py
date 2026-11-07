"""Elitist mutation search over positive diagonal PSD matrices."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t086.construction import initial_diagonals, matrices_from_diagonals
from tasks.t086.search_utils import diagonal_ratio, mutate_diagonals


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T086-C01") != "T086-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(300, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "50"))))
    population_size = max(2, min(12, int(os.environ.get("MATHBENCH_POPULATION", "6"))))
    rng = random.Random(seed ^ 0x094E701)
    identity = initial_diagonals()
    population = [(diagonal_ratio(identity), identity)]
    while len(population) < population_size:
        candidate = mutate_diagonals(identity, rng)
        population.append((diagonal_ratio(candidate), candidate))
    start = time.monotonic()
    completed = 0
    for _ in search_steps(generations):
        population.sort(key=lambda item: (item[0], item[1]))
        parent = rng.choice(population[:max(1, population_size // 2)])[1]
        child = mutate_diagonals(parent, rng)
        population.append((diagonal_ratio(child), child))
        population.sort(key=lambda item: (item[0], item[1]))
        population = population[:population_size]
        completed += 1
    score, best = population[0]
    return {
        **matrices_from_diagonals(best),
        "search_metadata": {
            "algorithm": "elitist evolution with positive-diagonal coordinate mutations",
            "seed": seed,
            "generations_requested": generations,
            "generations_run": completed,
            "population_size": population_size,
            "heuristic_ratio": score,
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed generations unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
