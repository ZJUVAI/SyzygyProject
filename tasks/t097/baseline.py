"""Seeded traditional greedy merge search from exact ear clipping."""
from tasks.t097.search_core import encode_solution, greedy_merge, load_boundary, seed_from_env, triangulate


def run_code():
    boundary = load_boundary()
    seed = triangulate(boundary)
    merged, metadata = greedy_merge(seed, seed_from_env(), max_sweeps=200)
    return encode_solution(merged, metadata)
