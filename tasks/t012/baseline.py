from mathbench.search import search_deadline, search_steps
"""Bounded deterministic integer add/delete local search."""
import math
import os
import random
import time
from tasks.t012.init_program import run_code as seed_program


def _score(a):
    n = len(a)
    if n < 2:
        return None
    sums = {x + y for x in a for y in a}
    diffs = {x - y for x in a for y in a}
    if len(sums) <= len(diffs) or len(diffs) <= n:
        return None
    return math.log(len(sums) / n) / math.log(len(diffs) / n)


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T012-C01") != "T012-C01":
        raise ValueError("unsupported configuration")
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    try:
        budget = min(2.0, max(0.01, float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2"))))
    except ValueError:
        budget = 2.0
    deadline = search_deadline()
    current = sorted(set(seed_program()["set"]))
    best = current[:]
    best_score = _score(best)
    lo, hi = -1000000, 1000000
    for _attempt in search_steps(2000):
        trial = current[:]
        if len(trial) < 512 and (len(trial) <= 2 or rng.random() < 0.55):
            choices = [x for x in (rng.randint(lo, hi) for _ in range(20)) if x not in set(trial)]
            if choices:
                trial.append(choices[0])
                trial.sort()
        elif len(trial) > 2:
            trial.pop(rng.randrange(len(trial)))
        score = _score(trial)
        if score is not None and (best_score is None or score > best_score):
            best, best_score = trial, score
            current = trial
        elif score is not None and rng.random() < 0.08:
            current = trial
    return {"set": best}
