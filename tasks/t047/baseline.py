"""Seeded randomized greedy search for unrestricted integer difference bases."""

import os
import random

from mathbench.search import search_steps


CONFIG_ID = "T047-C01"
N = 6166
RESTARTS = 6
RANDOM_CANDIDATES_PER_STEP = 32
MAX_ADDITIONS_PER_RESTART = 320


def _new_differences(point, basis):
    return {abs(point - old) for old in basis if point != old and abs(point - old) <= N}


def _greedy_restart(rng):
    basis = {0}
    covered = set()
    additions = 0
    while len(covered) < N and additions < MAX_ADDITIONS_PER_RESTART:
        missing = next(distance for distance in range(1, N + 1) if distance not in covered)
        anchor = max(basis)
        candidates = {anchor + missing}
        upper = max(N + anchor + 1, 2 * N)
        while len(candidates) < RANDOM_CANDIDATES_PER_STEP + 1:
            value = rng.randrange(0, upper + 1)
            if value not in basis:
                candidates.add(value)
        best_point = None
        best_gain = -1
        best_differences = None
        for point in candidates:
            differences = _new_differences(point, basis) - covered
            gain = len(differences)
            if gain > best_gain or (gain == best_gain and rng.random() < 0.5):
                best_point, best_gain, best_differences = point, gain, differences
        basis.add(best_point)
        covered.update(best_differences)
        additions += 1
    if len(covered) == N:
        return sorted(basis), additions
    return None, additions


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if config_id != CONFIG_ID:
        raise ValueError("unsupported configuration id")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    best = list(range(N + 1))
    best_size = len(best)
    complete_restarts = 0
    total_additions = 0
    for _ in search_steps(RESTARTS):
        candidate, additions = _greedy_restart(rng)
        total_additions += additions
        if candidate is not None:
            complete_restarts += 1
            if len(candidate) < best_size:
                best, best_size = candidate, len(candidate)
    return {
        "basis": best,
        "claimed_objective": best_size,
        "search_metadata": {
            "algorithm": "seeded randomized greedy set cover over integer differences; each step samples candidate marks and includes an anchor-plus-smallest-missing-distance point to guarantee progress",
            "configuration_id": config_id,
            "seed": seed,
            "restart_limit": RESTARTS,
            "random_candidates_per_step": RANDOM_CANDIDATES_PER_STEP,
            "max_additions_per_restart": MAX_ADDITIONS_PER_RESTART,
            "completed_restarts": complete_restarts,
            "total_additions": total_additions,
            "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            "comparison_data_read": False,
            "fallback": "all marks 0..6166 if no restart completed",
        },
    }
