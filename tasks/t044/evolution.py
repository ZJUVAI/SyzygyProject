"""Cold-start randomized search for distinct-difference rulers."""
import os
import random
import time


def _mark_count():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T044-C01")
    counts = {"T044-C01": 29, "T044-C02": 30, "T044-C03": 32}
    if config_id not in counts:
        raise ValueError(f"unknown T044 configuration: {config_id}")
    return counts[config_id]


def _valid(marks):
    used = set()
    for i, a in enumerate(marks):
        for b in marks[i + 1:]:
            d = b - a
            if d <= 0 or d in used:
                return False
            used.add(d)
    return True


def _grow(n, rng, deadline):
    marks = [0]
    used = set()
    while len(marks) < n:
        # Explore a small randomized window of legal next marks. The window
        # keeps growth compact while allowing independent cold starts.
        start = marks[-1] + 1
        legal = []
        for x in range(start, start + max(1000, 3 * len(marks))):
            ds = [x - y for y in marks]
            if len(set(ds)) == len(ds) and not (set(ds) & used):
                legal.append((x, ds))
                if len(legal) >= 3:
                    break
        if not legal:
            return None
        # Favor early marks, but sometimes accept a later choice to vary the
        # distance pattern and escape deterministic greedy prefixes.
        weights = [1.0 / ((x - start + 1) ** 2.5) for x, _ in legal]
        x, ds = rng.choices(legal, weights=weights, k=1)[0]
        marks.append(x)
        used.update(ds)
    return marks if len(marks) == n else None


def _greedy(n):
    """Guaranteed cold-start fallback using the earliest legal extension."""
    marks = [0]
    used = set()
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


def _shrink(marks, rng, deadline):
    """Try legal one-mark relocations, prioritizing span-reducing moves."""
    marks = list(marks)
    while time.monotonic() < deadline:
        marks.sort()
        span = marks[-1] - marks[0]
        moves = []
        # First test a shorter right endpoint. Then scan local moves that may
        # create a new arrangement from which the endpoint can move inward.
        candidates = [(len(marks) - 1, marks[-1] - 1)]
        for i in range(1, len(marks) - 1):
            candidates.extend(((i, marks[i] - 1), (i, marks[i] + 1)))
        for i, x in candidates:
            if x <= marks[i - 1] or (i + 1 < len(marks) and x >= marks[i + 1]):
                continue
            trial = marks[:]
            trial[i] = x
            if _valid(trial):
                new_span = max(trial) - min(trial)
                if new_span <= span:
                    moves.append((new_span, i, x))
        if not moves:
            break
        best_span = min(m[0] for m in moves)
        best_moves = [m for m in moves if m[0] == best_span]
        _, i, x = rng.choice(best_moves)
        marks[i] = x
        # A strict decrease is accepted immediately; equal-span steps are
        # limited to occasional neutral moves to allow endpoint unlocking.
        if best_span == span and rng.random() < 0.65:
            break
    return sorted(marks)


def run_code():
    n = _mark_count()
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    seconds = float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45"))
    deadline = time.monotonic() + max(0.0, min(seconds, 45.0))
    # Preserve a known-valid cold greedy ruler. Randomized starts only replace
    # it when they produce a strictly shorter valid construction.
    best = _greedy(n)
    while time.monotonic() < deadline:
        candidate = _grow(n, rng, deadline)
        if candidate is None:
            continue
        candidate = _shrink(candidate, rng, deadline)
        if _valid(candidate) and (best is None or candidate[-1] - candidate[0] < best[-1] - best[0]):
            best = candidate
    # A deterministic cold-start greedy result is usually available; retain
    # a valid construction even if an unusually short budget interrupts growth.
    if best is None or len(set(best)) != n or not _valid(best):
        raise RuntimeError("could not construct a valid ruler within the search budget")
    return {"marks": best}
