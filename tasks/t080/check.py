"""Exact finite set checks and a certified T080 logarithmic objective."""

from collections.abc import Mapping


CONFIG_ID = "T080-C01"
MIN_CARDINALITY = 2
MAX_CARDINALITY = 512
MAX_ELEMENT = 1_000_000
PARAMETERS = {
    "min_cardinality": 2,
    "max_cardinality": 512,
    "contains_zero": True,
    "integer_interval": [0, 1_000_000],
    "require_difference_size_lt_q": True,
    "q_definition": "2*max(U)+1",
    "objective": "1+ln(|U-U|/|U+U|)/ln(q)",
}


def _check_config(config):
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix the T080 cardinality, interval, and objective")


def _endpoint_text(endpoint, lower):
    text = str(endpoint).strip().strip("[]")
    parts = text.split(",", 1)
    return parts[0].strip() if lower else parts[-1].strip()


def validate(solution, config, strict=False):
    """Recompute s,d,q exactly and certify a conservative lower score endpoint."""
    _check_config(config)
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    raw = solution.get("set")
    if not isinstance(raw, (list, tuple)):
        raise ValueError("set must be a list of nonnegative integers")
    n = len(raw)
    if not MIN_CARDINALITY <= n <= MAX_CARDINALITY:
        raise ValueError("set cardinality must be in 2..512")
    values = []
    for index, item in enumerate(raw):
        if type(item) is not int:
            raise ValueError(f"element {index} must be an integer; bool is invalid")
        if item < 0 or item > MAX_ELEMENT:
            raise ValueError(f"element {index} lies outside [0,1000000]")
        values.append(item)
    if len(set(values)) != n:
        raise ValueError("set elements must be distinct")
    if 0 not in values:
        raise ValueError("U must contain zero")

    sumset = {a + b for a in values for b in values}
    difference_set = {a - b for a in values for b in values}
    sum_size = len(sumset)
    difference_size = len(difference_set)
    q = 2 * max(values) + 1
    if not difference_size < q:
        raise ValueError("the strict finite-lemma condition |U-U| < 2*max(U)+1 must hold")
    if sum_size <= 1 or difference_size <= 1 or q <= 1:
        raise ValueError("sumset, difference set, and q must give positive logarithm arguments")

    from mpmath import iv
    iv.dps = 80
    ratio_interval = iv.ln(iv.mpf(difference_size) / iv.mpf(sum_size)) / iv.ln(iv.mpf(q))
    score_interval = 1 + ratio_interval
    lower = _endpoint_text(score_interval.a, lower=True)
    upper = _endpoint_text(score_interval.b, lower=False)
    return {
        "objective": lower,
        "objective_value": lower,
        "verification_status": "certified",
        "details": {
            "cardinality": n,
            "sumset_size": sum_size,
            "difference_set_size": difference_size,
            "q": q,
            "strict_difference_bound_verified": True,
            "objective_interval": [lower, upper],
            "objective_lower_bound": lower,
            "sumset_exact": True,
            "difference_set_exact": True,
            "claimed_objective_ignored": True,
            "strict": bool(strict),
        },
    }
