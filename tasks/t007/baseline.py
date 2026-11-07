from mathbench.search import search_deadline, search_steps
"""Bounded seeded random construction with non-equivalent local moves."""
import os
import random
import time
import os
from itertools import combinations

from .check import validate


def _valid(marks):
    ds = [b-a for a, b in combinations(marks, 2)]
    return len(ds) == len(set(ds))


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T007-C01")
    counts = {"T007-C01": 29, "T007-C02": 30, "T007-C03": 32}
    if config_id not in counts:
        raise ValueError(f"unknown T007 configuration: {config_id}")
    count = counts[config_id]
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    seconds = max(.01, min(30., float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2"))))
    deadline = search_deadline()
    # Construct a guaranteed-valid fallback without loading either witness.
    best = [0]
    best_differences = set()
    while len(best) < count:
        c = best[-1] + 1
        while True:
            new = [c - p for p in best]
            if len(set(new)) == len(new) and not (set(new) & best_differences):
                best.append(c)
                best_differences.update(new)
                break
            c += 1
    # Greedy random gap construction produces valid, varied starting rulers.
    for restart in range(100):
        marks = [0]
        diffs = set()
        while len(marks) < count and time.monotonic() < deadline:
            start = marks[-1] + 1
            candidates = list(range(start, start + 45))
            rng.shuffle(candidates)
            for c in candidates:
                new = [c - p for p in marks]
                if len(set(new)) == len(new) and not (set(new) & diffs):
                    marks.append(c); diffs.update(new); break
            else:
                break
        if len(marks) == count and marks[-1] < best[-1] and _valid(marks):
            best = marks
        if time.monotonic() >= deadline: break
    validate({"marks": best}, {"parameters": {"marks": count}})
    return {"marks": best}
