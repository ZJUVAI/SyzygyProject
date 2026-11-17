"""Exact validation for the official LABS length 100 configuration."""


def aperiodic_autocorrelations(sequence):
    n = len(sequence)
    return [sum(sequence[i] * sequence[i + lag] for i in range(n - lag))
            for lag in range(1, n)]


def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    params = config.get("parameters", config)
    length = params.get("L") if isinstance(params, dict) else None
    if type(length) is not int or length != 100:
        raise ValueError("configuration must specify L=100")
    sequence = solution.get("sequence")
    if not isinstance(sequence, list) or len(sequence) != length:
        raise ValueError(f"sequence must contain exactly {length} signs")
    if any(type(value) is not int or value not in (-1, 1) for value in sequence):
        raise ValueError("sequence entries must be integer -1 or 1; bool is not accepted")
    correlations = aperiodic_autocorrelations(sequence)
    energy = sum(value * value for value in correlations)
    return {"objective": energy, "verification_status": "exact",
            "details": {"aperiodic_autocorrelations": correlations, "L": length}}
