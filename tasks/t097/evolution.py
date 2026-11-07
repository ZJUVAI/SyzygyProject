"""Deterministic seeded multi-start convex merge search."""
from tasks.t097.search_core import encode_solution, greedy_merge, load_boundary, seed_from_env, triangulate


def run_code():
    boundary = load_boundary()
    initial = triangulate(boundary)
    base_seed = seed_from_env()
    candidates = []
    trial_metadata = []
    for trial in range(2):
        polygons, metadata = greedy_merge(initial, base_seed + trial, max_sweeps=200)
        trial_metadata.append({"trial": trial, "piece_count": len(polygons), **metadata})
        candidates.append(polygons)
    best = min(candidates, key=len)
    return encode_solution(best, {
        "construction": "two seeded greedy convex-hull merge restarts from exact ear clipping",
        "base_seed": base_seed,
        "fixed_restarts": 2,
        "trials": trial_metadata,
        "comparison_data_read": False,
    })
