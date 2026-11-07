"""Bounded simulated-annealing edge swaps for T100."""

import os
import random
import time

from tasks.t100._graph import ALL_EDGES, M, N, triangle_count


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T100-C01") != "T100-C01":
        raise ValueError("unsupported T100 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = int(os.environ.get("T100_EVOLVE_STEPS", "10000"))
    if not 0 <= iterations <= 100000:
        raise ValueError("T100_EVOLVE_STEPS must be between 0 and 100000")
    rng = random.Random(seed ^ 0xA043)
    deadline = None
    if os.environ.get("MATHBENCH_SEARCH_SECONDS") is not None:
        seconds = float(os.environ["MATHBENCH_SEARCH_SECONDS"])
        if not 0 < seconds <= 300:
            raise ValueError("MATHBENCH_SEARCH_SECONDS must be in (0, 300]")
        deadline = time.monotonic() + seconds

    current = set(rng.sample(ALL_EDGES, M))
    score = triangle_count(current)
    best = set(current)
    best_score = score
    present = set(current)
    completed = 0
    for step in range(iterations):
        if deadline is not None and time.monotonic() >= deadline:
            break
        removed = rng.choice(tuple(present))
        absent = [edge for edge in ALL_EDGES if edge not in present]
        added = rng.choice(absent)
        candidate = set(present)
        candidate.remove(removed)
        candidate.add(added)
        candidate_score = triangle_count(candidate)
        temp = 150.0 * (0.02 ** (step / max(1, iterations - 1)))
        delta = candidate_score - score
        if delta <= 0 or rng.random() < pow(2.718281828459045, -delta / max(temp, 1e-9)):
            present, score = candidate, candidate_score
        completed += 1
        if candidate_score < best_score:
            best, best_score = candidate, candidate_score

    return {
        "vertices": N,
        "edges": [list(edge) for edge in sorted(best)],
        "search": {
            "algorithm": "simulated annealing with exact triangle-count feedback",
            "seed": seed,
            "iterations_requested": iterations,
            "iterations_completed": completed,
            "best_triangle_count": best_score,
            "comparison_data_read": False,
        },
    }
