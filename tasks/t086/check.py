"""Exact feasibility and certified objective bounds for T086-C01."""

from collections.abc import Mapping
from fractions import Fraction
from itertools import permutations, product
from math import isqrt
import sys


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

CONFIG_ID = "T086-C01"
MATRIX_COUNT = 4
DIMENSION = 3
ROOT_SCALE = 10**36
PARAMETERS = {
    "n": 4,
    "m": 4,
    "dimension": 3,
    "field": "complex",
    "matrix_class": "Hermitian positive semidefinite",
    "norm": "Schatten 2 / Frobenius",
    "numerator": "mean norm over 256 ordered products with replacement",
    "denominator": "mean norm over 24 ordered products without replacement",
}


def _check_config(config):
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix the T086 Duchi inside-sum instance")


def _fraction(value, label):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value.strip())
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"{label} must be an exact rational string") from exc
    raise ValueError(f"{label} must be an integer or exact rational string; floats are invalid")


def _complex_entry(value, label):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"{label} must be [real,imaginary]")
    return _fraction(value[0], f"{label}.real"), _fraction(value[1], f"{label}.imaginary")


def _parse_matrices(solution):
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    raw = solution.get("matrices")
    if not isinstance(raw, (list, tuple)) or len(raw) != MATRIX_COUNT:
        raise ValueError("matrices must contain exactly four matrices")
    matrices = []
    for mi, matrix in enumerate(raw):
        if not isinstance(matrix, (list, tuple)) or len(matrix) != DIMENSION:
            raise ValueError(f"matrix {mi} must have exactly three rows")
        parsed = []
        for ri, row in enumerate(matrix):
            if not isinstance(row, (list, tuple)) or len(row) != DIMENSION:
                raise ValueError(f"matrix {mi} row {ri} must have exactly three entries")
            parsed.append([_complex_entry(entry, f"matrices[{mi}][{ri}][{ci}]") for ci, entry in enumerate(row)])
        matrices.append(parsed)
    return matrices


def _conj(z):
    return z[0], -z[1]


def _add(a, b):
    return a[0] + b[0], a[1] + b[1]


def _mul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def _norm_sq(z):
    return z[0] * z[0] + z[1] * z[1]


def _permutation_sign(p):
    inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inversions % 2 else 1


def _det3(matrix):
    total = (Fraction(0), Fraction(0))
    for p in permutations(range(3)):
        term = _mul(_mul(matrix[0][p[0]], matrix[1][p[1]]), matrix[2][p[2]])
        if _permutation_sign(p) < 0:
            term = (-term[0], -term[1])
        total = _add(total, term)
    return total


def _validate_psd(matrix, index):
    for i in range(3):
        diagonal = matrix[i][i]
        if diagonal[1] != 0:
            raise ValueError(f"matrix {index} diagonal entries must be real")
        if diagonal[0] < 0:
            raise ValueError(f"matrix {index} has a negative diagonal principal minor")
        for j in range(i + 1, 3):
            if matrix[j][i] != _conj(matrix[i][j]):
                raise ValueError(f"matrix {index} must be Hermitian")
            minor = diagonal[0] * matrix[j][j][0] - _norm_sq(matrix[i][j])
            if minor < 0:
                raise ValueError(f"matrix {index} has a negative 2x2 principal minor")
    determinant = _det3(matrix)
    if determinant[1] != 0:
        raise ValueError(f"matrix {index} determinant must be real")
    if determinant[0] < 0:
        raise ValueError(f"matrix {index} has a negative determinant")


def _identity():
    return [[(Fraction(int(i == j)), Fraction(0)) for j in range(3)] for i in range(3)]


def _matrix_multiply(left, right):
    result = [[(Fraction(0), Fraction(0)) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            entry = (Fraction(0), Fraction(0))
            for k in range(3):
                entry = _add(entry, _mul(left[i][k], right[k][j]))
            result[i][j] = entry
    return result


def _product_norm_sq(matrices, indices):
    matrix = _identity()
    for index in indices:
        matrix = _matrix_multiply(matrix, matrices[index])
    return sum((_norm_sq(matrix[i][j]) for i in range(3) for j in range(3)), Fraction(0))


def _sqrt_interval(value, scale):
    if value < 0:
        raise ValueError("a squared norm cannot be negative")
    if value == 0:
        return Fraction(0), Fraction(0)
    scaled_numerator = value.numerator * scale * scale
    floor_root = isqrt(scaled_numerator // value.denominator)
    lower = Fraction(floor_root, scale)
    if floor_root * floor_root * value.denominator == scaled_numerator:
        return lower, lower
    return lower, Fraction(floor_root + 1, scale)


def _fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _norm_squares(matrices, tuples):
    return [_product_norm_sq(matrices, indices) for indices in tuples]


def _norm_sum_interval(norm_squares, scale):
    lower = Fraction(0)
    upper = Fraction(0)
    nonzero = False
    for norm_sq in norm_squares:
        lo, hi = _sqrt_interval(norm_sq, scale)
        lower += lo
        upper += hi
        nonzero |= norm_sq > 0
    return lower, upper, nonzero


def _scale_for_positive_lower(value):
    """Choose a decimal scale at which sqrt(value) has a positive lower bound."""
    needed = isqrt(value.denominator // value.numerator)
    if needed * needed * value.numerator < value.denominator:
        needed += 1
    return max(ROOT_SCALE, needed)


def validate(solution, config, strict=False):
    """Recompute PSD and the all-products ratio with exact rational arithmetic."""
    _check_config(config)
    matrices = _parse_matrices(solution)
    for index, matrix in enumerate(matrices):
        _validate_psd(matrix, index)

    if all(matrix == matrices[0] for matrix in matrices[1:]):
        common_norm_sq = _product_norm_sq(matrices, (0, 0, 0, 0))
        if common_norm_sq == 0:
            raise ValueError("without-replacement mean norm must be positive")
        return {
            "objective": "1",
            "objective_value": "1",
            "verification_status": "certified",
            "details": {
                "n": 4,
                "m": 4,
                "dimension": 3,
                "field": "complex rational",
                "norm": "Schatten 2 / Frobenius",
                "products_with_replacement": 256,
                "products_without_replacement": 24,
                "common_product_norm_squared": _fraction_text(common_norm_sq),
                "objective_interval": ["1", "1"],
                "upper_bound_for_minimization": "1",
                "psd_verified_by_all_principal_minors": True,
                "without_replacement_denominator_positive": True,
                "identical_products_cancel_exactly": True,
                "claimed_objective_ignored": True,
                "strict": bool(strict),
            },
        }

    with_replacement = product(range(MATRIX_COUNT), repeat=4)
    without_replacement = permutations(range(MATRIX_COUNT))
    wr_squares = _norm_squares(matrices, with_replacement)
    wo_squares = _norm_squares(matrices, without_replacement)
    positive_wo_squares = [value for value in wo_squares if value > 0]
    if not positive_wo_squares:
        raise ValueError("without-replacement mean norm must be positive")
    scale = _scale_for_positive_lower(min(positive_wo_squares))
    wr_lo, wr_hi, _wr_nonzero = _norm_sum_interval(wr_squares, scale)
    wo_lo, wo_hi, _wo_nonzero = _norm_sum_interval(wo_squares, scale)
    factor = Fraction(24, 256)
    lower = factor * wr_lo / wo_hi
    upper = factor * wr_hi / wo_lo
    interval = [_fraction_text(lower), _fraction_text(upper)]
    objective = _fraction_text(upper)
    return {
        "objective": objective,
        "objective_value": objective,
        "verification_status": "certified",
        "details": {
            "n": 4,
            "m": 4,
            "dimension": 3,
            "field": "complex rational",
            "norm": "Schatten 2 / Frobenius",
            "products_with_replacement": len(wr_squares),
            "products_without_replacement": len(wo_squares),
            "sqrt_interval_decimal_scale": str(scale),
            "with_replacement_norm_sum_interval": [_fraction_text(wr_lo), _fraction_text(wr_hi)],
            "without_replacement_norm_sum_interval": [_fraction_text(wo_lo), _fraction_text(wo_hi)],
            "objective_interval": interval,
            "upper_bound_for_minimization": objective,
            "psd_verified_by_all_principal_minors": True,
            "without_replacement_denominator_positive": True,
            "claimed_objective_ignored": True,
            "strict": bool(strict),
        },
    }
