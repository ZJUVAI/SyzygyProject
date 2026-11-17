"""Seeded greedy vertex-extension search; it does not read reference assets."""
import os
import random

from mathbench.search import search_steps


def _has_k_clique(neighbors, size=5):
    def visit(candidates, depth):
        if depth == size:
            return True
        if candidates.bit_count() < size - depth:
            return False
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            v = bit.bit_length() - 1
            if visit(candidates & neighbors[v], depth + 1):
                return True
        return False
    return visit((1 << len(neighbors)) - 1, 0)


def _valid(neighbors):
    n = len(neighbors)
    if _has_k_clique(neighbors):
        return False
    comp = [(((1 << n) - 1) ^ (1 << v) ^ neighbors[v]) for v in range(n)]
    return not _has_k_clique(comp)


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    best = [(1 << ((v - 1) % 5)) | (1 << ((v + 1) % 5)) for v in range(5)]
    # Fixed iteration default; the shared runner still applies hard time limits.
    attempts = search_steps(40)
    attempted = 0
    for _ in attempts:
        n = len(best)
        if n >= 45:
            break
        attempted += 1
        row = 0
        for v in range(n):
            if rng.getrandbits(1):
                row |= 1 << v
        candidate = [x | ((row >> i & 1) << n) for i, x in enumerate(best)]
        candidate.append(row)
        if _valid(candidate):
            best = candidate
    time_budget = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    return {
        "adjacency": [[w for w in range(len(best)) if row >> w & 1]
                      for row in best],
        "search_metadata": {
            "algorithm": "seeded random one-vertex extension with exact K5 exclusion checks",
            "seed": seed,
            "iterations_attempted": attempted,
            "iteration_budget": 40,
            "time_budget_seconds": float(time_budget) if time_budget is not None else None,
            "vertex_cap": 45,
        },
    }
