"""Fixed-seed greedy edge-swap search over all 50-vertex graphs."""

import os
import random
import time

from tasks.t100._graph import ALL_EDGES, M, N, triangle_count


def _edge_set(rng):
    return set(rng.sample(ALL_EDGES, M))


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T100-C01") != "T100-C01":
        raise ValueError("unsupported T100 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = int(os.environ.get("T100_SEARCH_STEPS", "5000"))
    if not 0 <= iterations <= 100000:
        raise ValueError("T100_SEARCH_STEPS must be between 0 and 100000")
    rng = random.Random(seed)
    deadline = None
    if os.environ.get("MATHBENCH_SEARCH_SECONDS") is not None:
        seconds = float(os.environ["MATHBENCH_SEARCH_SECONDS"])
        if not 0 < seconds <= 300:
            raise ValueError("MATHBENCH_SEARCH_SECONDS must be in (0, 300]")
        deadline = time.monotonic() + seconds

    current = _edge_set(rng)
    score = triangle_count(current)
    best = set(current)
    best_score = score
    completed = 0
    all_edge_set = set(ALL_EDGES)
    for step in range(iterations):
        if deadline is not None and time.monotonic() >= deadline:
            break
        removed = rng.choice(tuple(current))
        absent = all_edge_set.difference(current)
        added = rng.choice(tuple(absent))
        candidate = set(current)
        candidate.remove(removed)
        candidate.add(added)
        candidate_score = triangle_count(candidate)
        completed += 1
        if candidate_score < score or (step + 1) % 250 == 0:
            current, score = candidate, candidate_score
        if candidate_score < best_score:
            best, best_score = candidate, candidate_score

    return {
        "vertices": N,
        "edges": [list(edge) for edge in sorted(best)],
        "search": {
            "algorithm": "fixed-seed greedy edge swaps with a 250-step kick",
            "seed": seed,
            "iterations_requested": iterations,
            "iterations_completed": completed,
            "best_triangle_count": best_score,
            "comparison_data_read": False,
        },
    }
