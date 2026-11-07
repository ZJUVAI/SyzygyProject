"""Evolutionary order search for the weight-five conflict graph."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t067.baseline import _candidates, _greedy


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T067-C01") != "T067-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(300, int(os.environ.get("MATHBENCH_EVOLUTION_ITERATIONS", "60"))))
    population_size = max(2, min(12, int(os.environ.get("MATHBENCH_POPULATION", "6"))))
    rng = random.Random(seed ^ 0x68E701)
    words = _candidates()
    start = time.monotonic()
    population = []
    for _ in range(population_size):
        order = list(words)
        rng.shuffle(order)
        population.append((len(_greedy(order)), order))
    best_score, best_order = max(population, key=lambda item: item[0])
    completed = 0
    for _ in search_steps(generations):
        parent_score, parent = max(population, key=lambda item: item[0])
        child = list(parent)
        # A bounded block shuffle mutates candidate priority without using any
        # human or reference construction.
        left = rng.randrange(len(child))
        right = min(len(child), left + rng.randint(8, 128))
        block = child[left:right]
        rng.shuffle(block)
        child[left:right] = block
        child_score = len(_greedy(child))
        if child_score > best_score:
            best_score, best_order = child_score, child
        population.append((child_score, child))
        population.sort(key=lambda item: item[0], reverse=True)
        population = population[:population_size]
        completed += 1
    selected = _greedy(best_order)
    return {
        "codewords": [format(word, "017b") for word in selected],
        "search_metadata": {
            "algorithm": "elitist evolutionary search over greedy candidate orderings with block-shuffle mutation",
            "seed": seed,
            "generations_requested": generations,
            "generations_run": completed,
            "population_size": population_size,
            "best_size": len(selected),
            "generation_seconds": time.monotonic() - start,
            "budget": {
                "mode": "fixed generation count unless MATHBENCH_SEARCH_SECONDS is set",
                "runner_generation_limit_seconds": 300,
            },
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
