"""Seeded order-crossover genetic search, independent of comparison data."""

import os
import random

from mathbench.search import search_steps
from tasks.t028.baseline import neh
from tasks.t028.check import load_processing_times, makespan


POPULATION_SIZE = 24
GENERATION_LIMIT = 120


def _order_crossover(first, second, rng):
    left, right = sorted(rng.sample(range(50), 2))
    child = [None] * 50
    child[left:right + 1] = first[left:right + 1]
    retained = set(child[left:right + 1])
    fill = [job for job in second[right + 1:] + second[:right + 1] if job not in retained]
    positions = list(range(right + 1, 50)) + list(range(0, left))
    for position, job in zip(positions, fill):
        child[position] = job
    return child


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T028-C01")
    if config_id != "T028-C01":
        raise ValueError("configuration id must be T028-C01")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    processing_times = load_processing_times()
    base = neh(processing_times)
    population = [base[:]]
    for _ in range(POPULATION_SIZE - 1):
        member = base[:]
        for _ in range(5):
            a, b = rng.sample(range(50), 2)
            member[a], member[b] = member[b], member[a]
        population.append(member)
    scores = [makespan(member, processing_times) for member in population]
    best_index = min(range(len(scores)), key=scores.__getitem__)
    best, best_score = population[best_index][:], scores[best_index]
    generations = 0
    steps = iter(search_steps(GENERATION_LIMIT))
    for _ in range(GENERATION_LIMIT):
        if next(steps, None) is None:
            break
        ranked = sorted(zip(scores, population), key=lambda item: item[0])
        parents = [member for _, member in ranked[:POPULATION_SIZE // 2]]
        next_population = [member[:] for member in parents[:2]]
        while len(next_population) < POPULATION_SIZE:
            child = _order_crossover(*rng.sample(parents, 2), rng)
            if rng.random() < 0.35:
                a, b = rng.sample(range(50), 2)
                child[a], child[b] = child[b], child[a]
            next_population.append(child)
        population = next_population
        scores = [makespan(member, processing_times) for member in population]
        candidate_index = min(range(len(scores)), key=scores.__getitem__)
        if scores[candidate_index] < best_score:
            best, best_score = population[candidate_index][:], scores[candidate_index]
        generations += 1
    return {
        "permutation": best,
        "claimed_objective": best_score,
        "search_metadata": {
            "algorithm": "NEH-seeded genetic search with order crossover and swap mutation",
            "config_id": config_id,
            "seed": seed,
            "generations": generations,
            "generation_limit": GENERATION_LIMIT,
            "population_size": POPULATION_SIZE,
            "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            "reference_data_read": False,
            "budget": {"generation_limit": GENERATION_LIMIT,
                       "population_size": POPULATION_SIZE,
                       "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS")},
        },
    }
