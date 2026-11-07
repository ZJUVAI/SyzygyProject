"""Exact verifier for degree-100 primitive irreducible integer polynomials.

The candidate supplies rational complex root disks.  Each disk is certified by
Rouche's theorem using exact rational arithmetic; 100 disjoint disks account
for all roots.  The returned objective is a certified upper bound on Mahler
measure, which is conservative for this minimization task.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import gcd, isqrt
import sys
from typing import Any

CONFIG_ID = "T063-C01"
DEGREE = 100
PARAMETERS = {
    "degree": 100,
    "polynomial": "primitive_irreducible_integer",
    "domain": "Z[x]",
    "cyclotomic": "excluded",
    "objective": "Mahler_measure",
}
_SCALE = 10**30

# Rational root-disk data are proof inputs and may need arbitrary precision.
# The public runner limits candidate data to 16 MiB and the checker process to
# 4 GiB; Python's default decimal-to-int digit guard would impose an unrelated
# precision ceiling, so exact parsing is enabled here.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def _rat(value: Any, name: str) -> Fraction:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a rational string")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"invalid rational in {name}") from exc
    return result


def _complex_mul(a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _complex_eval(coefficients: list[int], z: tuple[Fraction, Fraction]):
    value = (Fraction(0), Fraction(0))
    derivative = (Fraction(0), Fraction(0))
    for coefficient in reversed(coefficients):
        derivative = _complex_mul(derivative, z)
        derivative = (derivative[0] + value[0], derivative[1] + value[1])
        value = _complex_mul(value, z)
        value = (value[0] + coefficient, value[1])
    return value, derivative


def _sqrt_bounds(value: Fraction) -> tuple[Fraction, Fraction]:
    """Return rational lower and upper bounds for sqrt(value)."""
    if value < 0:
        raise ValueError("negative squared modulus")
    scaled_floor = isqrt((value.numerator * _SCALE * _SCALE) // value.denominator)
    lower = Fraction(scaled_floor, _SCALE)
    if lower * lower == value:
        return lower, lower
    return lower, Fraction(scaled_floor + 1, _SCALE)


def _complex_bounds(z: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return _sqrt_bounds(z[0] * z[0] + z[1] * z[1])


def _parse_disk(raw: Any, index: int):
    if not isinstance(raw, Mapping):
        raise ValueError(f"root disk {index} must be an object")
    real = _rat(raw.get("center_real"), f"root_disks[{index}].center_real")
    imag = _rat(raw.get("center_imag"), f"root_disks[{index}].center_imag")
    radius = _rat(raw.get("radius"), f"root_disks[{index}].radius")
    if radius <= 0:
        raise ValueError(f"root disk {index} must have positive radius")
    return (real, imag), radius


def validate(solution: Any, config: Mapping[str, Any], strict: bool = False) -> dict[str, Any]:
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError("unsupported configuration id")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration parameters do not match T063-C01")
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")

    coefficients = solution.get("coefficients_ascending")
    if not isinstance(coefficients, (list, tuple)) or len(coefficients) != DEGREE + 1:
        raise ValueError("coefficients_ascending must contain exactly 101 integers")
    if any(type(value) is not int for value in coefficients):
        raise ValueError("coefficients must be integers; bool and floats are rejected")
    if coefficients[-1] == 0:
        raise ValueError("polynomial must have exact degree 100")
    content = 0
    for coefficient in coefficients:
        content = gcd(content, abs(coefficient))
    if content != 1:
        raise ValueError("polynomial must be primitive")

    # Exact factorization over Q for the fixed degree. Runtime and memory are
    # subject to the shared runner limits.
    from sympy import Poly, symbols

    x = symbols("x")
    polynomial = Poly.from_list(list(reversed(coefficients)), x)
    if not polynomial.is_irreducible:
        raise ValueError("polynomial must be irreducible over Q")

    raw_disks = solution.get("root_disks")
    if not isinstance(raw_disks, (list, tuple)) or len(raw_disks) != DEGREE:
        raise ValueError("exactly 100 root disks are required")
    disks = [_parse_disk(raw, i) for i, raw in enumerate(raw_disks)]

    # Pairwise disjointness: disjoint coordinate projections suffice.  This
    # is intentionally a conservative exact test.
    disjoint_checks = 0
    for i, (left, left_radius) in enumerate(disks):
        for right, right_radius in disks[:i]:
            disjoint_checks += 1
            if max(abs(left[0] - right[0]), abs(left[1] - right[1])) <= left_radius + right_radius:
                raise ValueError("root disks are not certified pairwise disjoint")

    lower_measure = Fraction(abs(coefficients[-1]))
    upper_measure = Fraction(abs(coefficients[-1]))
    rouche_checks = 0
    outside_count_lower = 0
    for index, (center, radius) in enumerate(disks):
        value, derivative = _complex_eval(coefficients, center)
        # |p'(c)| >= max(|Re p'(c)|, |Im p'(c)|), while |p(c)| is at
        # most |Re p(c)|+|Im p(c)|.
        derivative_lower = max(abs(derivative[0]), abs(derivative[1]))
        value_upper = abs(value[0]) + abs(value[1])
        center_lower, center_upper = _complex_bounds(center)
        disk_radius_upper = center_upper + radius
        remainder = Fraction(0)
        power = Fraction(1)
        for k in range(2, DEGREE + 1):
            if k > 2:
                power *= disk_radius_upper
            remainder += Fraction(k * (k - 1) * abs(coefficients[k]), 2) * radius * radius * power
        if radius * derivative_lower <= value_upper + remainder:
            raise ValueError(f"root disk {index} fails the exact Rouche certificate")
        rouche_checks += 1

        root_lower = max(Fraction(0), center_lower - radius)
        root_upper = center_upper + radius
        lower_measure *= max(Fraction(1), root_lower)
        upper_measure *= max(Fraction(1), root_upper)
        if root_lower > 1:
            outside_count_lower += 1

    # All 100 disks contain one root by Rouché and are pairwise disjoint.
    # Their count equals the degree, so these bounds cover the full root set.
    if lower_measure <= 1:
        raise ValueError("the certificate does not establish a noncyclotomic polynomial")
    if (upper_measure - lower_measure) * 10**10 > lower_measure:
        raise ValueError("Mahler measure interval is wider than the required relative 1e-10")

    return {
        "objective": str(upper_measure),
        "objective_value": str(upper_measure),
        "verification_status": "certified",
        "details": {
            "degree": DEGREE,
            "primitive": True,
            "irreducible_over_Q": True,
            "root_disks_checked": rouche_checks,
            "pairwise_disjoint_checks": disjoint_checks,
            "outside_unit_circle_roots_certified": outside_count_lower,
            "objective_interval": [str(lower_measure), str(upper_measure)],
            "relative_interval_width_at_most": "1/10000000000",
            "claimed_objective_ignored": True,
        },
    }
