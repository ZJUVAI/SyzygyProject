"""Randomized bitset search for independent sets in C7^5.

The product code in ``init_program.py`` remains the cold-start fallback. This
program uses only the task definition and constructs its own candidates.
"""

import itertools
import os
import random
import time

N = 7 ** 5
_POWERS = (7 ** 4, 7 ** 3, 7 ** 2, 7, 1)
_NEIGHBORHOODS = None


def _build_neighborhoods():
    """Return closed-neighborhood bitsets for all 7^5 words."""
    out = [0] * N
    for v in range(N):
        x = v
        digits = [0] * 5
        for i in range(4, -1, -1):
            digits[i] = x % 7
            x //= 7
        choices = [((d - 1) % 7, d, (d + 1) % 7) for d in digits]
        mask = 0
        for word in itertools.product(*choices):
            u = 0
            for d in word:
                u = 7 * u + d
            mask |= 1 << u
        out[v] = mask
    return out


def _decode(v):
    word = [0] * 5
    for i in range(4, -1, -1):
        word[i] = v % 7
        v //= 7
    return word


def run_code():
    global _NEIGHBORHOODS
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    try:
        budget = min(45.0, max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45"))))
    except ValueError:
        budget = 45.0
    rng = random.Random(seed)
    # Valid initial construction: the Cartesian product {0,2,4}^5.
    best = [sum(d * p for d, p in zip(word, _POWERS))
            for word in itertools.product((0, 2, 4), repeat=5)]
    if budget <= 0:
        return {"words": [_decode(v) for v in best]}
    if _NEIGHBORHOODS is None:
        _NEIGHBORHOODS = _build_neighborhoods()
    neighborhoods = _NEIGHBORHOODS
    deadline = time.monotonic() + budget

    while time.monotonic() < deadline:
        order = list(range(N))
        rng.shuffle(order)
        chosen = []
        blocked = 0
        for v in order:
            bit = 1 << v
            if blocked & bit:
                continue
            chosen.append(v)
            blocked |= neighborhoods[v]
        if len(chosen) > len(best):
            best = chosen

        # Remove a small random group, then greedily refill from vertices
        # whose neighborhoods intersect the removed words. The trial is
        # committed only when it increases the set.
        for _ in range(6):
            if time.monotonic() >= deadline or len(chosen) < 2:
                break
            remove_count = rng.choice((1, 2, 3))
            positions = set(rng.sample(range(len(chosen)), min(remove_count, len(chosen))))
            removed = [chosen[i] for i in positions]
            trial = [v for i, v in enumerate(chosen) if i not in positions]
            mask = 0
            for v in trial:
                mask |= neighborhoods[v]
            pool = set()
            for v in removed:
                bits = neighborhoods[v]
                while bits:
                    low = bits & -bits
                    pool.add(low.bit_length() - 1)
                    bits ^= low
            candidates = list(pool)
            rng.shuffle(candidates)
            for v in candidates:
                bit = 1 << v
                if not mask & bit:
                    trial.append(v)
                    mask |= neighborhoods[v]
            if len(trial) > len(chosen):
                chosen = trial
                if len(chosen) > len(best):
                    best = chosen[:]

    return {"words": [_decode(v) for v in best]}
