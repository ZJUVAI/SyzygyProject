"""Seeded randomized greedy construction; never reads comparison assets."""
import os, random
from mathbench.search import search_steps

N = 100
RESTARTS = 4

def _d2(a, b): return (a[0]-b[0])**2 + (a[1]-b[1])**2

def _addable(p, chosen, distance_sets):
    ds = [_d2(p, q) for q in chosen]
    if len(set(ds)) != len(ds): return False
    return all(d not in distance_sets[i] for i, d in enumerate(ds))

def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T101-C01") != "T101-C01": raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0")); rng = random.Random(seed)
    best = [(0, 0), (1, 0)]; steps = iter(search_steps(RESTARTS)); done = 0
    grid = [(x, y) for x in range(N) for y in range(N)]
    for _ in range(RESTARTS):
        if next(steps, None) is None: break
        order = grid[:]; rng.shuffle(order); chosen = []; distances = []
        for p in order:
            if not chosen:
                chosen.append(p); distances.append(set()); continue
            if _addable(p, chosen, distances):
                ds = [_d2(p, q) for q in chosen]
                chosen.append(p); distances.append(set(ds))
                for i, d in enumerate(ds): distances[i].add(d)
        if len(chosen) > len(best): best = chosen[:]
        done += 1
    return {"points": [list(p) for p in best], "claimed_objective": len(best), "search_metadata": {"algorithm": "seeded randomized greedy insertion using exact squared-distance uniqueness", "seed": seed, "restarts": done}}
