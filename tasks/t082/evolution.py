"""Elitist search over valid queen placements, independent of comparison data."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t082.construction import greedy_layout, mutate_layout


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T082-C01") != "T082-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(200, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "30"))))
    population_size = max(2, min(10, int(os.environ.get("MATHBENCH_POPULATION", "4"))))
    rng = random.Random(seed ^ 0x119E701)
    start = time.monotonic()
    population = [greedy_layout(rng, max_army=45) for _ in range(population_size)]
    completed = 0
    for _ in search_steps(generations):
        population.sort(key=lambda layout: (-len(layout["white"]), layout["white"], layout["black"]))
        parent = rng.choice(population[:max(1, population_size // 2)])
        child = mutate_layout(parent, rng)
        population.append(child)
        population.sort(key=lambda layout: (-len(layout["white"]), layout["white"], layout["black"]))
        population = population[:population_size]
        completed += 1
    best = max(population, key=lambda layout: len(layout["white"]))
    return {
        **best,
        "search_metadata": {
            "algorithm": "elitist evolutionary search over feasible layouts with pair removal and randomized valid pair extension",
            "seed": seed,
            "generations_requested": generations,
            "generations_run": completed,
            "population_size": population_size,
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed generations unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
