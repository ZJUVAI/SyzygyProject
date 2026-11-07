"""Exact verification of 10-dimensional rational lattice Gram matrices."""

from fractions import Fraction
import math
import re
import sys


CONFIG_ID = "T078-C01"
DIMENSION = 10
THRESHOLD = Fraction(4)
PARAMETERS = {
    "dimension": DIMENSION,
    "gram_entries": "exact rational numbers",
    "gram_matrix": "symmetric positive definite 10x10 matrix",
    "minimum_squared_norm": "at least 4 on nonzero integer vectors",
    "objective": "determinant of the Gram matrix",
}
_RATIONAL_RE = re.compile(r"(?:0|-[1-9][0-9]*|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def _as_fraction(value, label):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str) and _RATIONAL_RE.fullmatch(value):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"{label} is not a valid rational") from exc
    raise ValueError(f"{label} must be an integer or exact rational string")


def _check_config(config):
    if not isinstance(config, dict) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must specify the 10-dimensional lattice Gram problem")


def _ldl(matrix):
    """Return exact unit-lower L and positive diagonal D with G = L D L^T."""
    n = len(matrix)
    lower = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    diagonal = []
    for i in range(n):
        pivot = matrix[i][i] - sum(lower[i][k] ** 2 * diagonal[k] for k in range(i))
        if pivot <= 0:
            raise ValueError("Gram matrix must be positive definite")
        diagonal.append(pivot)
        for j in range(i + 1, n):
            numerator = matrix[j][i] - sum(lower[j][k] * lower[i][k] * diagonal[k] for k in range(i))
            lower[j][i] = numerator / pivot
    return lower, diagonal


def _floor(value):
    return value.numerator // value.denominator


def _ceil_sqrt_fraction(value):
    """Exact ceil(sqrt(value)) for nonnegative rational value."""
    if value < 0:
        raise ValueError("square-root bound must be nonnegative")
    floor_root = math.isqrt(value.numerator // value.denominator)
    if Fraction(floor_root * floor_root) == value:
        return floor_root
    return floor_root + 1


def _nearby_integers(center, radius):
    """Yield a safe finite coordinate superset from near to far from center."""
    base = _floor(center)
    lower = base - radius - 1
    upper = base + radius + 2
    delta = 0
    while base - delta >= lower or base + 1 + delta <= upper:
        left = base - delta
        right = base + 1 + delta
        if left >= lower:
            yield left
        if right <= upper:
            yield right
        delta += 1


def _enumerate_vectors(matrix, threshold=THRESHOLD, *, inclusive=False, stop_after=None):
    """Enumerate integer z with z^T G z < threshold (or <= if inclusive).

    Each coordinate range comes from exact rational LDL ellipsoid bounds. No
    fixed coordinate box or coefficient-size cap is used.
    """
    lower, diagonal = _ldl(matrix)
    n = len(matrix)
    vector = [0] * n
    found = []
    nodes = 0

    def within(value):
        return value <= threshold if inclusive else value < threshold

    def visit(i, used):
        nonlocal nodes
        nodes += 1
        if i < 0:
            if any(vector) and within(used):
                found.append(tuple(vector))
            return stop_after is not None and len(found) >= stop_after
        remaining = threshold - used
        if remaining < 0 or (remaining == 0 and not inclusive):
            return False
        center = -sum(lower[j][i] * vector[j] for j in range(i + 1, n))
        radius = _ceil_sqrt_fraction(remaining / diagonal[i])
        # A small exact superset avoids rational ceil/floor endpoint code;
        # every trial is then filtered by its exact quadratic contribution.
        for coordinate in _nearby_integers(center, radius):
            term = diagonal[i] * (Fraction(coordinate) - center) ** 2
            updated = used + term
            if within(updated):
                vector[i] = coordinate
                if visit(i - 1, updated):
                    return True
        vector[i] = 0
        return False

    visit(n - 1, Fraction(0))
    return found, nodes


def _parse_matrix(solution):
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    raw = solution.get("gram")
    if not isinstance(raw, list) or len(raw) != DIMENSION:
        raise ValueError("gram must be a 10x10 list")
    matrix = []
    for i, row in enumerate(raw):
        if not isinstance(row, list) or len(row) != DIMENSION:
            raise ValueError(f"gram row {i} must contain 10 entries")
        matrix.append([_as_fraction(value, f"gram[{i}][{j}]") for j, value in enumerate(row)])
    for i in range(DIMENSION):
        for j in range(i):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("Gram matrix must be exactly symmetric")
    return matrix


def validate(solution, config, strict=False):
    del strict
    _check_config(config)
    matrix = _parse_matrix(solution)
    _, diagonal = _ldl(matrix)
    determinant = math.prod(diagonal, start=Fraction(1))
    short_vectors, nodes = _enumerate_vectors(matrix, stop_after=1)
    if short_vectors:
        vector = short_vectors[0]
        raise ValueError(f"nonzero integer vector has squared norm below 4: {vector}")
    objective = determinant.numerator if determinant.denominator == 1 else str(determinant)
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "dimension": DIMENSION,
            "minimum_squared_norm_at_least": 4,
            "nonzero_vectors_below_threshold": 0,
            "ellipsoid_nodes_visited": nodes,
            "claimed_objective_ignored": True,
        },
    }
