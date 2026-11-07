"""Exact feasible-polynomial checker for the degree-146 integer Chebyshev task."""

from fractions import Fraction
import heapq
import math

DEGREE_LIMIT = 146
MAX_BERNSTEIN_SPLITS = 100_000
RELATIVE_WIDTH = Fraction(1, 10**10)


def _config_n(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    parameters = config.get("parameters")
    expected = {
        "degree_at_most": DEGREE_LIMIT,
        "interval": [0, 1],
        "coefficient_domain": "nonzero integer polynomials",
    }
    if parameters != expected:
        raise ValueError("configuration must be degree_at_most=146 on [0,1]")
    return DEGREE_LIMIT


def _parse_coefficients(solution):
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    coefficients = solution.get("coefficients")
    if not isinstance(coefficients, list) or not coefficients:
        raise ValueError("coefficients must be a nonempty low-to-high list")
    if len(coefficients) > DEGREE_LIMIT + 1:
        raise ValueError("polynomial degree exceeds 146")
    if any(type(value) is not int for value in coefficients):
        raise ValueError("coefficients must be integers; bool and numeric approximations are invalid")
    values = list(coefficients)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    if all(value == 0 for value in values):
        raise ValueError("the zero polynomial is excluded")
    return values


def _bernstein_coefficients(power_coefficients):
    """Convert power coefficients on [0,1] to Bernstein coefficients."""
    degree = len(power_coefficients) - 1
    result = []
    for k in range(degree + 1):
        value = Fraction(0)
        for i in range(k + 1):
            value += Fraction(power_coefficients[i] * math.comb(k, i), math.comb(degree, i))
        result.append(value)
    return result


def _split_bernstein(coefficients):
    """Return exact Bernstein coefficients on the left and right half intervals."""
    row = coefficients[:]
    left = [row[0]]
    right = [row[-1]]
    while len(row) > 1:
        row = [(row[i] + row[i + 1]) / 2 for i in range(len(row) - 1)]
        left.append(row[0])
        right.append(row[-1])
    right.reverse()
    return left, right, row[0]


def _upper(coefficients):
    return max(abs(value) for value in coefficients)


def _certified_supnorm(power_coefficients):
    """Bound ||P|| exactly by adaptive Bernstein convex-hull enclosures.

    For each interval, the polynomial is a convex combination of its Bernstein
    coefficients. Their maximum absolute value is therefore an upper bound.
    Dyadic subdivision tightens the bound. A dyadic value supplies the lower
    endpoint. No sample is used as an upper-bound certificate.
    """
    initial = _bernstein_coefficients(power_coefficients)
    lower = max(abs(initial[0]), abs(initial[-1]))
    serial = 0
    heap = [(-_upper(initial), serial, initial)]
    splits = 0
    while True:
        upper = -heap[0][0]
        if upper - lower <= max(lower, upper) * RELATIVE_WIDTH:
            return lower, upper, splits
        if splits >= MAX_BERNSTEIN_SPLITS:
            raise ValueError("exact sup-norm enclosure did not converge within the checker work limit")
        _, _, current = heapq.heappop(heap)
        left, right, midpoint_value = _split_bernstein(current)
        lower = max(lower, abs(midpoint_value))
        serial += 1
        heapq.heappush(heap, (-_upper(left), serial, left))
        serial += 1
        heapq.heappush(heap, (-_upper(right), serial, right))
        splits += 1


def validate(solution, config, strict=False):
    """Return an exact rational enclosure for the full-domain supremum norm."""
    del strict  # The same proof method is used in both modes.
    degree_limit = _config_n(config)
    coefficients = _parse_coefficients(solution)
    degree = len(coefficients) - 1
    lower, upper, splits = _certified_supnorm(coefficients)
    return {
        "objective": str(upper),
        "objective_value": str(upper),
        "verification_status": "certified",
        "details": {
            "objective_interval": [str(lower), str(upper)],
            "domain": "[0,1]",
            "degree": degree,
            "degree_at_most": degree_limit,
            "coefficients_low_to_high": len(coefficients),
            "method": "exact adaptive Bernstein convex-hull enclosure",
            "subdivision_count": splits,
            "claimed_objective_ignored": True,
        },
    }
