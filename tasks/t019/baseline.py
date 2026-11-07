from mathbench.search import search_deadline, search_steps
"""Seeded greedy construction and bounded interval-shrinking search."""
import os
import random
import time


def _primes(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i : n + 1 : i] = b"\x00" * (((n - i * i) // i) + 1)
    return [p for p, flag in enumerate(sieve) if flag]


def _admissible(values, primes):
    for p in primes:
        if len({x % p for x in values}) == p:
            return False
    return True


def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T019-C01")
    try: k = {"T019-C01":343,"T019-C02":1000,"T019-C03":3000}[cid]
    except KeyError: raise ValueError(f"unsupported T019 configuration: {cid}") from None
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    primes = _primes(k)
    if k != 343:
        from tasks.t019.init_program import run_code as cold_start
        best = cold_start()["tuple"]
        best_span = max(best)-min(best)
        # A small number of full exact-feasibility proposals scales to k=3000.
        for _ in range(3):
            candidate = best[:]
            i = rng.randrange(k)
            candidate[i] = rng.randrange(min(best), max(best)+1)
            if len(set(candidate)) == k and _admissible(candidate, primes):
                span = max(candidate)-min(candidate)
                if span < best_span: best,best_span=candidate,span
        return {"tuple":best}
    if k == 343:
        values = []
        occupied = {p: set() for p in primes}
        # Preserve the original accepted C01 greedy start.
        for x in range(200000):
            if all(len(occupied[p]) < p - 1 or x % p in occupied[p] for p in primes):
                values.append(x)
                for p in primes: occupied[p].add(x % p)
                if len(values) == k: break
        if len(values) != k: raise RuntimeError("greedy construction did not find k entries")
    else:
        # New configurations share the finite-span, reference-free cold seed.
        from tasks.t019.init_program import run_code as cold_start
        values = cold_start()["tuple"]
    # Restarted random interval search gives actual objective improvements when
    # it finds a feasible replacement. All checks cover the full prime domain.
    budget = max(0.0, float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2")))
    deadline = search_deadline()
    best = values[:]
    best_diameter = max(best) - min(best)
    for _attempt in search_steps(20):
        lo, hi = min(best), max(best)
        width = best_diameter
        # Local coordinate descent can change the objective in one accepted
        # step: propose a new integer near either current endpoint, then keep
        # it only when the entire finite prime set remains admissible.
        candidate = best[:]
        index = rng.randrange(k)
        candidate[index] = rng.randrange(lo, hi + 1)
        if len(set(candidate)) == k and _admissible(candidate, primes):
            score = max(candidate) - min(candidate)
            if score < best_diameter:
                best, best_diameter = candidate, score
                continue
        left = rng.randrange(lo, hi + 1)
        right = min(hi, left + rng.randrange(max(1, width // 2), width + 1))
        pool = [x for x in best if left <= x <= right]
        pool.extend(rng.randrange(left, right + 1) for _ in range(k))
        candidate = []
        for x in sorted(set(pool)):
            if _admissible(candidate + [x], primes):
                candidate.append(x)
                if len(candidate) == k:
                    break
        if len(candidate) == k:
            score = max(candidate) - min(candidate)
            if score < best_diameter:
                best, best_diameter = candidate, score
    return {"tuple": best}
