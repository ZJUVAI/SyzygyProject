"""Exact checker for bilinear rank decompositions of 3x3 matrix multiplication."""
from fractions import Fraction
import re

_CONFIG = {
    "matrix_order": 3,
    "field": "Q",
    "coefficient_domain": "arbitrary rational strings or exact Fraction values",
    "max_terms": 27,
    "term_count_is_scalar_multiplication_count": True,
}
_RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/-?(?:[1-9][0-9]*))?\Z")


def _fraction(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a rational coefficient")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, str) and _RATIONAL.fullmatch(value):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError):
            pass
    raise ValueError("coefficients must be integers, rational strings, or Fraction values")


def _vector(value, name):
    if not isinstance(value, list) or len(value) != 9:
        raise ValueError(f"{name} must be a list of exactly nine rational coefficients")
    return tuple(_fraction(item) for item in value)


def validate(solution, config, strict=False):
    """Check all 729 coefficients of the represented bilinear map exactly."""
    del strict  # Arithmetic is exact in every mode.
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    params = config.get("parameters", config)
    if not isinstance(params, dict) or any(params.get(k) != v for k, v in _CONFIG.items()):
        raise ValueError("configuration must specify 3x3 multiplication over Q with a 27-term resource cap")
    terms = solution.get("terms")
    if not isinstance(terms, list) or not 1 <= len(terms) <= _CONFIG["max_terms"]:
        raise ValueError("terms must contain between 1 and 27 bilinear products")

    parsed = []
    for index, term in enumerate(terms):
        if not isinstance(term, dict):
            raise ValueError(f"term {index} must be an object")
        alpha = _vector(term.get("alpha"), f"term {index} alpha")
        beta = _vector(term.get("beta"), f"term {index} beta")
        gamma = _vector(term.get("gamma"), f"term {index} gamma")
        if not any(alpha) or not any(beta) or not any(gamma):
            raise ValueError(f"term {index} has a zero factor and does not count as a product")
        parsed.append((alpha, beta, gamma))

    # Flattening convention: indices are row-major. gamma[i,k] multiplies
    # alpha(A) beta(B) into output C[i,k]. Hence the target is
    # sum_j A[i,j] B[j,k], with no exchange or mixing of A and B.
    for out_i in range(3):
        for out_k in range(3):
            gamma_index = 3 * out_i + out_k
            for a_i in range(3):
                for a_j in range(3):
                    a_index = 3 * a_i + a_j
                    for b_j in range(3):
                        for b_k in range(3):
                            b_index = 3 * b_j + b_k
                            value = sum((a[a_index] * b[b_index] * g[gamma_index]
                                         for a, b, g in parsed), Fraction(0))
                            expected = int(a_i == out_i and a_j == b_j and b_k == out_k)
                            if value != expected:
                                raise ValueError(
                                    "tensor identity fails at coefficient "
                                    f"A[{a_i},{a_j}] B[{b_j},{b_k}] -> C[{out_i},{out_k}]"
                                )
    return {
        "objective": len(parsed),
        "verification_status": "exact",
        "details": {
            "matrix_order": 3,
            "field": "Q",
            "tensor_coefficients_recomputed": 729,
            "input_forms": "alpha(A) * beta(B), separate linear forms",
            "output_convention": "gamma[i,k] contributes to C[i,k]",
            "claimed_objective_ignored": True,
            "max_terms_is_resource_cap_not_an_optimality_bound": True,
        },
    }
