"""Exact checker for admissible integer 343-tuples."""

_CONFIG_ID = "T019-C01"
_K = 343


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
    if config.get("id") != _CONFIG_ID:
        raise ValueError("unsupported T019 configuration")
    if isinstance(params, dict) and params.get("k", _K) != _K:
        raise ValueError("configuration parameters do not match id")
    values = solution.get("tuple")
    if not isinstance(values, list) or len(values) != _K:
        raise ValueError(f"tuple must contain exactly {_K} integers")
    if any(type(x) is not int for x in values):
        raise ValueError("tuple entries must be strict integers; bool is not accepted")
    if len(set(values)) != _K:
        raise ValueError("tuple entries must be distinct")
    residues = {}
    for p in _primes_through(_K):
        seen = {x % p for x in values}
        if len(seen) == p:
            raise ValueError(f"tuple covers every residue class modulo prime {p}")
        residues[p] = p - len(seen)
    diameter = max(values) - min(values)
    return {
        "objective": diameter,
        "verification_status": "exact",
        "details": {"k": _K, "diameter": diameter, "prime_count_checked": len(residues), "missing_residue_counts": residues, "claimed_objective_ignored": True},
    }
