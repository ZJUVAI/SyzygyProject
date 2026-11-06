"""Cold-start local evolution for finite integer sum-difference sets.

The optimizer starts only from the public task seed, keeps the best exact
checker-approved construction, and makes small structural edits so that a
useful MSTD set is not destroyed by unrelated large coordinates.
"""
import math
import os
import random
import time

from tasks.t057.check import validate
from tasks.t057.init_program import run_code as initial_program


_CONFIG = {"id": "T057-C01", "parameters": {
    "max_cardinality": 512, "integer_interval": [-1000000, 1000000]}}
_LOW, _HIGH = -1_000_000, 1_000_000


def _measure(values):
    """Return (score, sum size, difference size), or None when undefined."""
    n = len(values)
    sums = {a + b for a in values for b in values}
    diffs = {a - b for a in values for b in values}
    s, d = len(sums), len(diffs)
    if s <= d or d <= n:
        return None
    return math.log(s / n) / math.log(d / n), s, d


def _proposal(current, rng):
    """Make a bounded local point, fringe, or cardinality edit."""
    trial = current.copy()
    mode = rng.random()
    if mode < 0.64:
        # Move one existing point by a short amount. Occasionally move it
        # farther, while keeping the rest of a structured core intact.
        i = rng.randrange(len(trial))
        scale = rng.choice((1, 2, 3, 4, 6, 8, 12, 20, 40))
        delta = rng.choice((-scale, scale))
        value = trial[i] + delta
        if _LOW <= value <= _HIGH and value not in trial:
            trial[i] = value
    elif mode < 0.83 and len(trial) < 512:
        # Prefer adding near the current fringe or in a small gap. A rare
        # wider move explores a new fringe without spraying huge coordinates.
        ordered = sorted(trial)
        if rng.random() < 0.72:
            gap = rng.randrange(len(ordered) - 1)
            left, right = ordered[gap], ordered[gap + 1]
            if right - left > 1:
                value = rng.randint(left + 1, right - 1)
            else:
                value = ordered[0] - rng.randint(1, 8) if rng.random() < .5 else ordered[-1] + rng.randint(1, 8)
        else:
            span = max(8, ordered[-1] - ordered[0])
            value = (ordered[0] if rng.random() < .5 else ordered[-1]) + rng.choice((-1, 1)) * rng.randint(1, min(span, 64))
        if _LOW <= value <= _HIGH and value not in trial:
            trial.append(value)
    else:
        # Deletion is useful for pruning points that inflate A-A.
        if len(trial) > 2:
            trial.pop(rng.randrange(len(trial)))
    return sorted(trial)


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T057-C01") != "T057-C01":
        raise ValueError("unsupported configuration")
    try:
        budget = max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    except (TypeError, ValueError):
        budget = 45.0
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    deadline = time.monotonic() + budget

    # Normalize ordering and deduplicate the supplied cold-start seed. The
    # exact checker establishes the incumbent before search begins.
    best = sorted(set(initial_program()["set"]))
    checked = validate({"set": best}, _CONFIG)
    best_score = float(checked["objective"])
    current = best[:]
    current_measure = _measure(current)
    current_score = current_measure[0]
    iteration = 0

    while time.monotonic() < deadline:
        iteration += 1
        trial = _proposal(current, rng)
        measured = _measure(trial)
        if measured is None:
            # Failed MSTD proposals do not replace the valid state. Periodic
            # restarts from the best construction maintain useful exploration.
            if iteration % 80 == 0:
                current = best[:]
                current_score = best_score
            continue
        score = measured[0]
        # Simulated annealing accepts a few regressions to cross local plateaus.
        progress = min(1.0, (time.monotonic() - (deadline - budget)) / max(budget, 1e-9))
        temperature = 0.012 * (1.0 - progress) + 0.0004
        if score >= current_score or rng.random() < math.exp((score - current_score) / temperature):
            current, current_score = trial, score
        if score > best_score:
            try:
                result = validate({"set": trial}, _CONFIG)
            except (TypeError, ValueError, OverflowError):
                continue
            # Recomputed objective is authoritative; retain only a strict gain.
            exact_score = float(result["objective"])
            if exact_score > best_score:
                best, best_score = trial, exact_score

    # Recheck the archived construction at the return boundary.
    validate({"set": best}, _CONFIG)
    return {"set": best}


if __name__ == "__main__":
    print(run_code())
