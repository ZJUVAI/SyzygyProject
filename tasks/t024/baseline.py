"""Seeded edge-addition search; it does not read witness assets."""
import os, random
from mathbench.search import search_steps

def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "38"))
    rng = random.Random(seed)
    n = 41
    edges = set()
    # Start at a star, a simple C4-free graph.
    edges.update((0, v) for v in range(1, n))
    attempted = accepted = 0
    for _ in search_steps(3000):
        u, v = sorted(rng.sample(range(n), 2))
        attempted += 1
        if (u, v) in edges:
            continue
        adj = [set() for _ in range(n)]
        for a, b in edges:
            adj[a].add(b); adj[b].add(a)
        # Adding uv creates a C4 iff an existing length-3 path joins u to v.
        if any(y in adj[x] for x in adj[u] for y in adj[v] if x != y):
            continue
        edges.add((u, v)); accepted += 1
    adj = [[] for _ in range(n)]
    for u, v in sorted(edges):
        adj[u].append(v); adj[v].append(u)
    return {"adjacency": adj, "search_metadata": {
        "algorithm": "seeded random edge addition with exact C4 checker",
        "seed": seed, "iterations_attempted": attempted,
        "iteration_budget": 3000, "accepted_additions": accepted,
        "time_budget_seconds": float(os.environ["MATHBENCH_SEARCH_SECONDS"]) if "MATHBENCH_SEARCH_SECONDS" in os.environ else None}}
