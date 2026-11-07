"""Seeded sequential greedy search; no comparison witness is read."""

import os
import random

from mathbench.search import search_steps


CONFIG_ID = "T034-C01"
PLACEMENT_BUDGET = 20_000


def _allowed(colors, number, color):
    # Check exactly the progressions whose final term is the new number.
    for step in range(1, (number - 1) // 6 + 1):
        start = number - 1 - 6 * step
        if all(colors[start + j * step] == color for j in range(6)):
            return False
    return True


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if config_id != CONFIG_ID:
        raise ValueError("unsupported configuration id")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    colors = [0] * 6
    best = colors.copy()
    placements = 0
    restarts = 0
    for _ in search_steps(PLACEMENT_BUDGET):
        number = len(colors) + 1
        choices = [c for c in (0, 1) if _allowed(colors, number, c)]
        if not choices:
            if len(colors) > len(best):
                best = colors.copy()
            colors = [0] * 6
            restarts += 1
            continue
        colors.append(rng.choice(choices))
        placements += 1
    if len(colors) > len(best):
        best = colors
    return {
        "n": len(best),
        "colors": best,
        "claimed_objective": len(best),
        "search_metadata": {
            "algorithm": "seeded randomized sequential greedy extension with restart after dead end",
            "configuration_id": config_id,
            "seed": seed,
            "placements": placements,
            "placement_budget": PLACEMENT_BUDGET,
            "restarts": restarts,
            "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            "reference_data_read": False,
        },
    }
