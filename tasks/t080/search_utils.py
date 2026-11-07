"""Search helpers for T080; no comparison data is loaded."""

import math


def exact_counts(values):
    sums = {a + b for a in values for b in values}
    differences = {a - b for a in values for b in values}
    return len(sums), len(differences)


def heuristic_score(values):
    sum_size, difference_size = exact_counts(values)
    q = 2 * max(values) + 1
    if difference_size >= q:
        return None
    return 1 + math.log(difference_size / sum_size) / math.log(q)


def mutate(values, rng):
    child = set(values)
    mode = rng.random()
    if mode < 0.25 and len(child) < 512:
        while True:
            value = rng.randint(1, 1_000_000)
            if value not in child:
                child.add(value)
                break
    elif mode < 0.40 and len(child) > 2:
        child.remove(rng.choice(sorted(x for x in child if x != 0)))
    else:
        old = rng.choice(sorted(x for x in child if x != 0))
        child.remove(old)
        while True:
            value = rng.randint(1, 1_000_000)
            if value not in child:
                child.add(value)
                break
    return sorted(child)
