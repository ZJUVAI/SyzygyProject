"""Exact set counts and a certified logarithmic objective for T077-C01."""

from collections.abc import Mapping


CONFIG_ID = "T077-C01"
MIN_CARDINALITY = 2
MAX_CARDINALITY = 512
LOWER_BOUND = -1_000_000
UPPER_BOUND = 1_000_000
PARAMETERS = {
    "min_cardinality": 2,
    "max_cardinality": 512,
    "integer_interval": [-1_000_000, 1_000_000],
    "objective": "ln(|A-A|) / ln(|A+A|)",
}


def _check_config(config):
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix the T077 cardinality, interval, and objective")


def _interval_endpoint_text(endpoint, lower):
    text = str(endpoint).strip().strip("[]")
    pieces = text.split(",", 1)
    return pieces[0].strip() if lower else pieces[-1].strip()


def validate(solution, config, strict=False):
    """Validate the set, then return a conservative lower bound for maximization."""
    _check_config(config)
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    raw = solution.get("set")
    if not isinstance(raw, (list, tuple)):
        raise ValueError("set must be a list of integers")
    n = len(raw)
    if not MIN_CARDINALITY <= n <= MAX_CARDINALITY:
        raise ValueError("set cardinality must be in 2..512")
    values = []
    for index, item in enumerate(raw):
        if type(item) is not int:
            raise ValueError(f"element {index} must be an integer; bool is invalid")
        if item < LOWER_BOUND or item > UPPER_BOUND:
            raise ValueError(f"element {index} lies outside [-1000000,1000000]")
        values.append(item)
    if len(set(values)) != n:
        raise ValueError("set elements must be distinct")

    sumset = {a + b for a in values for b in values}
    difference_set = {a - b for a in values for b in values}
    sum_size = len(sumset)
    difference_size = len(difference_set)
    if sum_size <= 1 or difference_size <= 1:
        raise ValueError("both set cardinalities must exceed one for the logarithms")

    from mpmath import iv
    iv.dps = 80
    score_interval = iv.ln(iv.mpf(difference_size)) / iv.ln(iv.mpf(sum_size))
    lower = _interval_endpoint_text(score_interval.a, lower=True)
    upper = _interval_endpoint_text(score_interval.b, lower=False)
    return {
        "objective": lower,
        "objective_value": lower,
        "verification_status": "certified",
        "details": {
            "cardinality": n,
            "sumset_size": sum_size,
            "difference_set_size": difference_size,
            "objective_interval": [lower, upper],
            "objective_lower_bound": lower,
            "sumset_exact": True,
            "difference_set_exact": True,
            "claimed_objective_ignored": True,
            "strict": bool(strict),
        },
    }
