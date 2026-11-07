from mathbench.search import search_deadline, search_steps
"""Greedy set cover on sampled blocks, with a guaranteed seed fallback."""
import os
import random
import time
from itertools import combinations
from tasks.t008.init_program import run_code as seed_cover


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T008-C01")
    if config_id == "T008-C02":
        return _configured_greedy(config_id)
    if config_id != "T008-C01":
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


def _configured_greedy(config_id):
    from math import comb
    from tasks.t008.init_program import PARAMS
    v, k, t = PARAMS[config_id]
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    blocks = [tuple(b) for b in seed_cover_for(config_id)["blocks"]]
    universe = tuple(combinations(range(v), t))
    index = {q: i for i, q in enumerate(universe)}
    fallback = blocks
    pool = set()
    for _ in range(500):
        pool.add(tuple(sorted(rng.sample(range(v), k))))
    pool = sorted(pool)
    masks = [sum(1 << index[q] for q in combinations(b, t)) for b in pool]
    remaining = (1 << len(universe)) - 1
    chosen = []
    deadline = search_deadline()
    while remaining and time.monotonic() < deadline:
        i = max(range(len(pool)), key=lambda j: (masks[j] & remaining).bit_count())
        gain = masks[i] & remaining
        if not gain:
            break
        chosen.append(pool[i]); remaining &= ~masks[i]
    selected = list(chosen)
    # Close any remaining requirements with the configuration's cold seed.
    for block in fallback:
        mask = sum(1 << index[q] for q in combinations(block, t))
        if mask & remaining:
            selected.append(block)
            remaining &= ~mask
        if not remaining:
            break
    if remaining:
        return {"blocks": [list(b) for b in fallback]}
    return {"blocks": [list(b) for b in selected]}


def seed_cover_for(config_id):
    previous = os.environ.get("MATHBENCH_CONFIG_ID")
    os.environ["MATHBENCH_CONFIG_ID"] = config_id
    try:
        return seed_cover()
    finally:
        if previous is None:
            os.environ.pop("MATHBENCH_CONFIG_ID", None)
        else:
            os.environ["MATHBENCH_CONFIG_ID"] = previous
