"""Exact unit-distance counter over one real algebraic number field."""

from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction
from functools import reduce
from math import gcd
import re
import sys

import sympy as sp


POINT_COUNT = 100
CONFIG_ID = "T065-C01"
PARAMETERS = {
    "point_count": 100,
    "ambient_space": "Euclidean plane R^2",
    "objective": "unit_distance_pairs",
    "coordinate_domain": "real algebraic coordinates in one common number field",
}
_INTEGER_RE = re.compile(r"-?(?:0|[1-9][0-9]*)\Z")
_RATIONAL_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")

if hasattr(sys, "set_int_max_str_digits"):
    # Exact polynomial and rational inputs are bounded by the shared runner's
    # 16 MiB output limit and 4 GiB checker process limit.
    sys.set_int_max_str_digits(0)


def _integer(value, label):
    if type(value) is int:
        return value
    if isinstance(value, str) and _INTEGER_RE.fullmatch(value):
        return int(value)
    raise ValueError(f"{label} must be an integer or an integer string")


def _rational(value, label):
    if type(value) is int:
        return Fraction(value)
    if not isinstance(value, str) or not _RATIONAL_RE.fullmatch(value):
        raise ValueError(f"{label} must be an integer or rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{label} is not a valid rational") from exc


def _check_config(config):
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix 100 distinct points in R^2")


def _read_field(solution):
    raw = solution.get("minimal_polynomial")
    if not isinstance(raw, (list, tuple)) or len(raw) < 2:
        raise ValueError("minimal_polynomial must be a nonconstant coefficient array")
    coefficients = [_integer(c, "minimal_polynomial coefficient") for c in raw]
    if coefficients[-1] <= 0 or reduce(gcd, (abs(c) for c in coefficients), 0) != 1:
        raise ValueError("minimal_polynomial must be primitive with positive leading coefficient")

    x = sp.Symbol("x")
    polynomial = sp.Poly.from_list(list(reversed(coefficients)), gens=x, domain=sp.QQ)
    try:
        irreducible = polynomial.is_irreducible
    except Exception as exc:
        raise ValueError("could not certify minimal_polynomial irreducibility") from exc
    if not irreducible:
        raise ValueError("minimal_polynomial must be irreducible over Q")

    interval = solution.get("isolating_interval")
    if not isinstance(interval, (list, tuple)) or len(interval) != 2:
        raise ValueError("isolating_interval must contain two rational endpoints")
    left = _rational(interval[0], "left isolating endpoint")
    right = _rational(interval[1], "right isolating endpoint")
    if left >= right:
        raise ValueError("isolating_interval endpoints must be increasing")
    left_sym = sp.Rational(left.numerator, left.denominator)
    right_sym = sp.Rational(right.numerator, right.denominator)
    if polynomial.eval(left_sym) == 0 or polynomial.eval(right_sym) == 0:
        raise ValueError("isolating interval endpoints cannot be roots")
    try:
        root_count = polynomial.count_roots(left_sym, right_sym)
    except Exception as exc:
        raise ValueError("could not certify the real-root isolating interval") from exc
    if root_count != 1:
        raise ValueError("isolating_interval must contain exactly one real root")

    modulus = tuple(Fraction(c) for c in coefficients)
    return modulus, len(coefficients) - 1


def _reduce_polynomial(coefficients, modulus):
    degree = len(modulus) - 1
    work = list(coefficients) or [Fraction(0)]
    if len(work) < degree + 1:
        work.extend([Fraction(0)] * (degree + 1 - len(work)))
    for k in range(len(work) - 1, degree - 1, -1):
        leading = work[k]
        if leading:
            offset = k - degree
            scale = leading / modulus[degree]
            for j, coefficient in enumerate(modulus):
                work[offset + j] -= scale * coefficient
    return tuple((work + [Fraction(0)] * degree)[:degree])


def _parse_coordinates(solution, modulus, degree):
    raw_points = solution.get("points")
    if not isinstance(raw_points, (list, tuple)) or len(raw_points) != POINT_COUNT:
        raise ValueError(f"points must contain exactly {POINT_COUNT} entries")
    points = []
    for index, raw_point in enumerate(raw_points):
        if not isinstance(raw_point, Mapping) or set(raw_point) != {"x", "y"}:
            raise ValueError(f"point {index} must contain exactly x and y coordinates")
        parsed = []
        for axis in ("x", "y"):
            raw_coefficients = raw_point[axis]
            if not isinstance(raw_coefficients, (list, tuple)) or not raw_coefficients:
                raise ValueError(f"point {index} {axis} must be a nonempty rational coefficient array")
            coefficients = [
                _rational(value, f"point {index} {axis} coefficient")
                for value in raw_coefficients
            ]
            parsed.append(_reduce_polynomial(coefficients, modulus))
        points.append((parsed[0], parsed[1]))
    if len(set(points)) != POINT_COUNT:
        raise ValueError("all 100 points must be distinct in the selected real embedding")
    return points


def _add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def _subtract(left, right):
    return tuple(a - b for a, b in zip(left, right))


def _multiply_mod(left, right, modulus):
    degree = len(modulus) - 1
    work = [Fraction(0)] * (2 * degree - 1)
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    work[i + j] += a * b
    return _reduce_polynomial(work, modulus)


def validate(solution, config, strict=False):
    """Count all exact unit-distance pairs; candidate score fields are ignored."""
    _check_config(config)
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    modulus, degree = _read_field(solution)
    points = _parse_coordinates(solution, modulus, degree)

    one = (Fraction(1),) + (Fraction(0),) * (degree - 1)
    unit_pairs = 0
    pair_count = 0
    for i, (xi, yi) in enumerate(points):
        for xj, yj in points[:i]:
            dx = _subtract(xi, xj)
            dy = _subtract(yi, yj)
            squared_distance = _add(
                _multiply_mod(dx, dx, modulus),
                _multiply_mod(dy, dy, modulus),
            )
            if squared_distance == one:
                unit_pairs += 1
            pair_count += 1

    return {
        "objective": unit_pairs,
        "verification_status": "exact",
        "details": {
            "point_count": POINT_COUNT,
            "unordered_pairs_checked": pair_count,
            "unit_distance_pairs": unit_pairs,
            "coordinate_field_degree": degree,
            "minimal_polynomial_irreducible": True,
            "selected_real_root_count": 1,
            "claimed_objective_ignored": True,
            "strict": bool(strict),
        },
    }
