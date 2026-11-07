"""Rebuild the 17-point, 40-line rationally parameterized cubic construction."""

import os
from fractions import Fraction

from tasks.t066.algebra import add, div, from_int, mul, one, serialize_element, sub, zero


# Minimal polynomial of alpha = tan(pi/17), coefficients in ascending order.
MODULUS_INTS = (17, 0, -680, 0, 6188, 0, -19448, 0, 24310, 0, -12376, 0, 2380, 0, -136, 0, 1)
MODULUS = tuple(Fraction(value) for value in MODULUS_INTS)
DEGREE = len(MODULUS) - 1
ISOLATING_INTERVAL = ["9/50", "19/100"]


def build_human_orchard():
    alpha = tuple([Fraction(0), Fraction(1)] + [Fraction(0)] * (DEGREE - 2))
    tangent = zero(DEGREE)
    points = []
    for _k in range(17):
        tangent_squared = mul(tangent, tangent, MODULUS)
        y = div(mul(tangent_squared, tangent, MODULUS), add(one(DEGREE), tangent_squared), MODULUS)
        points.append({"x": serialize_element(tangent), "y": serialize_element(y)})
        tangent = div(
            add(tangent, alpha),
            sub(one(DEGREE), mul(alpha, tangent, MODULUS)),
            MODULUS,
        )
    return {
        "minimal_polynomial": list(MODULUS_INTS),
        "isolating_interval": list(ISOLATING_INTERVAL),
        "points": points,
    }


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T066-C01")
    if chosen != "T066-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return build_human_orchard()
