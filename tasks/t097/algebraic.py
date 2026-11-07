"""Exact arithmetic in a single real algebraic number field."""
from fractions import Fraction
from functools import lru_cache

import sympy as sp


def integer_text(value):
    if type(value) is int:
        return value
    if not isinstance(value, str) or not value or not value.isascii():
        raise ValueError("integer values must be ASCII integer strings")
    sign = -1 if value.startswith("-") else 1
    digits = value[1:] if value[:1] in "+-" else value
    if not digits or not digits.isdigit():
        raise ValueError("invalid integer string")
    width = len(digits) % 9 or 9
    out = int(digits[:width])
    for i in range(width, len(digits), 9):
        out = out * 10**9 + int(digits[i:i + 9])
    return sign * out


def rational(value):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, bool) or not isinstance(value, str) or value.count("/") > 1:
        raise ValueError("field coefficients must be exact rational strings or integers")
    if "/" not in value:
        return Fraction(integer_text(value))
    n, d = value.split("/")
    denominator = integer_text(d)
    if denominator == 0:
        raise ValueError("zero rational denominator")
    return Fraction(integer_text(n), denominator)


def _trim(poly):
    values = list(poly)
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def _add(a, b):
    return _trim([((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0))
                  for i in range(max(len(a), len(b)))])


def _sub(a, b):
    return _trim([((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0))
                  for i in range(max(len(a), len(b)))])


def _mul(a, b):
    if not a or not b:
        return ()
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return _trim(out)


def _divmod(a, b):
    if not b:
        raise ZeroDivisionError
    rem = list(a)
    quotient = [Fraction(0)] * max(0, len(a) - len(b) + 1)
    while rem and len(rem) >= len(b):
        shift = len(rem) - len(b)
        factor = rem[-1] / b[-1]
        quotient[shift] = factor
        for i, value in enumerate(b):
            rem[shift + i] -= factor * value
        while rem and rem[-1] == 0:
            rem.pop()
    return _trim(quotient), _trim(rem)


def _xgcd(a, b):
    old_r, r = a, b
    old_s, s = (Fraction(1),), ()
    old_t, t = (), (Fraction(1),)
    while r:
        q, rem = _divmod(old_r, r)
        old_r, r = r, rem
        old_s, s = s, _sub(old_s, _mul(q, s))
        old_t, t = t, _sub(old_t, _mul(q, t))
    if not old_r:
        return (), (), ()
    scale = old_r[-1]
    return tuple(c / scale for c in old_r), tuple(c / scale for c in old_s), tuple(c / scale for c in old_t)


def _interval_mul(a, b):
    products = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(products), max(products)


def _interval_eval(poly, interval):
    result = (Fraction(0), Fraction(0))
    for coefficient in reversed(poly):
        lo, hi = _interval_mul(result, interval)
        result = (lo + coefficient, hi + coefficient)
    return result


class RealAlgebraicField:
    def __init__(self, descriptor):
        if not isinstance(descriptor, dict) or set(descriptor) != {"minimal_polynomial", "isolating_interval"}:
            raise ValueError("algebraic_field must contain minimal_polynomial and isolating_interval")
        raw = descriptor["minimal_polynomial"]
        if not isinstance(raw, list) or len(raw) < 2:
            raise ValueError("minimal polynomial must have positive degree")
        coefficients = tuple(Fraction(integer_text(c)) for c in raw)
        if coefficients[-1] <= 0:
            raise ValueError("minimal polynomial must have positive leading coefficient")
        if any(c.denominator != 1 for c in coefficients):
            raise ValueError("minimal polynomial coefficients must be integers")
        import math
        gcd = 0
        for c in coefficients:
            gcd = math.gcd(gcd, abs(c.numerator))
        if gcd != 1:
            raise ValueError("minimal polynomial must be primitive")
        self.modulus = tuple(c / coefficients[-1] for c in coefficients)
        sym_x = sp.Symbol("alpha")
        self.sym_poly = sp.Poly(sum(sp.Rational(c.numerator, c.denominator) * sym_x**i
                                    for i, c in enumerate(self.modulus)), sym_x, domain=sp.QQ)
        if not self.sym_poly.is_irreducible:
            raise ValueError("minimal polynomial must be irreducible over Q")
        interval = descriptor["isolating_interval"]
        if not isinstance(interval, list) or len(interval) != 2:
            raise ValueError("isolating_interval must have two rational endpoints")
        self.lo, self.hi = rational(interval[0]), rational(interval[1])
        if self.lo >= self.hi:
            raise ValueError("isolating interval must have positive width")
        self.sturm = self.sym_poly.sturm()
        if self._poly_sign_at(self.sym_poly, self.lo) == 0 or self._poly_sign_at(self.sym_poly, self.hi) == 0:
            raise ValueError("isolating interval endpoints cannot be roots")
        if self._variations(self.lo) - self._variations(self.hi) != 1:
            raise ValueError("isolating interval must contain exactly one real root")
        self.degree = len(self.modulus) - 1
        self._sign_cache = {}

    @staticmethod
    def _poly_sign_at(poly, x):
        value = poly.eval(sp.Rational(x.numerator, x.denominator))
        return int(bool(value > 0)) - int(bool(value < 0))

    def _variations(self, x):
        signs = [self._poly_sign_at(poly, x) for poly in self.sturm]
        signs = [s for s in signs if s]
        return sum(a != b for a, b in zip(signs, signs[1:]))

    def reduce(self, poly):
        poly = _trim(poly)
        if not poly:
            return ()
        return _divmod(poly, self.modulus)[1]

    def element(self, raw):
        if not isinstance(raw, list) or not raw:
            raise ValueError("coordinates must be nonempty rational-polynomial coefficient lists")
        return self.reduce(tuple(rational(c) for c in raw))

    def const(self, value):
        return self.reduce((Fraction(value),)) if value else ()

    def add(self, a, b):
        return self.reduce(_add(a, b))

    def sub(self, a, b):
        return self.reduce(_sub(a, b))

    def neg(self, a):
        return self.reduce(tuple(-c for c in a))

    def mul(self, a, b):
        return self.reduce(_mul(a, b))

    def inv(self, a):
        if not a:
            raise ZeroDivisionError("division by zero algebraic number")
        gcd, s, _ = _xgcd(a, self.modulus)
        if len(gcd) != 1:
            raise ZeroDivisionError("noninvertible field element")
        return self.reduce(tuple(c / gcd[0] for c in s))

    def div(self, a, b):
        return self.mul(a, self.inv(b))

    def sign(self, value):
        value = self.reduce(value)
        if not value:
            return 0
        if value in self._sign_cache:
            return self._sign_cache[value]
        if self.degree == 1:
            root = -self.modulus[0]
            result = 0
            for c in reversed(value):
                result = result * root + c
            sign = (result > 0) - (result < 0)
            self._sign_cache[value] = sign
            return sign
        while True:
            lo, hi = _interval_eval(value, (self.lo, self.hi))
            if lo > 0:
                self._sign_cache[value] = 1
                return 1
            if hi < 0:
                self._sign_cache[value] = -1
                return -1
            mid = (self.lo + self.hi) / 2
            if self._variations(self.lo) - self._variations(mid) == 1:
                self.hi = mid
            else:
                self.lo = mid

    def compare(self, a, b):
        return self.sign(self.sub(a, b))


def output_rational(value):
    n, d = value.numerator, value.denominator
    return str(n) if d == 1 else f"{n}/{d}"
