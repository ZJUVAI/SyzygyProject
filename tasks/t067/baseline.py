"""Seeded randomized greedy construction; it never reads reference data."""

import os
import random

from mathbench.search import search_steps


COLOR_LIMIT = 6
PLACEMENT_BUDGET = 50_000


def _can_extend(colors, number, color):
    # For x+y=number, x<=y enumerates each unordered pair once, including x=y.
    for x in range(1, number // 2 + 1):
        y = number - x
        if colors[x - 1] == color and colors[y - 1] == color:
            return False
    return True


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    requested_seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    best = [0, 1, 1, 0]
    placements = 0
    restarts = 1
    colors = []
    for _ in search_steps(PLACEMENT_BUDGET):
        number = len(colors) + 1
        available = [color for color in range(COLOR_LIMIT) if _can_extend(colors, number, color)]
        if not available:
            if len(colors) > len(best):
                best = colors
            colors = []
            restarts += 1
            number = 1
            available = list(range(COLOR_LIMIT))
        colors.append(rng.choice(available))
        placements += 1
    if len(colors) > len(best):
        best = colors
    return {
        "n": len(best),
        "colors": best,
        "search_metadata": {
            "algorithm": "seeded randomized sequential greedy coloring with restarts",
            "seed": seed,
            "placements": placements,
            "placement_budget": PLACEMENT_BUDGET,
            "restarts": restarts,
            "wall_clock_cutoff_seconds": requested_seconds,
            "reference_data_read": False,
        },
    }
