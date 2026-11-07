"""Search-only helpers; these functions do not load comparison witnesses."""

import os


def search_integer_limit():
    """Return a heuristic proposal cap; the task and checker have no such cap."""
    value = int(os.environ.get("MATHBENCH_SEARCH_INTEGER_LIMIT", "4096"))
    if value < 32:
        raise ValueError("search integer limit must be at least 32")
    return value


def score(elements):
    sums = {a + b for a in elements for b in elements}
    products = {a * b for a in elements for b in elements}
    return max(len(sums), len(products))


def mutate(elements, rng, integer_limit):
    child = list(elements)
    count = 1 if rng.random() < 0.85 else 2
    for _ in range(count):
        index = rng.randrange(len(child))
        occupied = set(child)
        occupied.remove(child[index])
        choices = [x for x in range(1, integer_limit + 1) if x not in occupied]
        child[index] = rng.choice(choices)
    return sorted(child)
