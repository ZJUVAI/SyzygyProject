"""Exact checker for minimum spherical 5-designs in S^3."""

from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction
from functools import reduce
from itertools import product
from math import gcd
import re
import sys

import sympy as sp


CONFIG_ID = "T073-C01"
DIMENSION = 3
AMBIENT_DIMENSION = 4
STRENGTH = 5
PARAMETERS = {
    "sphere": "S^3 subset R^4 unit sphere",
    "design_strength": 5,
    "weights": "equal positive weights",
    "objective": "number of distinct points",
    "coordinate_domain": "real algebraic coordinates in one common real algebraic number field",
}
_INTEGER_RE = re.compile(r"-?(?:0|[1-9][0-9]*)\Z")
_RATIONAL_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def _integer(value, label):
    if type(value) is int:
        return value
    if isinstance(value, str) and _INTEGER_RE.fullmatch(value):
        return int(value)
    raise ValueError(f"{label} must be an integer or integer string")


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
        raise ValueError("configuration must fix an equal-weight 5-design on the unit sphere S^3")


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
        if not polynomial.is_irreducible:
            raise ValueError("minimal_polynomial must be irreducible over Q")
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("could not certify minimal_polynomial irreducibility") from exc

    interval = solution.get("isolating_interval")
    if not isinstance(interval, (list, tuple)) or len(interval) != 2:
        raise ValueError("isolating_interval must contain two rational endpoints")
    left, right = (_rational(interval[i], "isolating endpoint") for i in range(2))
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
    return tuple(Fraction(c) for c in coefficients), len(coefficients) - 1


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


def _multiply_mod(left, right, modulus):
    degree = len(modulus) - 1
    work = [Fraction(0)] * (2 * degree - 1)
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    work[i + j] += a * b
    return _reduce_polynomial(work, modulus)


def _add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def _monomials():
    return [powers for powers in product(range(STRENGTH + 1), repeat=AMBIENT_DIMENSION)
            if sum(powers) <= STRENGTH]


def _sphere_moment(exponents):
    if any(power % 2 for power in exponents):
        return Fraction(0)
    half = [power // 2 for power in exponents]
    total = sum(half)
    numerator = 1
    for value in half:
        for k in range(1, value + 1):
            numerator *= 2 * k - 1
    denominator = 1
    for k in range(total):
        denominator *= AMBIENT_DIMENSION + 2 * k
    return Fraction(numerator, denominator)


def _parse_points(solution, modulus, degree):
    raw_points = solution.get("points")
    if not isinstance(raw_points, (list, tuple)) or not raw_points:
        raise ValueError("points must be a nonempty list of 4D points")
    points = []
    for index, raw_point in enumerate(raw_points):
        if not isinstance(raw_point, (list, tuple)) or len(raw_point) != AMBIENT_DIMENSION:
            raise ValueError(f"point {index} must contain exactly four coordinates")
        coordinates = []
        for axis, raw_coefficients in enumerate(raw_point):
            if not isinstance(raw_coefficients, (list, tuple)) or not raw_coefficients:
                raise ValueError(f"point {index} coordinate {axis} must be a nonempty coefficient array")
            coefficients = [_rational(value, f"point {index} coordinate {axis} coefficient")
                            for value in raw_coefficients]
            coordinates.append(_reduce_polynomial(coefficients, modulus))
        points.append(tuple(coordinates))
    if len(set(points)) != len(points):
        raise ValueError("all sphere points must be distinct")
    return points


def validate(solution, config, strict=False):
    """Verify unit norms and all equal-weight moments through total degree five."""
    del strict
    _check_config(config)
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    modulus, degree = _read_field(solution)
    points = _parse_points(solution, modulus, degree)
    zero = (Fraction(0),) * degree
    one = (Fraction(1),) + (Fraction(0),) * (degree - 1)

    point_powers = []
    for index, point in enumerate(points):
        norm = zero
        powers_by_axis = []
        for coordinate in point:
            norm = _add(norm, _multiply_mod(coordinate, coordinate, modulus))
            powers = [one]
            for _ in range(STRENGTH):
                powers.append(_multiply_mod(powers[-1], coordinate, modulus))
            powers_by_axis.append(powers)
        if norm != one:
            raise ValueError(f"point {index} is not on the unit sphere")
        point_powers.append(powers_by_axis)

    checked_monomials = 0
    for exponents in _monomials():
        total = zero
        for powers_by_axis in point_powers:
            term = one
            for axis, power in enumerate(exponents):
                if power:
                    term = _multiply_mod(term, powers_by_axis[axis][power], modulus)
            total = _add(total, term)
        expected = len(points) * _sphere_moment(exponents)
        target = (expected,) + (Fraction(0),) * (degree - 1)
        if total != target:
            raise ValueError(f"spherical moment mismatch for monomial exponents {exponents}")
        checked_monomials += 1

    return {
        "objective": len(points),
        "verification_status": "exact",
        "details": {
            "dimension": DIMENSION,
            "ambient_dimension": AMBIENT_DIMENSION,
            "design_strength": STRENGTH,
            "point_count": len(points),
            "unit_norms_verified": len(points),
            "monomials_checked": checked_monomials,
            "coordinate_field_degree": degree,
            "minimal_polynomial_irreducible": True,
            "selected_real_root_count": 1,
            "claimed_objective_ignored": True,
        },
    }
