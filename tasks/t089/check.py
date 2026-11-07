"""Exact checker for polynomial-Gaussian sign-uncertainty witnesses."""

from __future__ import annotations

import math
from fractions import Fraction
from functools import reduce
from math import comb, factorial, isqrt

import sympy as sp


CONFIG_ID = "T089-C01"
_EXPECTED_PARAMETERS = {
    "dimension": 1,
    "polynomial_variable": "t=pi*x^2",
    "candidate_family": "p(t)*exp(-pi*x^2), p in Q[t], finite degree without a configured cap",
    "fourier_convention": "integral f(x)*exp(-2*pi*i*x*xi) dx",
    "origin_signs": "p(0)<0 and q(0)<0",
    "objective": "minimize A(f)*A(fhat); exact algebraic root isolation, rational interval returned",
}
_ROOT_EPS = sp.Rational(1, 10**30)
_PI_TERMS_5 = 60
_PI_TERMS_239 = 20
_SCALE = 10**40


def _fraction(value):
    if type(value) is bool:
        raise ValueError("Boolean coefficients are not numbers here")
    if type(value) is int:
        return Fraction(value)
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("Coefficient floats must be finite")
        return Fraction.from_float(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("Coefficient strings must be exact rational numbers") from exc
    raise ValueError("Coefficients must be integers, finite floats, or rational strings")


def _trim(values):
    values = list(values)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return values


def _fourier_polynomial(p):
    """Map p(t) to q(t) for f(x)=p(pi*x^2) exp(-pi*x^2), exactly."""
    degree = len(p) - 1
    q = [Fraction(0) for _ in range(degree + 1)]
    factorials = [factorial(k) for k in range(2 * degree + 1)]
    for k, coefficient in enumerate(p):
        if coefficient == 0:
            continue
        for r in range(k + 1):
            factor = Fraction(
                (-1) ** r * factorials[2 * k] * 4**r,
                4**k * factorials[k - r] * factorials[2 * r],
            )
            q[r] += coefficient * factor
    return _trim(q)


def _sympy_poly(coefficients):
    x = sp.Symbol("t")
    return sp.Poly.from_list([sp.Rational(c.numerator, c.denominator)
                              for c in reversed(coefficients)], gens=x)


def _sign_on_interval(poly, left, right):
    if left == right:
        raise ValueError("Root isolating intervals cannot have empty gaps")
    sample = (left + right) / 2
    value = poly.eval(sp.Rational(sample.numerator, sample.denominator))
    if value == 0:
        raise ArithmeticError("Root isolation left a root inside a sign interval")
    return 1 if value > 0 else -1


def _last_negative_root(coefficients):
    """Return the rational isolating interval for the final negative-to-positive root."""
    if len(coefficients) < 2 or coefficients[0] >= 0:
        raise ValueError("The polynomial must have negative value at the origin and positive degree")
    if coefficients[-1] <= 0:
        raise ValueError("The polynomial must be positive for all sufficiently large t")

    poly = _sympy_poly(coefficients)
    root_intervals = poly.intervals(eps=_ROOT_EPS)
    positive = []
    for (left, right), _multiplicity in root_intervals:
        lo = Fraction(int(left.p), int(left.q))
        hi = Fraction(int(right.p), int(right.q))
        if hi <= 0:
            continue
        if lo <= 0:
            raise ArithmeticError("A root box crossed t=0 despite a nonzero constant")
        positive.append((lo, hi))

    if not positive:
        raise ValueError("No positive sign change was found")
    positive.sort()

    gap_signs = []
    previous = Fraction(0)
    for lo, hi in positive:
        if previous < lo:
            gap_signs.append(_sign_on_interval(poly, previous, lo))
        else:
            raise ArithmeticError("Positive root intervals overlap")
        previous = hi
    # A rational point to the right of every positive real root has the leading sign.
    tail_sample = previous + 1
    tail_value = poly.eval(sp.Rational(tail_sample.numerator, tail_sample.denominator))
    if tail_value == 0:
        tail_sample += 1
        tail_value = poly.eval(sp.Rational(tail_sample.numerator, tail_sample.denominator))
    gap_signs.append(1 if tail_value > 0 else -1)

    # Each root box separates consecutive root-free gaps. Pick the last root
    # whose left gap is negative and right gap is positive. This ignores even
    # multiplicity contacts, including contacts after the final crossing.
    crossing = None
    for i, (lo, hi) in enumerate(positive):
        if gap_signs[i] < 0 and gap_signs[i + 1] > 0:
            crossing = (lo, hi)
    if crossing is None:
        raise ValueError("The polynomial has no final negative-to-positive crossing")
    return crossing


def _atan_inverse_interval(q, terms):
    partial = sum((Fraction((-1) ** j, (2 * j + 1) * q ** (2 * j + 1))
                   for j in range(terms)), Fraction(0))
    next_term = Fraction((-1) ** terms, (2 * terms + 1) * q ** (2 * terms + 1))
    return min(partial, partial + next_term), max(partial, partial + next_term)


def _pi_interval():
    lo5, hi5 = _atan_inverse_interval(5, _PI_TERMS_5)
    lo239, hi239 = _atan_inverse_interval(239, _PI_TERMS_239)
    # Machin's identity: pi = 16 atan(1/5) - 4 atan(1/239).
    return 16 * lo5 - 4 * hi239, 16 * hi5 - 4 * lo239


def _sqrt_interval(value):
    """Rational enclosure of sqrt(value) with denominator _SCALE."""
    if value < 0:
        raise ValueError("A square-root argument must be nonnegative")
    scaled_num = value.numerator * _SCALE * _SCALE
    floor_value = isqrt(scaled_num // value.denominator)
    lower = Fraction(floor_value, _SCALE)
    if lower * lower == value:
        return lower, lower
    return lower, Fraction(floor_value + 1, _SCALE)


def _score_interval(p_root, q_root):
    p_lo, p_hi = p_root
    q_lo, q_hi = q_root
    pi_lo, pi_hi = _pi_interval()
    sqrt_lo, _ = _sqrt_interval(p_lo * q_lo)
    _, sqrt_hi = _sqrt_interval(p_hi * q_hi)
    return sqrt_lo / pi_hi, sqrt_hi / pi_lo


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("id") != CONFIG_ID:
        raise ValueError("Unknown T089 configuration")
    parameters = config.get("parameters")
    if (not isinstance(parameters, dict)
            or parameters.keys() != _EXPECTED_PARAMETERS.keys()
            or any(type(parameters[key]) is not type(expected)
                   or parameters[key] != expected
                   for key, expected in _EXPECTED_PARAMETERS.items())):
        raise ValueError("T089 parameters do not match the fixed configuration")
    if config.get("direction") != "minimize":
        raise ValueError("T089-C01 is a minimization configuration")
    if not isinstance(solution, dict):
        raise ValueError("Solution must be a JSON object")
    if "coefficients" not in solution or not isinstance(solution["coefficients"], list):
        raise ValueError("Solution must include ascending polynomial coefficients")
    p = _trim([_fraction(value) for value in solution["coefficients"]])
    if len(p) < 2:
        raise ValueError("A nonconstant polynomial is required")
    if p[0] >= 0:
        raise ValueError("f(0)=p(0) must be strictly negative")

    q = _fourier_polynomial(p)
    if q[0] >= 0:
        raise ValueError("fhat(0)=q(0) must be strictly negative")
    p_root = _last_negative_root(p)
    q_root = _last_negative_root(q)
    lower, upper = _score_interval(p_root, q_root)
    expression = (
        f"sqrt(root_p*root_q)/pi; root_p in [{p_root[0]},{p_root[1]}], "
        f"root_q in [{q_root[0]},{q_root[1]}]"
    )
    raw_interval = [str(lower), str(upper)]
    return {
        "objective": str(upper),
        "objective_value": str(upper),
        "verification_status": "certified",
        "details": {
            "fourier_coefficients_ascending": [str(v) for v in q],
            "last_negative_to_positive_root_p": [str(v) for v in p_root],
            "last_negative_to_positive_root_q": [str(v) for v in q_root],
            "objective_interval": raw_interval,
            "raw_product_interval": raw_interval,
            "raw_product_expression": expression,
            "objective_meaning": "conservative rational upper endpoint for A(f)*A(fhat); the interval encloses the raw product",
            "claimed_score_ignored": True,
        },
    }
