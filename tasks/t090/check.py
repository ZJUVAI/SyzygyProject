"""Exact integer checker for length-64 periodic binary autocorrelation energy."""

LENGTH = 64
CONFIG_ID = "T090-C01"
PARAMETERS = {
    "length": 64,
    "alphabet": [-1, 1],
    "boundary": "periodic",
    "correlation": "C_k = sum_i s_i s_(i+k mod 64), for k=1..63",
    "objective": "sum of squared off-peak periodic autocorrelations",
}


def _check_config(config):
    if type(config) is not dict or type(config.get("id")) is not str or config.get("id") != CONFIG_ID:
        raise ValueError(f"configuration id must be {CONFIG_ID}")
    if not _same_typed(config.get("parameters"), PARAMETERS):
        raise ValueError("configuration parameters do not match the frozen periodic problem")
    if type(config.get("direction")) is not str or config.get("direction") != "minimize":
        raise ValueError("periodic autocorrelation energy is minimized")


def _same_typed(actual, expected):
    """Compare nested JSON values without Python's bool/int equality alias."""
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return actual.keys() == expected.keys() and all(
            _same_typed(actual[key], expected[key]) for key in expected
        )
    if type(expected) is list:
        return len(actual) == len(expected) and all(
            _same_typed(left, right) for left, right in zip(actual, expected)
        )
    return actual == expected


def periodic_correlations(sequence):
    return [
        sum(sequence[index] * sequence[(index + shift) % LENGTH] for index in range(LENGTH))
        for shift in range(LENGTH)
    ]


def validate(solution, config, strict=False):
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    sequence = solution.get("sequence")
    if not isinstance(sequence, list) or len(sequence) != LENGTH:
        raise ValueError("sequence must contain exactly 64 entries")
    if any(type(value) is not int or value not in (-1, 1) for value in sequence):
        raise ValueError("each sequence entry must be the integer -1 or +1")
    correlations = periodic_correlations(sequence)
    energy = sum(value * value for value in correlations[1:])
    psl = max(abs(value) for value in correlations[1:])
    return {
        "objective": energy,
        "verification_status": "exact",
        "details": {
            "length": LENGTH,
            "periodic_correlations_including_peak": correlations,
            "off_peak_energy": energy,
            "peak_sidelobe_level": psl,
            "claimed_objective_ignored": True,
        },
    }
