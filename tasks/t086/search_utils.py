"""Heuristic search utilities; no human/reference files are imported."""

from itertools import permutations, product
import math


def diagonal_ratio(diagonals):
    def product_norm(indices):
        squared = 0
        for coordinate in range(3):
            value = 1
            for index in indices:
                value *= diagonals[index][coordinate]
            squared += value * value
        return math.sqrt(squared)

    wr = sum(product_norm(t) for t in product(range(4), repeat=4)) / 256
    wo = sum(product_norm(t) for t in permutations(range(4))) / 24
    return wr / wo if wo else math.inf


def mutate_diagonals(diagonals, rng):
    result = [row[:] for row in diagonals]
    matrix = rng.randrange(4)
    coordinate = rng.randrange(3)
    result[matrix][coordinate] = rng.randint(1, 5)
    return result
