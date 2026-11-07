"""Rational reconstruction of Rechenberg's published 12-point diagram."""

from fractions import Fraction
import math
import os


SQRT3_DENOMINATOR = 10**63
SQRT3_LOWER_NUMERATOR = 1732050807568877293527446341505872366942805253810380628055806979


def build_rechenberg12_rational():
    # Exact floor(sqrt(3)*10^63), with the integer proof checked below.
    numerator = math.isqrt(3 * SQRT3_DENOMINATOR**2)
    if numerator != SQRT3_LOWER_NUMERATOR:
        raise ArithmeticError("frozen square-root reconstruction is inconsistent")
    r = Fraction(numerator, SQRT3_DENOMINATOR)
    if not (r * r < 3 < Fraction(numerator + 1, SQRT3_DENOMINATOR) ** 2):
        raise ArithmeticError("rational does not bracket sqrt(3)")
    half = Fraction(1, 2)
    points = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (half, r / 2),
        (half, 1 + r / 2),
        (half - r / 2, half + r / 2),
        (half + r / 2, half + r / 2),
        (-r / 2, half),
        (-r / 2, -half),
        (Fraction(0), Fraction(-1)),
        (Fraction(1), Fraction(-1)),
        (1 + r / 2, -half),
        (1 + r / 2, half),
    ]
    return {
        "points": [
            [x.numerator if x.denominator == 1 else str(x),
             y.numerator if y.denominator == 1 else str(y)]
            for x, y in points
        ]
    }


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T081-C01")
    if chosen != "T081-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return build_rechenberg12_rational()
