"""Return the fixed, feasible primorial-multiple seed for k=343."""


def _primes_through(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i : n + 1 : i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i, flag in enumerate(sieve) if flag]


def run_code():
    primorial = 1
    for p in _primes_through(343):
        primorial *= p
    return {"tuple": [i * primorial for i in range(343)]}
