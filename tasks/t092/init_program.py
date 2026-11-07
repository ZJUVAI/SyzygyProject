"""Standalone homogenized Legendre zonal harmonic P_20(z)."""
import os
from fractions import Fraction

DEGREE = 20
EXPONENTS = [(a, b, DEGREE - a - b) for a in range(DEGREE, -1, -1) for b in range(DEGREE - a, -1, -1)]


def _add_scaled(target, source, scale):
    out = dict(target)
    for exponent, value in source.items():
        out[exponent] = out.get(exponent, Fraction(0)) + scale * value
    return {key: value for key, value in out.items() if value}


def _multiply_r2(poly):
    out = {}
    for (a, b, c), value in poly.items():
        for exponent in ((a + 2, b, c), (a, b + 2, c), (a, b, c + 2)):
            out[exponent] = out.get(exponent, Fraction(0)) + value
    return out


def _zonal():
    h0 = {(0, 0, 0): Fraction(1)}
    h1 = {(0, 0, 1): Fraction(1)}
    for n in range(1, DEGREE):
        zhn = {(a, b, c + 1): value * (2 * n + 1) for (a, b, c), value in h1.items()}
        r2hprev = _multiply_r2(h0)
        numerator = _add_scaled(zhn, r2hprev, Fraction(-n))
        hn1 = {key: value / (n + 1) for key, value in numerator.items()}
        h0, h1 = h1, hn1
    return h1


def _text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T092-C01") != "T092-C01":
        raise ValueError("unsupported configuration")
    polynomial = _zonal()
    return {"coefficients": [_text(polynomial.get(exponent, Fraction(0))) for exponent in EXPONENTS]}
