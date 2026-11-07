"""Exact checker for admissible integer k-tuples."""

_CONFIGS = {"T019-C01": 343, "T019-C02": 1000, "T019-C03": 3000}


def _primes_through(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i : n + 1 : i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i, flag in enumerate(sieve) if flag]


def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    params = config.get("parameters", config)
    config_id = config.get("id")
    k = _CONFIGS.get(config_id)
    if k is None:
        raise ValueError("unsupported T019 configuration")
    if isinstance(params, dict) and params.get("k", k) != k:
        raise ValueError("configuration parameters do not match id")
    values = solution.get("tuple")
    if not isinstance(values, list) or len(values) != k:
        raise ValueError(f"tuple must contain exactly {k} integers")
    if any(type(x) is not int for x in values):
        raise ValueError("tuple entries must be strict integers; bool is not accepted")
    if len(set(values)) != k:
        raise ValueError("tuple entries must be distinct")
    residues = {}
    for p in _primes_through(k):
        seen = {x % p for x in values}
        if len(seen) == p:
            raise ValueError(f"tuple covers every residue class modulo prime {p}")
        residues[p] = p - len(seen)
    diameter = max(values) - min(values)
    return {
        "objective": diameter,
        "verification_status": "exact",
        "details": {"k": k, "diameter": diameter, "prime_count_checked": len(residues), "missing_residue_counts": residues, "claimed_objective_ignored": True},
    }
