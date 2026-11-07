"""Seeded multi-start DSATUR greedy coloring; reads only the fixed graph."""

import heapq
import os
import random

from mathbench.search import search_steps
from tasks.t030.check import load_graph


ITERATION_LIMIT = 8


def dsatur_coloring(adjacency, rng):
    """Build one proper coloring using saturation-degree vertex selection."""
    n = len(adjacency)
    degrees = [len(neighbors) for neighbors in adjacency]
    saturation = [0] * n  # Bitset of colors already used by colored neighbors.
    colors = [-1] * n
    tie_break = [rng.random() for _ in range(n)]
    queue = [(0, -degrees[v], tie_break[v], v) for v in range(n)]
    heapq.heapify(queue)

    for color_step in range(n):
        while True:
            neg_sat_degree, neg_degree, tie, vertex = heapq.heappop(queue)
            if colors[vertex] != -1:
                continue
            if neg_sat_degree != -saturation[vertex].bit_count():
                continue
            if neg_degree != -degrees[vertex] or tie != tie_break[vertex]:
                continue
            break

        used = saturation[vertex]
        available = ~used
        color = (available & -available).bit_length() - 1
        colors[vertex] = color
        color_bit = 1 << color
        for neighbor in adjacency[vertex]:
            if colors[neighbor] == -1 and not (saturation[neighbor] & color_bit):
                saturation[neighbor] |= color_bit
                heapq.heappush(queue, (-saturation[neighbor].bit_count(),
                                       -degrees[neighbor], tie_break[neighbor], neighbor))
    return colors


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T030-C01")
    if config_id != "T030-C01":
        raise ValueError("unsupported configuration id")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    adjacency, _ = load_graph()
    best = None
    best_count = len(adjacency) + 1
    iterations = 0
    steps = iter(search_steps(ITERATION_LIMIT))
    for _ in range(ITERATION_LIMIT):
        if next(steps, None) is None:
            break
        candidate = dsatur_coloring(adjacency, rng)
        count = len(set(candidate))
        iterations += 1
        if count < best_count:
            best, best_count = candidate, count
    return {
        "colors": best,
        "claimed_objective": best_count,
        "search_metadata": {
            "algorithm": "multi-start DSATUR greedy coloring with seeded random tie breaks",
            "configuration_id": config_id,
            "seed": seed,
            "iterations": iterations,
            "iteration_limit": ITERATION_LIMIT,
            "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            "reference_data_read": False,
            "budget": {"iteration_limit": ITERATION_LIMIT,
                       "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS")},
        },
    }
