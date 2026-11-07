"""Exact rational-coordinate D4 and generic field serialization helpers."""

from fractions import Fraction
from itertools import product
from math import isqrt


def rational_text(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def rational_field():
    return {"minimal_polynomial": [0, 1], "isolating_interval": ["-1", "1"]}


def serialize_rational_points(points):
    return {
        **rational_field(),
        "points": [[[rational_text(value)] for value in point] for point in points],
    }


def d4_24cell_points():
    points = []
    for axis in range(4):
        for sign in (-1, 1):
            point = [Fraction(0)] * 4
            point[axis] = Fraction(sign)
            points.append(point)
    points.extend(
        [Fraction(sign, 2) for sign in signs]
        for signs in product((-1, 1), repeat=4)
    )
    return points


def signed_permutation_orbit(pattern):
    from itertools import permutations

    points = set()
    for permuted in set(permutations(pattern)):
        nonzero = [axis for axis, value in enumerate(permuted) if value]
        for signs in product((-1, 1), repeat=len(nonzero)):
            point = list(permuted)
            for axis, sign in zip(nonzero, signs):
                point[axis] *= sign
            points.add(tuple(point))
    return sorted(points)


def radical_field_solution(integer_points, squared_norm):
    """Encode v/sqrt(s) using alpha=sqrt(s), so coordinate is v*alpha/s."""
    return {
        "minimal_polynomial": [-squared_norm, 0, 1],
        "isolating_interval": [str(isqrt(squared_norm)), str(isqrt(squared_norm) + 1)],
        "points": [
            [["0", rational_text(Fraction(value, squared_norm))] for value in point]
            for point in integer_points
        ],
    }
