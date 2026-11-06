"""Exact sum and difference counts with a certified objective interval."""
from fractions import Fraction

PARAMETERS = {"max_cardinality": 512, "integer_interval": [-1000000, 1000000]}


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("id") != "T057-C01" or config.get("parameters") != PARAMETERS:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    values = solution.get("set")
    if not isinstance(values, (list, tuple)):
        raise ValueError("set must be a list of integers")
    n = len(values)
    if not 2 <= n <= 512:
        raise ValueError("set cardinality must be in 2..512")
    if any(type(x) is not int for x in values):
        raise ValueError("elements must be integers; bool is rejected")
    if len(set(values)) != n:
        raise ValueError("set elements must be distinct")
    if any(x < -1000000 or x > 1000000 for x in values):
        raise ValueError("elements must lie in [-1000000,1000000]")
    sums = {a + b for a in values for b in values}
    diffs = {a - b for a in values for b in values}
    s, d = len(sums), len(diffs)
    # For ratios > 1, both logarithm arguments must exceed one. The ratio
    # exceeds one exactly when s > d, so no floating-point comparison is used.
    if s <= n or d <= n or s <= d:
        raise ValueError("objective is defined only for |A+A| > |A-A| > |A|")
    from mpmath import iv
    iv.dps = 80
    numerator = iv.ln(iv.mpf(s) / n)
    denominator = iv.ln(iv.mpf(d) / n)
    result = numerator / denominator
    # mpmath prints even a point interval as ``[x, x]``. Extract the
    # endpoint itself so the record remains a plain decimal string.
    lower = str(result.a).strip("[]").split(",", 1)[0].strip()
    upper = str(result.b).strip("[]").split(",", 1)[-1].strip()
    claimed = solution.get("objective")
    mismatch = claimed is not None and (type(claimed) not in (int, float) or not float(claimed) == float(lower))
    return {
        "objective": lower,
        "objective_value": lower,
        "verification_status": "certified",
        "details": {"cardinality": n, "sumset_size": s, "difference_set_size": d,
                    "objective_interval": [lower, upper], "objective_lower_bound": lower,
                    "claimed_objective_mismatch": mismatch,
                    "sumset_exact": True, "difference_set_exact": True}
    }
