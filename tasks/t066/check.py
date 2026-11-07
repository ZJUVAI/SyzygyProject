"""Exact checker for 3-rich lines among 17 planar real algebraic points."""

from fractions import Fraction
from functools import lru_cache, reduce
from math import gcd
import re
import sys

import sympy as sp

from tasks.t066.algebra import add, mul, parse_rational, reduce_element, sub, zero, inv


POINT_COUNT = 17
CONFIG_ID = "T066-C01"
PARAMETERS = {
    "point_count": POINT_COUNT,
    "ambient_space": "Euclidean plane R^2",
    "coordinate_domain": "real algebraic coordinates in a common real algebraic number field",
    "objective": "number of distinct lines containing exactly 3 input points",
}
_INTEGER_RE = re.compile(r"-?(?:0|[1-9][0-9]*)\Z")

if hasattr(sys, "set_int_max_str_digits"):
    # The shared output-size and process limits bound candidate input size.
    # Do not impose an additional arbitrary precision ceiling on exact data.
    sys.set_int_max_str_digits(0)


def _integer(value, label):
    if type(value) is int:
        return value
    if isinstance(value, str) and _INTEGER_RE.fullmatch(value):
        return int(value)
    raise ValueError(f"{label} must be an integer or integer string")


def _check_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    if config.get("id") not in (None, CONFIG_ID):
        raise ValueError(f"unsupported configuration: expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must describe exactly 17 real algebraic planar points")


@lru_cache(maxsize=32)
def _validate_field(raw_polynomial, raw_interval):
    if not isinstance(raw_polynomial, tuple) or len(raw_polynomial) < 2:
        raise ValueError("minimal_polynomial must be a nonconstant integer coefficient array")
    if any(type(c) is not int for c in raw_polynomial):
        raise ValueError("minimal_polynomial coefficients must be JSON integers")
    if raw_polynomial[-1] <= 0 or reduce(gcd, (abs(c) for c in raw_polynomial), 0) != 1:
        raise ValueError("minimal_polynomial must be primitive with positive leading coefficient")
    x = sp.Symbol("x")
    poly = sp.Poly.from_list(list(reversed(raw_polynomial)), gens=x, domain=sp.QQ)
    try:
        if not poly.is_irreducible:
            raise ValueError("minimal_polynomial must be irreducible over Q")
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("could not certify minimal_polynomial irreducibility") from exc
    if not isinstance(raw_interval, tuple) or len(raw_interval) != 2:
        raise ValueError("isolating_interval must contain two rational endpoints")
    left = parse_rational(raw_interval[0], "left interval endpoint")
    right = parse_rational(raw_interval[1], "right interval endpoint")
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
    return tuple(Fraction(c) for c in raw_polynomial), len(raw_polynomial) - 1


def _read_field(solution):
    raw_poly = solution.get("minimal_polynomial")
    raw_interval = solution.get("isolating_interval")
    if not isinstance(raw_poly, list) or not isinstance(raw_interval, list):
        raise ValueError("minimal_polynomial and isolating_interval are required arrays")
    polynomial = tuple(_integer(coefficient, "minimal_polynomial coefficient") for coefficient in raw_poly)
    if any(type(endpoint) not in (int, str) for endpoint in raw_interval):
        raise ValueError("isolating_interval endpoints must be rational integers or strings")
    modulus, degree = _validate_field(polynomial, tuple(raw_interval))
    return modulus, degree


def _parse_points(solution, modulus, degree):
    raw_points = solution.get("points")
    if not isinstance(raw_points, list) or len(raw_points) != POINT_COUNT:
        raise ValueError(f"points must contain exactly {POINT_COUNT} entries")
    points = []
    for i, point in enumerate(raw_points):
        if not isinstance(point, dict) or set(point) != {"x", "y"}:
            raise ValueError(f"point {i} must contain exactly x and y coordinate polynomials")
        coordinates = []
        for axis in ("x", "y"):
            raw = point[axis]
            if not isinstance(raw, list) or not raw:
                raise ValueError(f"point {i} {axis} must be a nonempty rational coefficient array")
            coeffs = [parse_rational(c, f"point {i} {axis} coefficient") for c in raw]
            coordinates.append(reduce_element(coeffs, modulus))
        points.append((coordinates[0], coordinates[1]))
    if len(set(points)) != POINT_COUNT:
        raise ValueError("all 17 points must be distinct in the selected real embedding")
    return points


def _line_from_pair(first, second, modulus, degree):
    x1, y1 = first
    x2, y2 = second
    a = sub(y1, y2)
    b = sub(x2, x1)
    c = sub(mul(x1, y2, modulus), mul(x2, y1, modulus))
    if not any(a) and not any(b):
        raise ValueError("duplicate points do not define a line")
    pivot = a if any(a) else b
    scale = inv(pivot, modulus)
    return tuple(mul(coefficient, scale, modulus) for coefficient in (a, b, c))


def _line_contains(line, point, modulus, zero_element):
    a, b, c = line
    x, y = point
    value = add(add(mul(a, x, modulus), mul(b, y, modulus)), c)
    return value == zero_element


def validate(solution, config, strict=False):
    """Count distinct geometric lines incident with exactly three input points."""
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    modulus, degree = _read_field(solution)
    points = _parse_points(solution, modulus, degree)
    lines = {}
    for i in range(POINT_COUNT):
        for j in range(i):
            line = _line_from_pair(points[i], points[j], modulus, degree)
            lines[line] = None

    zero_element = zero(degree)
    exactly_three = 0
    incidence_sizes = []
    for line in lines:
        count = sum(_line_contains(line, point, modulus, zero_element) for point in points)
        incidence_sizes.append(count)
        if count == 3:
            exactly_three += 1

    return {
        "objective": exactly_three,
        "verification_status": "exact",
        "details": {
            "point_count": POINT_COUNT,
            "distinct_lines_checked": len(lines),
            "exactly_three_point_lines": exactly_three,
            "largest_line_incidence": max(incidence_sizes),
            "coordinate_field_degree": degree,
            "minimal_polynomial_irreducible": True,
            "real_root_isolated_by_sturm_count": 1,
            "claimed_objective_ignored": True,
        },
    }
