"""Generic random-greedy F_2^13 construction plus seeded row-deletion proposals."""
import os
import random

from tasks.t091.check import validate


def _generic_labels(dimension, seed):
    rng = random.Random(seed)
    labels = []
    blocked = {0}
    proposals = 0
    while len(labels) < 63:
        value = rng.randrange(1, 1 << dimension)
        proposals += 1
        if value in blocked:
            continue
        old = labels
        blocked.add(value)
        for a in old:
            blocked.add(value ^ a)
        for i, a in enumerate(old):
            for b in old[i + 1:]:
                blocked.add(value ^ a ^ b)
        labels.append(value)
    return labels, proposals


def _rows(labels, dimension):
    result = []
    for form in range(1 << dimension):
        row = 0
        for j, label in enumerate(labels):
            row |= ((form & label).bit_count() & 1) << j
        result.append(row)
    if len(set(result)) != 1 << dimension:
        raise RuntimeError("random-greedy labels do not span their row space")
    return result


def search(iterations):
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    labels, label_proposals = _generic_labels(13, seed)
    current = _rows(labels, 13)
    best = current[:]
    rng = random.Random(seed ^ 0x5A17)
    accepted = proposals = 0
    for _ in range(int(iterations)):
        proposals += 1
        indices = set(rng.sample(range(len(current)), 16))
        trial = [row for i, row in enumerate(current) if i not in indices]
        try:
            validate({"rows": trial}, {"id": "T091-C01", "parameters": {
                "columns": 63, "levels": 2, "strength": 4, "row_repetition": "allowed"}})
        except ValueError:
            continue
        current = trial
        accepted += 1
        if len(current) < len(best):
            best = current[:]
    return {
        "rows": best,
        "search_metadata": {
            "seed": seed,
            "seed_dimension": 13,
            "label_proposals": label_proposals,
            "iterations_requested": int(iterations),
            "proposals_evaluated": proposals,
            "moves_accepted": accepted,
            "seed_rows": 1 << 13,
            "row_deletion_proposal_size": 16,
            "comparison_data_read": False
        }
    }
