"""Exact checker for finite +/-1 sequences with discrepancy at most 3."""


SEQUENCE_LENGTH = "variable"
CONFIG_ID = "T051-C01"
CAP = 3
ENTRY_DOMAIN = [-1, 1]
CONSTRAINT = "every prefix of every homogeneous arithmetic progression has absolute sum at most 3"


def _check_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    if config.get("id") not in (None, CONFIG_ID):
        raise ValueError(f"unsupported configuration: expected {CONFIG_ID}")
    parameters = config.get("parameters")
    if not isinstance(parameters, dict) or set(parameters) != {
        "discrepancy_cap", "entry_domain", "constraint"
    }:
        raise ValueError("configuration must fix discrepancy cap C=3 and unrestricted signs")
    domain = parameters.get("entry_domain")
    if (type(parameters.get("discrepancy_cap")) is not int
            or parameters["discrepancy_cap"] != CAP
            or not isinstance(domain, list)
            or len(domain) != 2
            or any(type(value) is not int for value in domain)
            or domain != ENTRY_DOMAIN
            or parameters.get("constraint") != CONSTRAINT):
        raise ValueError("configuration must fix discrepancy cap C=3 and unrestricted signs")


def validate(solution, config, strict=False):
    """Recompute all homogeneous-progression prefix sums exactly."""
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    sequence = solution.get("sequence")
    if not isinstance(sequence, list) or not sequence:
        raise ValueError("sequence must be a nonempty JSON array")
    for i, value in enumerate(sequence):
        if type(value) is not int or value not in (-1, 1):
            raise ValueError(f"sequence entry {i} must be the integer -1 or +1")

    n = len(sequence)
    maximum = 0
    maximizing_witness = None
    for d in range(1, n + 1):
        partial = 0
        k = 0
        for index in range(d - 1, n, d):
            partial += sequence[index]
            k += 1
            magnitude = abs(partial)
            if magnitude > CAP:
                raise ValueError(
                    f"discrepancy exceeds 3: d={d}, k={k}, signed_sum={partial}"
                )
            if magnitude > maximum:
                maximum = magnitude
                maximizing_witness = {"difference": d, "prefix_length": k, "signed_sum": partial}
    return {
        "objective": n,
        "verification_status": "exact",
        "details": {
            "sequence_length": n,
            "discrepancy": maximum,
            "maximizing_prefix": maximizing_witness,
            "homogeneous_progression_prefixes_checked": sum(n // d for d in range(1, n + 1)),
            "claimed_objective_ignored": True,
        },
    }
