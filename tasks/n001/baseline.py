from mathbench.search import search_deadline, search_steps
"""Seeded randomized greedy and one-for-many bitset local search."""
import itertools
import os
import random
import time

N = 7 ** 5

def _decode(v):
    out = [0] * 5
    for i in range(4, -1, -1):
        out[i] = v % 7
        v //= 7
    return tuple(out)

def _encode(w):
    v = 0
    for x in w:
        v = 7 * v + x
    return v

def _neighbors(v):
    w = _decode(v)
    choices = [((x - 1) % 7, x, (x + 1) % 7) for x in w]
    for u in itertools.product(*choices):
        x = _encode(u)
        if x != v:
            yield x

def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    try:
        budget = min(2.0, max(0.05, float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2"))))
    except ValueError:
        budget = 2.0
    rng = random.Random(seed)
    deadline = search_deadline()
    best = [_encode(w) for w in itertools.product((0,2,4), repeat=5)]
    for _attempt in search_steps(1):
        order = list(range(N))
        rng.shuffle(order)
        chosen = []
        blocked = 0
        for v in order:
            bit = 1 << v
            if blocked & bit:
                continue
            chosen.append(v)
            blocked |= bit
            for u in _neighbors(v):
                blocked |= 1 << u
        if len(chosen) > len(best):
            best = chosen
        # Remove a selected vertex, then greedily insert compatible vertices
        # from its closed neighborhood. This can improve cardinality.
        for _ in range(min(8, len(chosen))):
            if time.monotonic() >= deadline:
                break
            pos = rng.randrange(len(chosen))
            trial = chosen[:pos] + chosen[pos+1:]
            mask = 0
            for v in trial:
                mask |= 1 << v
                for u in _neighbors(v):
                    mask |= 1 << u
            pool = list(_neighbors(chosen[pos]))
            rng.shuffle(pool)
            for v in pool:
                bit = 1 << v
                if not mask & bit:
                    trial.append(v); mask |= bit
                    for u in _neighbors(v): mask |= 1 << u
            if len(trial) > len(chosen):
                chosen = trial
            if len(chosen) > len(best):
                best = chosen[:]
    return {"words": [list(_decode(v)) for v in best]}
