"""Exact sphere-moment checker for degree-20 real spherical harmonics."""
from fractions import Fraction
from itertools import product

DEGREE = 20
PARAMETERS = {"degree": 20, "domain": "real spherical harmonics on S^2", "coefficient_domain": "rational dense subspace", "objective": "normalized L4/L2 ratio"}
EXPONENTS = [(a, b, DEGREE - a - b) for a in range(DEGREE, -1, -1) for b in range(DEGREE - a, -1, -1)]
EXPONENT_INDEX = {exponent: i for i, exponent in enumerate(EXPONENTS)}


def _integer_text(text):
    if not isinstance(text, str) or not text:
        raise ValueError("invalid integer text")
    sign = 1
    if text[0] in "+-":
        if text[0] == "-":
            sign = -1
        text = text[1:]
    if not text or not text.isascii() or not text.isdigit():
        raise ValueError("invalid integer text")
    first = len(text) % 9 or 9
    value = int(text[:first])
    for start in range(first, len(text), 9):
        value = value * 10**9 + int(text[start:start + 9])
    return sign * value


def _rational(value):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, bool) or not isinstance(value, str) or value.count("/") > 1:
        raise ValueError("coefficients must be rational integer strings or integers")
    if "/" not in value:
        return Fraction(_integer_text(value))
    numerator, denominator = value.split("/")
    den = _integer_text(denominator)
    if den == 0:
        raise ValueError("rational denominator cannot be zero")
    return Fraction(_integer_text(numerator), den)


def _monomial_exponents(total_degree):
    return [(a, b, total_degree - a - b)
            for a in range(total_degree, -1, -1)
            for b in range(total_degree - a, -1, -1)]


def _harmonic_laplacian(coefficients):
    laplacian = {}
    for (a, b, c), value in zip(EXPONENTS, coefficients):
        if a >= 2:
            key = (a - 2, b, c)
            laplacian[key] = laplacian.get(key, Fraction(0)) + value * a * (a - 1)
        if b >= 2:
            key = (a, b - 2, c)
            laplacian[key] = laplacian.get(key, Fraction(0)) + value * b * (b - 1)
        if c >= 2:
            key = (a, b, c - 2)
            laplacian[key] = laplacian.get(key, Fraction(0)) + value * c * (c - 1)
    return {key: value for key, value in laplacian.items() if value}


def _multiply(left, right):
    out = {}
    for (a, b, c), x in left.items():
        for (d, e, f), y in right.items():
            key = (a + d, b + e, c + f)
            out[key] = out.get(key, Fraction(0)) + x * y
    return {key: value for key, value in out.items() if value}


def _double_factorial(n):
    result = 1
    while n > 1:
        result *= n
        n -= 2
    return result


def _sphere_moment(exponent):
    a, b, c = exponent
    if (a | b | c) & 1:
        return Fraction(0)
    p, q, r = a // 2, b // 2, c // 2
    numerator = _double_factorial(2 * p - 1) * _double_factorial(2 * q - 1) * _double_factorial(2 * r - 1)
    denominator = _double_factorial(a + b + c + 1)
    return Fraction(numerator, denominator)


def _integrate_unit_sphere(poly):
    return sum((coefficient * _sphere_moment(exponent)
                for exponent, coefficient in poly.items()), Fraction(0))


def _integer_output(value):
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    chunks = []
    while value:
        value, part = divmod(value, 10**9)
        chunks.append(part)
    return sign + str(chunks[-1]) + "".join(f"{part:09d}" for part in reversed(chunks[:-1]))


def _fraction_text(value):
    numerator = _integer_output(value.numerator)
    return numerator if value.denominator == 1 else f"{numerator}/{_integer_output(value.denominator)}"


def _fourth_root_bounds(value, scale=10**18):
    if value < 0:
        raise ValueError("fourth-root argument must be nonnegative")
    numerator = value.numerator * scale**4
    denominator = value.denominator
    q = __import__("math").isqrt(__import__("math").isqrt(numerator // denominator))
    while (q + 1) ** 4 * denominator <= numerator:
        q += 1
    while q**4 * denominator > numerator:
        q -= 1
    lower = Fraction(q, scale)
    upper = lower if q**4 * denominator == numerator else Fraction(q + 1, scale)
    return lower, upper


def validate(solution, config, strict=False):
    if (not isinstance(config, dict) or config.get("id") != "T092-C01"
            or config.get("direction") != "maximize"
            or not isinstance(config.get("parameters"), dict)
            or config["parameters"] != PARAMETERS
            or any(type(config["parameters"].get(k)) is not type(v) for k, v in PARAMETERS.items())):
        raise ValueError("unsupported configuration or parameters")
    if not isinstance(solution, dict) or not isinstance(solution.get("coefficients"), list):
        raise ValueError("solution must contain a coefficient list")
    raw = solution["coefficients"]
    if len(raw) != len(EXPONENTS):
        raise ValueError("a degree-20 homogeneous polynomial requires 231 coefficients")
    coefficients = [_rational(value) for value in raw]
    if not any(coefficients):
        raise ValueError("the polynomial must be nonzero")
    residual = _harmonic_laplacian(coefficients)
    if residual:
        raise ValueError("the homogeneous polynomial is not harmonic")
    polynomial = {exp: value for exp, value in zip(EXPONENTS, coefficients) if value}
    square = _multiply(polynomial, polynomial)
    fourth_power = _multiply(square, square)
    m2 = _integrate_unit_sphere(square)
    m4 = _integrate_unit_sphere(fourth_power)
    if m2 <= 0 or m4 <= 0:
        raise ValueError("nonzero harmonic polynomial must have positive second and fourth moments")
    ratio = m4 / (m2 * m2)
    lower, upper = _fourth_root_bounds(ratio)
    ratio_text = _fraction_text(ratio)
    exact_objective = f"fourth_root({ratio_text})"
    return {
        "objective": exact_objective,
        "objective_value": _fraction_text(lower),
        "verification_status": "certified",
        "details": {
            "degree": DEGREE,
            "monomial_count": len(EXPONENTS),
            "harmonic_laplacian_residual_terms": 0,
            "sphere_average_M2": _fraction_text(m2),
            "sphere_average_M4": _fraction_text(m4),
            "fourth_power_ratio": ratio_text,
            "objective_interval": [_fraction_text(lower), _fraction_text(upper)],
            "moment_method": "Exact rational monomial moments on the unit sphere: odd powers integrate to zero, and E[x^(2a)y^(2b)z^(2c)]=(2a-1)!!(2b-1)!!(2c-1)!!/(2(a+b+c)+1)!!.",
            "claimed_score_ignored": True
        }
    }
