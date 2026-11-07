"""Standalone random-greedy F_2^14 seed; it uses no BCH or comparison assets."""
import os
import random


def _labels(dimension, seed):
    rng = random.Random(seed)
    chosen = []
    blocked = {0}
    proposed = 0
    while len(chosen) < 63:
        value = rng.randrange(1, 1 << dimension)
        proposed += 1
        if value in blocked:
            continue
        old = chosen
        blocked.add(value)
        for a in old:
            blocked.add(value ^ a)
        for i, a in enumerate(old):
            for b in old[i + 1:]:
                blocked.add(value ^ a ^ b)
        chosen.append(value)
    return chosen, proposed


def _rows(labels, dimension):
    rows = []
    for linear_form in range(1 << dimension):
        row = 0
        for j, label in enumerate(labels):
            row |= ((linear_form & label).bit_count() & 1) << j
        rows.append(row)
    if len(set(rows)) != 1 << dimension:
        raise RuntimeError("the labels do not span the full row space")
    return rows


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T091-C01") != "T091-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    labels, _ = _labels(14, seed)
    return {"rows": _rows(labels, 14)}
