"""Fixed-seed greedy extension search for unrestricted discrepancy C=3."""

import math
import os
import random
import time


def _divisors_table(limit):
    divisors = [[] for _ in range(limit + 1)]
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            divisors[n].append(d)
    return divisors


def _grow(divisors, limit, rng, counter, deadline=None):
    sums = [0] * (limit + 1)
    seq = []
    for n in range(1, limit + 1):
        if deadline is not None and time.monotonic() >= deadline:
            break
        allowed = [s for s in (-1, 1) if all(abs(sums[d] + s) <= 3 for d in divisors[n])]
        counter[0] += 1
        if not allowed:
            break
        sign = rng.choice(allowed)
        seq.append(sign)
        for d in divisors[n]:
            sums[d] += sign
    return seq


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    trials = int(os.environ.get("T051_SEARCH_TRIALS", "24"))
    limit = int(os.environ.get("T051_SEARCH_LIMIT", "5000"))
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    if trials < 0 or limit < 1:
        raise ValueError("search trials must be nonnegative and limit positive")
    if seconds is None:
        deadline = None
    else:
        duration = float(seconds)
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + duration
    divisors = _divisors_table(limit)
    rng = random.Random(seed)
    best = [1]
    attempts = [0]
    completed = 0
    for _ in range(trials):
        candidate = _grow(divisors, limit, rng, attempts, deadline)
        completed += 1
        if len(candidate) > len(best):
            best = candidate
        if deadline is not None and time.monotonic() >= deadline:
            break
    return {"sequence": best, "search": {
        "algorithm": "random greedy legal-sign extension; every divisor-ending prefix checked",
        "seed": seed,
        "trial_limit": trials,
        "trials_completed": completed,
        "extension_attempts": attempts[0],
        "search_limit": limit,
        "reference_data_read": False,
    }}
