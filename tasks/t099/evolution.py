"""Cold-start search for narrow admissible 343-tuples.

The search uses only the task definition. It builds candidates from an interval
after excluding residue classes for each prime, then improves the interval by
randomized endpoint/shift attempts.
"""
import os
import random
import time


def _primes(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i : n + 1 : i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i, flag in enumerate(sieve) if flag]


def _build(lo, width, primes, excluded):
    """Sieve an interval, retaining integers outside every excluded class."""
    blocked = bytearray(width + 1)
    for p in primes:
        residue = excluded[p]
        first = lo + ((residue - lo) % p)
        for x in range(first, lo + width + 1, p):
            blocked[x - lo] = 1
    return [lo + i for i, flag in enumerate(blocked) if not flag]


def run_code():
    primes = _primes(343)
    # Cold-start greedy feasible tuple, derived from the constraints alone.
    best = []
    occupied = {p: set() for p in primes}
    for x in range(200000):
        if all(len(occupied[p]) < p - 1 or x % p in occupied[p] for p in primes):
            best.append(x)
            for p in primes:
                occupied[p].add(x % p)
            if len(best) == 343:
                break
    if len(best) != 343:
        raise RuntimeError("failed to build feasible greedy seed")
    best.sort()
    missing = {p: next(r for r in range(p) if r not in occupied[p]) for p in primes}
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    seconds = min(45.0, max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45"))))
    deadline = time.monotonic() + seconds
    iterations = 0
    # Start with the exact missing residues of the greedy tuple. Each sieve
    # candidate is admissible because it avoids one residue for every prime.
    while time.monotonic() < deadline:
        iterations += 1
        best_span = best[-1] - best[0]
        target_width = max(342, best_span - rng.randint(1, 40))
        lo = rng.randint(best[0], best[-1] - target_width)
        excluded = dict(missing)
        # Repeated coordinate sweeps retain improvements on this interval.
        # Occasional random kicks move the search off local plateaus.
        current = len(_build(lo, target_width, primes, excluded))
        stale = 0
        while time.monotonic() < deadline and stale < 2 and current < 343:
            improved = False
            for p in rng.sample(primes, len(primes)):
                if time.monotonic() >= deadline:
                    break
                options = rng.sample(range(p), min(p, 12))
                options.append(excluded[p])
                scored = [(len(_build(lo, target_width, primes,
                                      {**excluded, p: r})), r) for r in options]
                count, residue = max(scored)
                if count > current:
                    excluded[p] = residue
                    current = count
                    improved = True
                    if current >= 343:
                        break
            if improved:
                stale = 0
            else:
                stale += 1
                p = rng.choice(primes)
                excluded[p] = rng.randrange(p)
        candidate = _build(lo, target_width, primes, excluded)
        if len(candidate) >= 343:
            candidate = candidate[:343]
            if candidate[-1] - candidate[0] < best_span:
                best = candidate
                missing = excluded
    return {"tuple": best, "search_iterations": iterations,
            "search_method": "excluded-residue sieve with coordinate sweeps and random kicks"}
