"""Small exact arithmetic helpers for Q[alpha] / (minimal polynomial)."""

from fractions import Fraction
import re


_RATIONAL_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")


def parse_rational(value, label):
    if type(value) is int:
        return Fraction(value)
    if not isinstance(value, str) or not _RATIONAL_RE.fullmatch(value):
        raise ValueError(f"{label} must be an integer or rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{label} is not a valid rational") from exc


def _trim(poly):
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out or [Fraction(0)]


def _poly_add(a, b):
    out = [Fraction(0)] * max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += value
    return _trim(out)


def _poly_sub(a, b):
    out = [Fraction(0)] * max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] -= value
    return _trim(out)


def _poly_mul(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i + j] += x * y
    return _trim(out)


def _poly_divmod(a, b):
    a = _trim(a)
    b = _trim(b)
    if b == [0]:
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [Fraction(0)] * max(1, len(a) - len(b) + 1)
    while a != [0] and len(a) >= len(b):
        offset = len(a) - len(b)
        factor = a[-1] / b[-1]
        quotient[offset] += factor
        for i, value in enumerate(b):
            a[offset + i] -= factor * value
        a = _trim(a)
    return _trim(quotient), a


def reduce_element(coefficients, modulus):
    degree = len(modulus) - 1
    work = list(coefficients) or [Fraction(0)]
    work += [Fraction(0)] * max(0, degree + 1 - len(work))
    for k in range(len(work) - 1, degree - 1, -1):
        lead = work[k]
        if lead:
            scale = lead / modulus[degree]
            offset = k - degree
            for j, coefficient in enumerate(modulus):
                work[offset + j] -= scale * coefficient
    return tuple((work + [Fraction(0)] * degree)[:degree])


def zero(degree):
    return tuple(Fraction(0) for _ in range(degree))


def one(degree):
    return tuple([Fraction(1)] + [Fraction(0)] * (degree - 1))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, b, modulus):
    degree = len(modulus) - 1
    product = [Fraction(0)] * (2 * degree - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    product[i + j] += x * y
    for k in range(len(product) - 1, degree - 1, -1):
        lead = product[k]
        if lead:
            scale = lead / modulus[degree]
            offset = k - degree
            for j, coefficient in enumerate(modulus):
                product[offset + j] -= scale * coefficient
    return tuple(product[:degree])


def inv(a, modulus):
    """Return the exact inverse of a nonzero field element."""
    if not any(a):
        raise ZeroDivisionError("zero has no inverse")
    r0, r1 = _trim(list(modulus)), _trim(list(a))
    s0, s1 = [Fraction(0)], [Fraction(1)]
    while r1 != [0]:
        quotient, remainder = _poly_divmod(r0, r1)
        r0, r1 = r1, remainder
        s0, s1 = s1, _poly_sub(s0, _poly_mul(quotient, s1))
    if len(r0) != 1:
        raise ValueError("the supplied modulus is not irreducible")
    return reduce_element([coefficient / r0[0] for coefficient in s0], modulus)


def div(a, b, modulus):
    return mul(a, inv(b, modulus), modulus)


def from_int(value, degree):
    return tuple([Fraction(value)] + [Fraction(0)] * (degree - 1))


def serialize_element(element):
    return [str(value) for value in element]
