"""Exact checker for admissible integer 343-tuples."""


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
    k = params.get("k") if isinstance(params, dict) else None
    if type(k) is not int or k != 343:
        raise ValueError("configuration must specify k=343")
    values = solution.get("tuple")
    if not isinstance(values, list) or len(values) != k:
        raise ValueError("tuple must contain exactly 343 integers")
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
        "details": {"k": k, "diameter": diameter, "prime_count_checked": len(residues), "missing_residue_counts": residues},
    }
