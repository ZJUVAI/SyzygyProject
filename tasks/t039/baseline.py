"""Seeded greedy search for short difference triangle sets.

The search starts from a simple construction, then uses fixed-count randomized
greedy restarts under decreasing scope caps. It does not read comparison data.
"""
import os
import random

from mathbench.search import search_steps
from tasks.t039.init_program import run_code as initial_run


def _valid(rows):
    seen = set()
    for row in rows:
        ordered = sorted(row)
        if len(ordered) != 6 or len(set(ordered)) != 6:
            return False
        for i, left in enumerate(ordered):
            for right in ordered[i + 1:]:
                difference = right - left
                if difference <= 0 or difference in seen:
                    return False
                seen.add(difference)
    return len(rows) == 7


def _random_greedy(cap, rng):
    order = list(range(7))
    rng.shuffle(order)
    rows = [None] * 7
    used = set()
    for row_index in order:
        row = [0]
        while len(row) < 6:
            candidates = []
            # Scan marks in increasing order, then choose among a small random
            # prefix of legal marks. This keeps the construction compact while
            # varying the local greedy choice.
            choice_width = rng.randint(1, 4)
            for mark in range(row[-1] + 1, cap + 1):
                new = [mark - old for old in row]
                if len(set(new)) == len(new) and not used.intersection(new):
                    candidates.append((mark, new))
                    if len(candidates) >= choice_width:
                        break
            if not candidates:
                return None
            mark, new = rng.choice(candidates)
            row.append(mark)
            used.update(new)
        rows[row_index] = row
    return rows


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T039-C01")
    if config_id != "T039-C01":
        raise ValueError(f"unknown T039 configuration: {config_id}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    best = initial_run()["rows"]
    best_value = max(max(row) - min(row) for row in best)
    attempts = 0
    for step in search_steps(100):
        attempts = step + 1
        cap = max(150, 260 - step)
        candidate = _random_greedy(cap, rng)
        if candidate is None or not _valid(candidate):
            continue
        value = max(max(row) - min(row) for row in candidate)
        if value < best_value:
            best, best_value = candidate, value
    if not _valid(best):
        raise RuntimeError("search returned an invalid construction")
    return {
        "rows": best,
        "search_method": "seeded randomized greedy row completion with decreasing scope caps",
        "search_seed": seed,
        "search_iterations": attempts,
        "initial_objective": max(max(row) - min(row) for row in initial_run()["rows"]),
    }
