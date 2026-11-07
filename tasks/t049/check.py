"""Exact distinct-distance checker over a common real algebraic number field."""

from __future__ import annotations

from fractions import Fraction
from functools import reduce
from math import gcd
import re

import sympy as sp


POINT_COUNT = 91
CONFIG_ID = "T049-C01"
_RATIONAL_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")


def _parse_rational(value, label):
    if type(value) is int:
        return Fraction(value)
    if not isinstance(value, str) or not _RATIONAL_RE.fullmatch(value):
        raise ValueError(f"{label} must be an integer or a rational string such as '-3/2'")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{label} is not a valid rational") from exc


def _check_config(config):
    expected = {
        "point_count": POINT_COUNT,
        "ambient_space": "Euclidean plane R^2",
        "coordinate_domain": "real algebraic coordinates in a common real algebraic number field",
    }
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    if config.get("id") not in (None, CONFIG_ID):
        raise ValueError(f"unsupported configuration: expected {CONFIG_ID}")
    if config.get("parameters") != expected:
        raise ValueError("configuration must fix exactly 91 distinct points in R^2")


def _element_reduce(coeffs, modulus):
    """Reduce a rational polynomial modulo the primitive minimal polynomial."""
    degree = len(modulus) - 1
    work = list(coeffs) or [Fraction(0)]
    work += [Fraction(0)] * max(0, degree + 1 - len(work))
    for k in range(len(work) - 1, degree - 1, -1):
        lead = work[k]
        if lead:
            scale = lead / modulus[degree]
            offset = k - degree
            for j, coefficient in enumerate(modulus):
                work[offset + j] -= scale * coefficient
    return tuple((work + [Fraction(0)] * degree)[:degree])


def _add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _mul_mod(a, b, modulus):
    degree = len(modulus) - 1
    work = [Fraction(0)] * (2 * degree - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    work[i + j] += x * y
    for k in range(len(work) - 1, degree - 1, -1):
        lead = work[k]
        if lead:
            scale = lead / modulus[degree]
            offset = k - degree
            for j, coefficient in enumerate(modulus):
                work[offset + j] -= scale * coefficient
    return tuple(work[:degree])


def _read_field(solution):
    raw = solution.get("minimal_polynomial")
    if not isinstance(raw, list) or len(raw) < 2:
        raise ValueError("minimal_polynomial must be a nonconstant integer coefficient array")
    if any(type(c) is not int for c in raw):
        raise ValueError("minimal_polynomial coefficients must be JSON integers")
    if raw[-1] <= 0 or reduce(gcd, (abs(c) for c in raw), 0) != 1:
        raise ValueError("minimal_polynomial must be primitive with positive leading coefficient")
    if raw[-1] == 0:
        raise ValueError("minimal_polynomial must have its leading coefficient last")
    x = sp.Symbol("x")
    poly = sp.Poly.from_list(list(reversed(raw)), gens=x, domain=sp.QQ)
    try:
        irreducible = poly.is_irreducible
    except Exception as exc:
        raise ValueError("could not certify minimal_polynomial irreducibility") from exc
    if not irreducible:
        raise ValueError("minimal_polynomial must be irreducible over Q")
    interval = solution.get("isolating_interval")
    if not isinstance(interval, list) or len(interval) != 2:
        raise ValueError("isolating_interval must contain two rational endpoints")
    left = _parse_rational(interval[0], "left interval endpoint")
    right = _parse_rational(interval[1], "right interval endpoint")
    if left >= right:
        raise ValueError("isolating_interval endpoints must be increasing")
    left_sym = sp.Rational(left.numerator, left.denominator)
    right_sym = sp.Rational(right.numerator, right.denominator)
    if poly.eval(left_sym) == 0 or poly.eval(right_sym) == 0:
        raise ValueError("isolating interval endpoints cannot be roots")
    try:
        root_count = poly.count_roots(left_sym, right_sym)
    except Exception as exc:
        raise ValueError("could not certify the isolating interval") from exc
    if root_count != 1:
        raise ValueError("isolating_interval must contain exactly one real root (Sturm count)")
    return tuple(Fraction(c) for c in raw), len(raw) - 1


def _parse_coordinates(solution, modulus, degree):
    points = solution.get("points")
    if not isinstance(points, list) or len(points) != POINT_COUNT:
        raise ValueError(f"points must contain exactly {POINT_COUNT} entries")
    parsed = []
    for i, point in enumerate(points):
        if not isinstance(point, dict) or set(point) != {"x", "y"}:
            raise ValueError(f"point {i} must contain exactly x and y coordinate polynomials")
        coordinates = []
        for axis in ("x", "y"):
            raw = point[axis]
            if not isinstance(raw, list) or not raw:
                raise ValueError(f"point {i} {axis} must be a nonempty rational coefficient array")
            if len(raw) > 1_000_000:
                raise ValueError("coordinate polynomial is too large")
            coefficients = [_parse_rational(c, f"point {i} {axis} coefficient") for c in raw]
            coordinates.append(_element_reduce(coefficients, modulus))
        parsed.append((coordinates[0], coordinates[1]))
    if len(set(parsed)) != POINT_COUNT:
        raise ValueError("all 91 points must be distinct in the selected real embedding")
    return parsed


def validate(solution, config, strict=False):
    """Count distinct positive distances exactly; candidate score fields are ignored."""
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    modulus, degree = _read_field(solution)
    points = _parse_coordinates(solution, modulus, degree)
    zero = tuple(Fraction(0) for _ in range(degree))
    squared_distances = set()
    pair_count = 0
    for i in range(POINT_COUNT):
        xi, yi = points[i]
        for j in range(i):
            xj, yj = points[j]
            dx = _sub(xi, xj)
            dy = _sub(yi, yj)
            squared = _add(_mul_mod(dx, dx, modulus), _mul_mod(dy, dy, modulus))
            if squared == zero:
                raise ValueError("distinct point entries must have positive pairwise distance")
            squared_distances.add(squared)
            pair_count += 1
    objective = len(squared_distances)
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "point_count": POINT_COUNT,
            "unordered_pair_count": pair_count,
            "distinct_positive_distances": objective,
            "coordinate_field_degree": degree,
            "minimal_polynomial_irreducible": True,
            "real_root_isolated_by_sturm_count": 1,
            "claimed_objective_ignored": True,
        },
    }
