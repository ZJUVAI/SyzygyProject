"""Reconstruct a large-factor witness with the repository's greedy method."""

import os

N = 100000
THRESHOLD = 33330
_LAST_SUBFACTOR_COUNT = 0


def _smallest_prime_factors(limit):
    spf = [0] * (limit + 1)
    primes = []
    for value in range(2, limit + 1):
        if spf[value] == 0:
            spf[value] = value
            primes.append(value)
        for prime in primes:
            multiple = value * prime
            if multiple > limit or prime > spf[value]:
                break
            spf[multiple] = prime
    return spf, primes


def _factor_small(value, spf):
    exponents = {}
    while value > 1:
        prime = spf[value]
        count = 0
        while value % prime == 0:
            value //= prime
            count += 1
        exponents[prime] = count
    return exponents


def build_greedy_witness(n=N, threshold=THRESHOLD):
    global _LAST_SUBFACTOR_COUNT
    if n != N or threshold != THRESHOLD:
        raise ValueError("unsupported fixed configuration")
    spf, all_primes = _smallest_prime_factors(n)
    small_primes = [p for p in all_primes if p < threshold]
    prime_index = {p: i for i, p in enumerate(small_primes)}
    exponents = {}
    for prime in small_primes:
        exponent = 0
        power = prime
        while power <= n:
            exponent += n // power
            if power > n // prime:
                break
            power *= prime
        exponents[prime] = exponent

    # Each item stores (factor value, prime-exponent pairs), so we can restore
    # all prime powers that the greedy subfactorization did not use.
    items = []
    for prime in all_primes:
        if prime >= threshold:
            item = (prime, ((prime, 1),))
            items.extend([item] * (n // prime))

    i = len(small_primes) - 1
    min_m = 0
    while True:
        while i >= 0 and exponents[small_primes[i]] == 0:
            i -= 1
        if i < 0:
            break

        prime = small_primes[i]
        m = max((threshold + prime - 1) // prime, min_m)
        while m < threshold:
            factors_m = _factor_small(m, spf)
            x = dict(factors_m)
            x[prime] = x.get(prime, 0) + 1
            divisions = min(exponents[p] // count for p, count in x.items())
            if divisions >= 1:
                break
            m += 1
            if exponents[prime] >= x.get(prime, 0):
                min_m = m

        if m == threshold:
            break

        for p, count in x.items():
            exponents[p] -= count * divisions
        factorization = dict(factors_m)
        factorization[prime] = factorization.get(prime, 0) + 1
        encoded = tuple(sorted(factorization.items()))
        items.extend([(m * prime, encoded)] * divisions)

    if len(items) < N:
        raise RuntimeError(f"greedy method produced only {len(items)} large factors")
    _LAST_SUBFACTOR_COUNT = len(items)

    factors = [value for value, _ in items[:N]]
    used = {p: 0 for p in all_primes}
    for _, factorization in items[:N]:
        for prime, exponent in factorization:
            used[prime] += exponent

    # Distribute every unallocated prime power across all retained factors.
    # This converts the divisor with at least N large factors into exactly N
    # factors of the full factorial, while preserving the minimum threshold.
    cursor = 0
    for prime in all_primes:
        total = 0
        power = prime
        while power <= n:
            total += n // power
            if power > n // prime:
                break
            power *= prime
        remaining = total - used[prime]
        if remaining < 0:
            raise RuntimeError("greedy factorization used too many prime powers")
        common, remainder = divmod(remaining, N)
        if common:
            multiplier = prime ** common
            factors = [value * multiplier for value in factors]
        for offset in range(remainder):
            index = (cursor + offset) % N
            factors[index] *= prime
        cursor = (cursor + remainder) % N

    if len(factors) != N or min(factors) < threshold:
        raise RuntimeError("constructed witness failed its local checks")
    return factors


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T053-C01") != "T053-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    factors = build_greedy_witness()
    return {
        "factors": factors,
        "method_metadata": {
            "method": "Andrew Sutherland's greedy large-factor method, reconstructed from the pinned repository source",
            "threshold": THRESHOLD,
            "factors_before_restoring_residual": _LAST_SUBFACTOR_COUNT,
            "seed": seed,
            "residual_prime_powers_distributed": True,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
