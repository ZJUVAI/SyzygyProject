"""Seeded evolutionary search over integer point placements."""

import os
import random
import time
from fractions import Fraction

from mathbench.search import search_steps
from tasks.t074.check import PARAMETERS, validate


CONFIG = {"id": "T074-C01", "parameters": PARAMETERS}


def _score(points):
    return Fraction(validate({"points": points}, CONFIG)["objective"])


def _mutate(points, rng, coordinate_limit):
    child = [point[:] for point in points]
    index = rng.randrange(len(child))
    child[index] = [rng.randint(-coordinate_limit, coordinate_limit),
                    rng.randint(-coordinate_limit, coordinate_limit)]
    return child


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T074-C01") != "T074-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(300, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "60"))))
    population_size = max(2, min(12, int(os.environ.get("MATHBENCH_POPULATION", "6"))))
    coordinate_limit = max(12, min(1000, int(os.environ.get("MATHBENCH_SEARCH_COORDINATE_LIMIT", "40"))))
    rng = random.Random(seed ^ 0x013E701)
    start = time.monotonic()
    initial = [[i, i * i] for i in range(12)]
    population = [( _score(initial), initial)]
    while len(population) < population_size:
        candidate = _mutate(initial, rng, coordinate_limit)
        try:
            population.append((_score(candidate), candidate))
        except ValueError:
            continue

    completed = invalid = 0
    for _ in search_steps(generations):
        parent_score, parent = rng.choice(population[:max(1, population_size // 2)])
        candidate = _mutate(parent, rng, coordinate_limit)
        try:
            candidate_score = _score(candidate)
        except ValueError:
            invalid += 1
            completed += 1
            continue
        population.append((candidate_score, candidate))
        population.sort(key=lambda item: (-item[0], item[1]))
        population = population[:population_size]
        completed += 1
    best_score, best = population[0]
    return {
        "points": best,
        "search_metadata": {
            "algorithm": "elitist evolutionary search with one-point integer-coordinate mutation",
            "seed": seed,
            "generations_requested": generations,
            "generations_run": completed,
            "population_size": population_size,
            "invalid_trials": invalid,
            "search_only_coordinate_proposal_limit": coordinate_limit,
            "best_objective": str(best_score),
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed generations unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
