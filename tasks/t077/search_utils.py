"""Search helpers for T077; they do not read comparison data."""

import math


LOWER = -1_000_000
UPPER = 1_000_000


def cardinalities(values):
    sums = {a + b for a in values for b in values}
    differences = {a - b for a in values for b in values}
    return len(sums), len(differences)


def heuristic_score(values):
    sum_size, difference_size = cardinalities(values)
    return math.log(difference_size) / math.log(sum_size)


def mutate(values, rng):
    child = set(values)
    mode = rng.random()
    if mode < 0.25 and len(child) < 512:
        while True:
            new_value = rng.randint(LOWER, UPPER)
            if new_value not in child:
                child.add(new_value)
                break
    elif mode < 0.40 and len(child) > 2:
        child.remove(rng.choice(sorted(child)))
    else:
        old_value = rng.choice(sorted(child))
        child.remove(old_value)
        while True:
            new_value = rng.randint(LOWER, UPPER)
            if new_value not in child:
                child.add(new_value)
                break
    return sorted(child)
