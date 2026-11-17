"""Exact arithmetic for algebraic and planar coordinates."""
from fractions import Fraction
import re


_RATIONAL_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")


def rational(value, label):
    if type(value) is int:
        return Fraction(value)
    if not isinstance(value, str) or not _RATIONAL_RE.fullmatch(value):
        raise ValueError(f"{label} must be an integer or rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{label} is not a valid rational") from exc


def reduce_polynomial(coefficients, modulus):
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


def multiply_mod(left, right, modulus):
    degree = len(modulus) - 1
    work = [Fraction(0)] * (2 * degree - 1)
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    work[i + j] += a * b
    return reduce_polynomial(work, modulus)


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def on_segment(a, b, p):
    return (cross(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))
