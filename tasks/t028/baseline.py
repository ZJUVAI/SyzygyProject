"""NEH construction followed by seeded swap/insertion local search."""

import os
import random

from mathbench.search import search_steps
from tasks.t028.check import load_processing_times, makespan


ITERATION_LIMIT = 2_000


def neh(processing_times):
    jobs = range(1, 51)
    order = sorted(jobs, key=lambda job: sum(row[job - 1] for row in processing_times), reverse=True)
    sequence = []
    for job in order:
        candidates = [sequence[:index] + [job] + sequence[index:]
                     for index in range(len(sequence) + 1)]
        sequence = min(candidates, key=lambda candidate: makespan(candidate, processing_times))
    return sequence


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T028-C01")
    if config_id != "T028-C01":
        raise ValueError("configuration id must be T028-C01")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    processing_times = load_processing_times()
    current = neh(processing_times)
    current_score = makespan(current, processing_times)
    best = current[:]
    best_score = current_score
    iterations = 0
    steps = iter(search_steps(ITERATION_LIMIT))
    for _ in range(ITERATION_LIMIT):
        if next(steps, None) is None:
            break
        proposal = current[:]
        left, right = sorted(rng.sample(range(50), 2))
        if rng.random() < 0.65:
            proposal[left], proposal[right] = proposal[right], proposal[left]
        else:
            job = proposal.pop(right)
            proposal.insert(left, job)
        score = makespan(proposal, processing_times)
        iterations += 1
        if score < current_score or rng.random() < 0.025:
            current, current_score = proposal, score
        if score < best_score:
            best, best_score = proposal, score
    return {
        "permutation": best,
        "claimed_objective": best_score,
        "search_metadata": {
            "algorithm": "NEH insertion construction with randomized swap/insertion local search",
            "config_id": config_id,
            "seed": seed,
            "iterations": iterations,
            "iteration_limit": ITERATION_LIMIT,
            "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            "reference_data_read": False,
            "budget": {"iteration_limit": ITERATION_LIMIT,
                       "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS")},
        },
    }
