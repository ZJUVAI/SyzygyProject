from mathbench.search import search_deadline, search_steps
"""Greedy set cover on sampled blocks, with a guaranteed seed fallback."""
import os
import random
import time
from itertools import combinations
from tasks.t060.init_program import run_code as seed_cover


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T060-C01") != "T060-C01":
        raise ValueError("unsupported configuration")
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    try:
        budget = min(2.0, max(0.01, float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2"))))
    except ValueError:
        budget = 2.0
    deadline = search_deadline()
    blocks = [tuple(b) for b in seed_cover()["blocks"]]
    index = {q: i for i, q in enumerate(combinations(range(24), 4))}
    pool = set()
    for _ in search_steps(500):
        pool.add(tuple(sorted(rng.sample(range(24), 14))))
    # Add the seed blocks to ensure the candidate pool covers every four-set.
    pool = sorted(pool | set(blocks))
    masks = [sum(1 << index[q] for q in combinations(b, 4)) for b in pool]
    remaining = (1 << 10626) - 1
    chosen = []
    while remaining and time.monotonic() < deadline:
        i = max(range(len(pool)), key=lambda j: (masks[j] & remaining).bit_count())
        if not (masks[i] & remaining):
            break
        chosen.append(pool[i])
        remaining &= ~masks[i]
    if not remaining and len(chosen) < len(blocks):
        blocks = chosen
    return {"blocks": [list(b) for b in blocks]}
