"""Seeded randomized greedy search for 3-AP-free subsets of [1, 212]."""

import os
import random

from mathbench.search import search_steps


CONFIG_ID = "T042-C01"
N = 212
RESTARTS = 48


def _triple_incidence():
    """Map each point to pairs that would complete a 3-term progression."""
    incidence = [[] for _ in range(N + 1)]
    for a in range(1, N + 1):
        for b in range(a + 1, N + 1):
            c = 2 * b - a
            if c <= N:
                incidence[a].append((b, c))
                incidence[b].append((a, c))
                incidence[c].append((a, b))
    return incidence


def _is_compatible(point, selected, incidence):
    return not any(left in selected and right in selected for left, right in incidence[point])


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if config_id != CONFIG_ID:
        raise ValueError("unsupported configuration id")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    incidence = _triple_incidence()
    best = [1]
    restarts = 0
    steps = iter(search_steps(RESTARTS))
    for _ in range(RESTARTS):
        if next(steps, None) is None:
            break
        order = list(range(2, N + 1))
        rng.shuffle(order)
        selected = {1}
        for point in order:
            if _is_compatible(point, selected, incidence):
                selected.add(point)
        restarts += 1
        if len(selected) > len(best):
            best = sorted(selected)
    return {
        "elements": best,
        "claimed_objective": len(best),
        "search_metadata": {
            "algorithm": "seeded randomized greedy insertion with exact AP-triple incidence checks",
            "configuration_id": config_id,
            "seed": seed,
            "restarts": restarts,
            "restart_limit": RESTARTS,
            "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            "comparison_data_read": False,
            "budget": {
                "restart_limit": RESTARTS,
                "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            },
        },
    }
