"""Seeded population search using block mutations and hard-feasible selection."""

import os
import random
import time

from tasks.t055.check import PARAMETERS, validate
from tasks.t055.maxsat import HARD, SOFT, hard_sat_assignment, random_perturb, score_assignment


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T055-C01") != "T055-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "96"))))
    from mathbench.search import search_steps

    rng = random.Random(seed ^ 0x1112026)
    anchor = hard_sat_assignment(HARD)
    anchor_score = score_assignment(anchor, HARD, SOFT)["soft_satisfied_weight"]
    population = [(anchor, anchor_score) for _ in range(8)]
    best = anchor[:]
    best_score = anchor_score
    start = time.monotonic()
    tried = 0
    feasible = 0
    for generation in search_steps(generations):
        tried += 1
        parent, _ = rng.choice(population)
        candidate = random_perturb(rng, parent, rng.randint(1, 24))
        result = score_assignment(candidate, HARD, SOFT)
        if result["hard_satisfied"] == len(HARD):
            feasible += 1
            score = result["soft_satisfied_weight"]
            if score > best_score:
                best, best_score = candidate[:], score
            if score >= population[generation % len(population)][1] or rng.random() < 0.1:
                population[generation % len(population)] = (candidate, score)
    output = {"assignment": best}
    validate(output, {"parameters": PARAMETERS}, strict=True)
    output["search_metadata"] = {
        "algorithm": "seeded population block mutation with exact hard-feasibility filtering",
        "seed": seed,
        "generations_requested": generations,
        "generations_run": tried,
        "hard_feasible_mutants": feasible,
        "objective_recomputed": best_score,
        "generation_seconds": time.monotonic() - start,
        "budget": {"mode": "fixed iterations unless MATHBENCH_SEARCH_SECONDS is set", "runner_generation_seconds": 300},
    }
    return output


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
