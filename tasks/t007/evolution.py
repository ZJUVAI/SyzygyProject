"""Warm-started mutation search for distinct-difference rulers."""
import math
import json
import os
import random
import time


def _mark_count():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T007-C01")
    counts = {"T007-C01": 29, "T007-C02": 30, "T007-C03": 32}
    if config_id not in counts:
        raise ValueError(f"unknown T007 configuration: {config_id}")
    return counts[config_id]


def _valid(marks):
    if len(marks) != len(set(marks)) or any(type(x) is not int for x in marks):
        return False
    marks = sorted(marks)
    used = set()
    for i, a in enumerate(marks):
        for b in marks[i + 1:]:
            d = b - a
            if d in used:
                return False
            used.add(d)
    return True


def _greedy(n):
    marks, used = [0], set()
    while len(marks) < n:
        x = marks[-1] + 1
        while True:
            ds = [x - y for y in marks]
            if len(set(ds)) == len(ds) and not (set(ds) & used):
                marks.append(x)
                used.update(ds)
                break
            x += 1
    return marks


def _load_start(n):
    path = os.environ.get("MATHBENCH_WARM_START")
    if not path:
        return None
    raw = json.loads(open(path, encoding="utf-8").read())
    marks = raw.get("marks") if isinstance(raw, dict) else None
    if not isinstance(marks, list) or len(marks) != n or not _valid(marks):
        raise ValueError("warm start is not a valid ruler of the configured size")
    marks = sorted(marks)
    return [x - marks[0] for x in marks]


def _prime_factors(value):
    factors = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    return factors


def _singer_ruler(q, wanted):
    """Build a Singer cyclic difference set from GF(q^3), then cut its circle."""
    modulus = q * q + q + 1
    field_order = q ** 3
    factors = _prime_factors(field_order - 1)

    # Elements are triples (constant, x, x^2), reduced by x^3 = -a*x-b.
    def add(u, v):
        return tuple((u[i] + v[i]) % q for i in range(3))

    def mul(u, v, a, b):
        c = [0] * 5
        for i in range(3):
            for j in range(3):
                c[i + j] += u[i] * v[j]
        for k in (4, 3):
            c[k - 3] -= b * c[k]
            c[k - 2] -= a * c[k]
        return tuple(c[i] % q for i in range(3))

    def power(base, exponent, a, b):
        out = (1, 0, 0)
        while exponent:
            if exponent & 1:
                out = mul(out, base, a, b)
            base = mul(base, base, a, b)
            exponent >>= 1
        return out

    # A cubic is irreducible exactly when it has no root in F_q.
    chosen = None
    for a in range(q):
        for b in range(q):
            if all((x * x * x + a * x + b) % q for x in range(q)):
                chosen = (a, b)
                break
        if chosen:
            break
    if chosen is None:
        raise RuntimeError("could not find an irreducible cubic")
    a, b = chosen

    generator = None
    for c0 in range(q):
        for c1 in range(q):
            for c2 in range(q):
                candidate = (c0, c1, c2)
                if candidate == (0, 0, 0):
                    continue
                if all(power(candidate, (field_order - 1) // p, a, b) != (1, 0, 0)
                       for p in factors):
                    generator = candidate
                    break
            if generator:
                break
        if generator:
            break
    if generator is None:
        raise RuntimeError("could not find a primitive field element")

    # Trace(g^i) has zero constant coordinate precisely on the Singer hyperplane.
    points = []
    value = (1, 0, 0)
    q2 = q * q
    for i in range(modulus):
        trace = add(add(value, power(value, q, a, b)), power(value, q2, a, b))
        if trace[0] == 0:
            points.append(i)
        value = mul(value, generator, a, b)
    if len(points) != q + 1:
        raise RuntimeError(f"Singer hyperplane has {len(points)} points, expected {q + 1}")

    residues = set(points)
    cyclic_differences = [(x - y) % modulus for x in points for y in points if x != y]
    if len(set(cyclic_differences)) != modulus - 1 or set(cyclic_differences) != set(range(1, modulus)):
        raise RuntimeError("Singer set failed exact cyclic difference verification")

    # Cut after a largest circular gap. For C01, test every one-point deletion.
    best = None
    # Multipliers preserve cyclic differences but change the largest gap.
    for multiplier in range(1, modulus):
        if math.gcd(multiplier, modulus) != 1:
            continue
        transformed = sorted((multiplier * x) % modulus for x in points)
        selections = [transformed]
        if wanted == q:
            selections = [transformed[:i] + transformed[i + 1:] for i in range(len(transformed))]
        for ordered in selections:
            gaps = [(ordered[(i + 1) % len(ordered)] - ordered[i]) % modulus
                    for i in range(len(ordered))]
            i = max(range(len(gaps)), key=gaps.__getitem__)
            span = modulus - gaps[i]
            if best is None or span < best[-1]:
                start = ordered[(i + 1) % len(ordered)]
                best = sorted((x - start) % modulus for x in ordered)
    if best is None or len(best) != wanted:
        raise RuntimeError("could not cut Singer set into a valid ruler")
    return best


def _rebuild(current, rng, deadline):
    """Remove several marks and refill with legal positions under a shorter cap."""
    cap = current[-1] - rng.choice((0, 0, 1, 2))
    width = rng.choice((2, 3, 4))
    removed = set(rng.sample(range(1, len(current)), width))
    if cap < current[-1]:
        removed.add(len(current) - 1)
    fixed = [x for i, x in enumerate(current) if i not in removed]
    used = {b-a for i, a in enumerate(fixed) for b in fixed[i+1:]}
    nodes = [0]
    def fill(marks, differences):
        if len(marks) == len(current):
            return sorted(marks)
        positions = list(range(1, cap + 1))
        rng.shuffle(positions)
        for x in positions:
            nodes[0] += 1
            if nodes[0] > 1800 or time.monotonic() >= deadline:
                return None
            ds = [abs(x-y) for y in marks]
            if 0 in ds or len(set(ds)) != len(ds) or differences.intersection(ds):
                continue
            result = fill(marks + [x], differences.union(ds))
            if result is not None:
                return result
        return None
    return fill(fixed, used)


def run_code():
    n = _mark_count()
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    seconds = max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    deadline = time.monotonic() + seconds
    best = _load_start(n) or _greedy(n)
    q = {29: 29, 30: 29, 32: 31}[n]
    singer = _singer_ruler(q, n)
    if singer[-1] < best[-1]:
        best = singer
    current = best[:]
    best_span = best[-1]
    iterations = accepted = 0
    while time.monotonic() < deadline:
        iterations += 1
        current_span = current[-1]
        if iterations % 4 == 0:
            rebuilt = _rebuild(current, rng, deadline)
            if rebuilt is not None:
                current = rebuilt
                if rebuilt[-1] < best_span:
                    best, best_span = rebuilt[:], rebuilt[-1]
            continue
        trial = current[:]
        # Include the right endpoint so legal proposals can shorten the ruler.
        count = 1 if rng.random() < 0.78 else 2
        for i in rng.sample(range(1, n), count):
            trial[i] = rng.randint(1, max(1, current_span - 1))
        trial.sort()
        if len(set(trial)) != n or not _valid(trial):
            continue
        span = trial[-1]
        if span < best_span:
            best, best_span = trial, span
            current, accepted = trial[:], accepted + 1
        elif span <= current_span or rng.random() < 0.001:
            current, accepted = trial, accepted + 1
        # Periodically restart at the best known ruler to keep progress.
        if iterations % 5000 == 0:
            current = best[:]
    if not _valid(best):
        raise RuntimeError("search lost its valid ruler")
    return {"marks": best, "search_method": "Singer multiplier/deletion family and bounded multi-mark exact refill",
            "search_iterations": iterations, "accepted_moves": accepted}
