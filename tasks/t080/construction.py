"""Finite simplex projection from Gyarmati, Hennecart, and Ruzsa §2."""

from itertools import product


def projected_simplex(m=6, L=5):
    weights = [1]
    for _ in range(1, m):
        weights.append(2 * L * weights[-1] + 1)
    values = []
    for vector in product(range(L + 1), repeat=m):
        if sum(vector) <= L:
            values.append(sum(x * weight for x, weight in zip(vector, weights)))
    if len(set(values)) != len(values):
        raise ValueError("projection weights did not produce distinct integers")
    return sorted(values), weights
