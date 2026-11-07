"""Warm-started tabu and perturbation search for LABS sequences."""
import json
import os
import random
import time
from pathlib import Path
import numpy as np

LENGTHS = {"T013-C01": 100, "T013-C02": 80, "T013-C03": 120}


def _state(seq):
    """Return exact integer energy, lag correlations, and flip neighbors."""
    n = len(seq)
    corr = np.array([sum(seq[i] * seq[i + k] for i in range(n-k))
                     for k in range(1, n)], dtype=np.int64)
    neighbors = np.zeros((n-1, n), dtype=np.int64)
    for row, k in enumerate(range(1, n)):
        if k < n:
            neighbors[row, :n-k] += seq[k:]
            neighbors[row, k:] += seq[:-k]
    return int(corr @ corr), corr, neighbors


def _saved_start(config, n):
    """Load the runner-provided, task-owned warm start for this configuration."""
    raw_path = os.environ.get("MATHBENCH_WARM_START")
    if not raw_path:
        return None
    try:
        payload = json.loads(Path(raw_path).read_text())
        if payload.get("config_id", config) != config:
            return None
        sequence = payload.get("sequence")
    except (OSError, ValueError, TypeError, AttributeError):
        return None
    if (isinstance(sequence, list) and len(sequence) == n
            and all(type(value) is int and value in (-1, 1) for value in sequence)):
        return np.asarray(sequence, dtype=np.int64)
    return None


def _pick_move(admissible, delta, rng):
    """Sample from the best few admissible moves to reduce deterministic cycling."""
    count = min(5, len(admissible))
    if count == 1:
        return int(admissible[0])
    values = delta[admissible]
    chosen = np.argpartition(values, count - 1)[:count]
    candidates = admissible[chosen]
    # Rank weights retain a strong preference for lower energy changes.
    order = np.argsort(delta[candidates], kind="stable")
    ranked = candidates[order]
    weights = [0.58 ** rank for rank in range(count)]
    return int(rng.choices(ranked.tolist(), weights=weights, k=1)[0])



def _best_pair(seq, corr, neighbors, delta):
    """Return the best simultaneous two-bit move, using exact integer deltas."""
    n = len(seq)
    pair = delta[:, None] + delta[None, :] + 8 * (seq[:, None] * seq[None, :]) * (neighbors.T @ neighbors)
    i, j = np.triu_indices(n, 1)
    lag = j - i - 1
    correction = 8 * seq[i] * seq[j] * (corr[lag] - 2 * seq[i] * neighbors[lag, i] - 2 * seq[j] * neighbors[lag, j]) + 16
    values = pair[i, j] + correction
    k = int(np.argmin(values))
    return int(i[k]), int(j[k]), int(values[k])

def _python_run_code():
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T013-C01")
    n = LENGTHS[config]
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "7301")))
    budget = float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS",
                                  os.environ.get("T013_SEARCH_SECONDS", "45")))
    deadline = time.monotonic() + max(0.1, budget)
    warm = _saved_start(config, n)
    if warm is None:
        best, best_score = None, float("inf")
    else:
        best = warm.copy()
        best_score, _, _ = _state(best)
    total_iterations = 0
    restarts = 0
    while time.monotonic() < deadline:
        restarts += 1
        if best is not None and rng.random() < 0.42:
            seq = best.copy()
            # A range of kick sizes moves between nearby basins and broad regions.
            flips = rng.randint(max(2, n // 40), max(5, n // 8))
            for position in rng.sample(range(n), flips):
                seq[position] *= -1
        else:
            seq = np.array([rng.choice((-1, 1)) for _ in range(n)], dtype=np.int64)
        score, corr, neighbors = _state(seq)
        local_best, local_score = seq.copy(), score
        tabu_until = np.zeros(n, dtype=np.int64)
        iteration = 0
        stall = 0
        chain_end = time.monotonic() + min(3.0, max(1.2, budget / 60))
        while time.monotonic() < deadline and time.monotonic() < chain_end:
            # Exact energy change for flipping each bit, computed together.
            delta = 4 * np.sum(neighbors * neighbors, axis=0) - 4 * seq * (corr @ neighbors)
            admissible = np.flatnonzero((tabu_until <= iteration) | (score + delta < best_score))
            if not len(admissible):
                admissible = np.arange(n)
            idx = _pick_move(admissible, delta, rng)
            old = int(seq[idx])
            changes = -2 * old * neighbors[:, idx].copy()
            score += int(delta[idx])
            corr += changes
            seq[idx] = -old
            # A flip changes the two neighboring products for each lag.
            for row, k in enumerate(range(1, n)):
                left, right = idx-k, idx+k
                if left >= 0:
                    neighbors[row, left] -= 2 * old
                if right < n:
                    neighbors[row, right] -= 2 * old
            tabu_until[idx] = iteration + rng.randint(max(3, n//12), max(5, n//8))
            iteration += 1
            total_iterations += 1
            if score < local_score:
                local_best, local_score, stall = seq.copy(), score, 0
            else:
                stall += 1
            if score < best_score:
                checked, _, _ = _state(seq)
                if checked != score:
                    raise RuntimeError("incremental LABS score mismatch")
                best, best_score = seq.copy(), checked
            if stall and stall % (2*n) == 0:
                pair_delta = 4 * np.sum(neighbors * neighbors, axis=0) - 4 * seq * (corr @ neighbors)
                a, b, change = _best_pair(seq, corr, neighbors, pair_delta)
                if change < 0:
                    old_score = score
                    seq[a] *= -1
                    seq[b] *= -1
                    score, corr, neighbors = _state(seq)
                    if score != old_score + change:
                        raise RuntimeError("two-bit LABS score mismatch")
                    if score < best_score:
                        best, best_score = seq.copy(), score
                    if score < local_score:
                        local_best, local_score = seq.copy(), score
                    stall = 0
            if stall >= 3*n:
                # Alternate local and global kicks to escape repeated plateaus.
                seq = local_best.copy()
                if best is not None and rng.random() < 0.35:
                    seq = best.copy()
                flips = rng.randint(max(2, n // 40), max(5, n // 10))
                for j in rng.sample(range(n), flips):
                    seq[j] *= -1
                score, corr, neighbors = _state(seq)
                stall = 0
                tabu_until.fill(iteration)
        if local_score < best_score:
            checked, _, _ = _state(local_best)
            if checked != local_score:
                raise RuntimeError("incremental LABS score mismatch")
            best, best_score = local_best.copy(), checked
    checked, _, _ = _state(best)
    if checked != best_score:
        raise RuntimeError("final LABS score mismatch")
    return {"sequence": best.tolist(), "search_iterations": total_iterations,
            "search_method": "exact tabu with exhaustive two-bit descent and multibit perturbations",
            "_evolution": {"iterations": total_iterations, "restarts": restarts,
                           "budget_seconds": budget, "warm_start_used": warm is not None}}


def run_code():
    """Compile the integer search kernel inside a temporary task-run folder."""
    import subprocess
    import tempfile
    import shutil
    if shutil.which("g++") is None:
        return _python_run_code()
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T013-C01")
    n = LENGTHS[config]
    seed = int(os.environ.get("MATHBENCH_SEED", "7301"))
    budget = max(0.1, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    started = time.monotonic()
    warm = _saved_start(config, n)
    if warm is None:
        rng = random.Random(seed)
        warm = np.array([rng.choice((-1, 1)) for _ in range(n)], dtype=np.int64)
    run_dir = Path(__file__).resolve().parent / "runs"
    run_dir.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="labs_kernel_", dir=run_dir) as folder:
        executable = str(Path(folder) / "labs")
        subprocess.run(["g++", "-O3", "-std=c++17", str(Path(__file__).with_name("search_labs.cpp")), "-o", executable], check=True, capture_output=True, timeout=min(30, budget+10))
        remaining = max(.01, budget-(time.monotonic()-started)-.1)
        result = subprocess.run([executable, str(remaining), str(seed)], input=str(n)+"\n"+" ".join(map(str,warm.tolist()))+"\n", text=True, capture_output=True, check=True, timeout=remaining+5)
    numbers = list(map(int,result.stdout.split()))
    score, iterations, restarts = numbers[:3]
    best = np.array(numbers[3:], dtype=np.int64)
    if len(best)!=n or _state(best)[0]!=score:
        raise RuntimeError("compiled LABS energy mismatch")
    return {"sequence":best.tolist(), "search_iterations":iterations,
            "search_method":"compiled exact integer tabu with elite basin restarts",
            "_evolution":{"iterations":iterations,"restarts":restarts,"budget_seconds":budget,"warm_start_used":os.environ.get("MATHBENCH_WARM_START") is not None}}
