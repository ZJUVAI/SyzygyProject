"""Finite integer projection from Gyarmati, Hennecart, and Ruzsa §2."""

from itertools import product


def projected_simplex(m=6, L=5):
    """Return the projection of V(m,L) using the paper's recurrence weights."""
    weights = [1]
    for _ in range(1, m):
        weights.append(2 * L * weights[-1] + 1)
    values = []
    for vector in product(range(L + 1), repeat=m):
        if sum(vector) <= L:
            values.append(sum(x * weight for x, weight in zip(vector, weights)))
    if len(set(values)) != len(values):
        raise ValueError("projection weights did not produce a unique integer set")
    return sorted(values), weights
