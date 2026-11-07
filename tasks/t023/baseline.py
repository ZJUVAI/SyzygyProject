"""Seeded random construction, exact repair, then greedy row deletion."""
import os
import random
from array import array
from itertools import combinations
from mathbench.search import search_steps


def run_code():
    k, t, v = 20, 4, 2
    width = v ** t
    cols = list(combinations(range(k), t))
    projection_count = len(cols)
    counts = [0] * (projection_count * width)
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    steps = iter(search_steps(100_000))
    iterations = 0

    def charge_step():
        nonlocal iterations
        step = next(steps, None)
        if step is None:
            return False
        iterations += 1
        return True

    def add_row(row):
        ids = array("I")
        for ci, c in enumerate(cols):
            pattern = 0
            for j in c:
                pattern = (pattern << 1) | row[j]
            idx = ci * width + pattern
            ids.append(idx)
            counts[idx] += 1
        return ids

    # A random starting sample. Repeated rows are removed deterministically.
    rows = []
    row_ids = []
    present = set()
    while len(rows) < 256 and charge_step():
        row = tuple(rng.randrange(v) for _ in range(k))
        if row in present:
            continue
        present.add(row)
        rows.append(row)
        row_ids.append(add_row(row))

    # Repair every uncovered interaction by adding a row that realizes it.
    missing = {i for i, count in enumerate(counts) if count == 0}
    while missing and charge_step():
        target = next(iter(missing))
        ci, pattern = divmod(target, width)
        row = [rng.randrange(v) for _ in range(k)]
        value = pattern
        for j in reversed(cols[ci]):
            row[j] = value % v
            value //= v
        row = tuple(row)
        if row in present:
            # A missing interaction cannot be present in an existing row.
            raise RuntimeError("repair selected an already present row")
        present.add(row)
        rows.append(row)
        ids = add_row(row)
        row_ids.append(ids)
        for idx in ids:
            if counts[idx] == 1:
                missing.discard(idx)

    # If an explicit wall-clock cutoff interrupted repair, use the guaranteed
    # feasible simple construction instead of returning a partial array.
    if missing:
        from tasks.t023.init_program import run_code as simple_seed
        return {**simple_seed(), "search_metadata": {
            "seed": int(os.environ.get("MATHBENCH_SEED", "0")),
            "algorithm": "random rows, exact uncovered-pattern repair, greedy deletion",
            "iterations": iterations, "fallback": "Hamming weight <= 4 seed",
            "search_limit_steps": 100_000}}

    order = list(range(len(rows)))
    rng.shuffle(order)
    alive = bytearray([1]) * len(rows)
    for ri in order:
        if not charge_step():
            break
        ids = row_ids[ri]
        if all(counts[idx] > 1 for idx in ids):
            alive[ri] = 0
            for idx in ids:
                counts[idx] -= 1
    output_rows = [[int(x) for x in row] for i, row in enumerate(rows) if alive[i]]
    return {"array": output_rows, "search_metadata": {
        "seed": int(os.environ.get("MATHBENCH_SEED", "0")),
        "algorithm": "256 random rows, exact uncovered-pattern repair, seeded greedy row deletion",
        "iterations": iterations, "search_limit_steps": 100_000,
        "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS")}}
