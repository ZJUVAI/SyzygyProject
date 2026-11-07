"""Search for narrow admissible k-tuples with residue-mask updates."""
import json
import os
import random
import time


def _primes(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i:n + 1:i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i, flag in enumerate(sieve) if flag]


def _missing(values, primes):
    if len(values) < 2 or any(type(x) is not int for x in values):
        return None
    if len(set(values)) != len(values):
        return None
    out = {}
    for p in primes:
        used = {x % p for x in values}
        if len(used) == p:
            return None
        out[p] = next(r for r in range(p) if r not in used)
    return out


def _bit_count(value):
    return bin(value).count("1")

def _interval_counts(lo, width, primes, excluded):
    """Return coverage counts for numbers blocked by selected residues."""
    counts = [0] * (width + 1)
    for p in primes:
        first = lo + ((excluded[p] - lo) % p)
        for x in range(first, lo + width + 1, p):
            counts[x - lo] += 1
    return counts


def _candidate(lo, counts):
    return [lo + i for i, count in enumerate(counts) if count == 0]


def _coordinate_update(lo, counts, width, p, old, new):
    first = lo + ((old - lo) % p)
    for x in range(first, lo + width + 1, p):
        counts[x - lo] -= 1
    first = lo + ((new - lo) % p)
    for x in range(first, lo + width + 1, p):
        counts[x - lo] += 1


def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T019-C01")
    try: k = {"T019-C01":343,"T019-C02":1000,"T019-C03":3000}[cid]
    except KeyError: raise ValueError(f"unsupported T019 configuration: {cid}") from None
    primes = _primes(k)
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    seconds = min(240.0, max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45"))))
    deadline = time.monotonic() + seconds

    # Only a path explicitly supplied by the experiment runner is read.
    # The runner points this to the task's own best solution.
    best = None
    warm_path = os.environ.get("MATHBENCH_WARM_START")
    if warm_path:
        try:
            with open(warm_path, "r", encoding="utf-8") as stream:
                warm = json.load(stream).get("tuple")
            if _missing(warm, primes) is not None:
                best = sorted(warm)
        except (OSError, ValueError, TypeError):
            pass

    # Keep the accepted C01 fallback; new configs start from the finite-span
    # self-contained seed so score conversion never sees huge integers.
    if best is None and k == 343:
        occupied = {p: set() for p in primes}
        values = []
        for x in range(200000):
            if all(len(occupied[p]) < p - 1 or x % p in occupied[p] for p in primes):
                values.append(x)
                for p in primes: occupied[p].add(x % p)
                if len(values) == k: break
        if len(values) != k: raise RuntimeError("failed to construct a feasible seed")
        best = sorted(values)
    elif best is None:
        from tasks.t019.init_program import run_code as cold_start
        best = cold_start()["tuple"]

    missing = _missing(best, primes)
    iterations = 0
    elites = {}
    while time.monotonic() < deadline:
        iterations += 1
        span = best[-1]-best[0]
        width = max(k-1, span-2)
        lo = best[0] + rng.choice((-8,-6,-4,-2,0,2,4,6,8))
        key = (lo, width)
        full = (1 << (width+1))-1
        masks = {}
        for p in primes:
            masks[p] = []
            for r in range(p):
                mask = 0
                for i in range((r-lo) % p, width+1, p):
                    mask |= 1 << i
                masks[p].append(mask)
        excluded = dict(elites[key][1]) if key in elites else dict(missing)
        # Coordinated kicks release two or three prime constraints together.
        for p in rng.sample(primes[2:], rng.choice((2, 3, 5))):
            excluded[p] = rng.randrange(p)
        stale = 0
        for sweep in range(35):
            if time.monotonic() >= deadline:
                break
            changed = False
            order = rng.sample(primes, len(primes))
            active = [masks[p][excluded[p]] for p in order]
            # Prefix/suffix unions exclude one prime without a full resieve.
            prefix = [0]
            for mask in active:
                prefix.append(prefix[-1] | mask)
            suffix = [0]*(len(order)+1)
            for j in range(len(order)-1, -1, -1):
                suffix[j] = suffix[j+1] | active[j]
            for j,p in enumerate(order):
                others = prefix[j] | suffix[j+1]
                available = full & ~others
                old = excluded[p]
                losses = [_bit_count(available & mask) for mask in masks[p]]
                minimum = min(losses)
                choices = [r for r,cost in enumerate(losses) if cost == minimum]
                new = rng.choice(choices)
                if losses[new] < losses[old] or (new != old and rng.random()<.2):
                    excluded[p] = new
                    active[j] = masks[p][new]
                    changed = True
                # Update the prefix for changes already made this sweep.
                prefix[j+1] = prefix[j] | active[j]
            # Jointly optimize two residue exclusions. Their overlapping
            # losses can make a two-prime move profitable even when neither
            # one-prime move improves the number of available integers.
            if sweep % 3 == 2:
                p, q = rng.sample(primes[1:15], 2)
                others = 0
                for prime in primes:
                    if prime not in (p, q):
                        others |= masks[prime][excluded[prime]]
                available = full & ~others
                left = [available & mask for mask in masks[p]]
                right = [available & mask for mask in masks[q]]
                left_cost = [_bit_count(mask) for mask in left]
                right_cost = [_bit_count(mask) for mask in right]
                best_pair = None
                best_cost = width+2
                ties = 0
                for r, first in enumerate(left):
                    for t, second in enumerate(right):
                        cost = left_cost[r]+right_cost[t]-_bit_count(first & second)
                        if cost < best_cost:
                            best_cost, best_pair, ties = cost, (r, t), 1
                        elif cost == best_cost:
                            ties += 1
                            if rng.randrange(ties) == 0:
                                best_pair = (r, t)
                excluded[p], excluded[q] = best_pair
            blocked = 0
            for p in primes:
                blocked |= masks[p][excluded[p]]
            free = full & ~blocked
            free_count = _bit_count(free)
            if key not in elites or free_count > elites[key][0]:
                elites[key] = (free_count, dict(excluded))
            if free_count >= k:
                values = []
                while free:
                    bit = free & -free
                    values.append(lo+bit.bit_length()-1)
                    free ^= bit
                # Pick the narrowest consecutive k survivors, including both fringes.
                start = min(range(len(values)-k+1), key=lambda i: values[i+k-1]-values[i])
                candidate = values[start:start+k]
                if candidate[-1]-candidate[0] < span:
                    if _missing(candidate, primes) is None:
                        raise RuntimeError("bitset residue search lost admissibility")
                    best = candidate
                    missing = _missing(best, primes)
                    elites.clear()
                break
            stale = 0 if changed else stale+1
            if stale >= 2 or sweep % 10 == 9:
                for p in rng.sample(primes[2:], 2):
                    excluded[p] = rng.randrange(p)
                stale = 0
    return {"tuple": best, "search_iterations": iterations,
            "search_method": "persistent near-feasible interval elites, exact two-prime updates, symmetric shifts and kicks"}
