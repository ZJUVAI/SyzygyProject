"""Seeded evolutionary search over guillotine dissection plans."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t070.construction import coprime_guillotine_plan


def _random_plan(rng, depth):
    return [(rng.randrange(10_000), rng.randrange(2), rng.randrange(1000))
            for _ in range(depth)]


def _mutate(plan, rng):
    child = list(plan)
    if not child or rng.random() < 0.15:
        child.append((rng.randrange(10_000), rng.randrange(2), rng.randrange(1000)))
    if len(child) > 16:
        child.pop(rng.randrange(len(child)))
    index = rng.randrange(len(child))
    leaf, axis, cut = child[index]
    change = rng.randrange(3)
    if change == 0:
        leaf = rng.randrange(10_000)
    elif change == 1:
        axis = 1 - axis
    else:
        cut = rng.randrange(1000)
    child[index] = (leaf, axis, cut)
    return child


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T070-C01") != "T070-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(300, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "60"))))
    population_size = max(2, min(12, int(os.environ.get("MATHBENCH_POPULATION", "6"))))
    rng = random.Random(seed ^ 0x033E701)
    start = time.monotonic()
    population = []
    for _ in range(population_size):
        plan = _random_plan(rng, rng.randint(3, 10))
        candidate = coprime_guillotine_plan(plan)
        population.append((len(candidate["squares"]), plan, candidate))
    best = min(population, key=lambda item: item[0])
    completed = 0
    for _ in search_steps(generations):
        parent = min(population, key=lambda item: item[0])
        plan = _mutate(parent[1], rng)
        candidate = coprime_guillotine_plan(plan)
        individual = (len(candidate["squares"]), plan, candidate)
        if individual[0] < best[0]:
            best = individual
        population.append(individual)
        population.sort(key=lambda item: item[0])
        population = population[:population_size]
        completed += 1
    solution = {"squares": best[2]["squares"]}
    solution["search_metadata"] = {
        "algorithm": "elitist evolutionary search over integer guillotine split plans; leaves use Euclidean square tilings and one square is refined to force gcd 1 when needed",
        "seed": seed,
        "generations_requested": generations,
        "generations_run": completed,
        "population_size": population_size,
        "winning_plan": best[1],
        "best_size": len(solution["squares"]),
        "generation_seconds": time.monotonic() - start,
        "budget": {
            "mode": "fixed generation count unless MATHBENCH_SEARCH_SECONDS is set",
            "runner_generation_limit_seconds": 300,
        },
    }
    return solution


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
