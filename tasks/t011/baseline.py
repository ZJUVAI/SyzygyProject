from mathbench.search import search_deadline, search_steps
"""Seeded randomized greedy and one-for-many bitset local search."""
import itertools
import os
import random
import time

def _power():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T011-C01")
    powers = {"T011-C01": 5, "T011-C02": 4, "T011-C03": 6}
    if cid not in powers:
        raise ValueError(f"unsupported configuration: {cid}")
    return powers[cid]

def _size(power):
    return 7 ** power

def _decode(v, power):
    out = [0] * power
    for i in range(power - 1, -1, -1):
        out[i] = v % 7
        v //= 7
    return tuple(out)

def _encode(w):
    v = 0
    for x in w:
        v = 7 * v + x
    return v

def _neighbors(v, power):
    w = _decode(v, power)
    choices = [((x - 1) % 7, x, (x + 1) % 7) for x in w]
    for u in itertools.product(*choices):
        x = _encode(u)
        if x != v:
            yield x

def run_code():
    power = _power()
    size = _size(power)
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    try:
        budget = min(2.0, max(0.05, float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2"))))
    except ValueError:
        budget = 2.0
    rng = random.Random(seed)
    deadline = search_deadline()
    best = [_encode(w) for w in itertools.product((0,2,4), repeat=power)]
    for _attempt in search_steps(1):
        order = list(range(size))
        rng.shuffle(order)
        chosen = []
        blocked = 0
        for v in order:
            bit = 1 << v
            if blocked & bit:
                continue
            chosen.append(v)
            blocked |= bit
            for u in _neighbors(v, power):
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
                for u in _neighbors(v, power):
                    mask |= 1 << u
            pool = list(_neighbors(chosen[pos], power))
            rng.shuffle(pool)
            for v in pool:
                bit = 1 << v
                if not mask & bit:
                    trial.append(v); mask |= bit
                    for u in _neighbors(v, power): mask |= 1 << u
            if len(trial) > len(chosen):
                chosen = trial
            if len(chosen) > len(best):
                best = chosen[:]
    return {"words": [list(_decode(v, power)) for v in best]}
