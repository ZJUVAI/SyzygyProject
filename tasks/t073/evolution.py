"""Vectorized tabu search for low-autocorrelation binary sequences."""
import os
import random
import time
import numpy as np

LENGTHS = {"T073-C01": 100, "T073-C02": 80, "T073-C03": 120}


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


def run_code():
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T073-C01")
    n = LENGTHS[config]
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "7301")))
    deadline = time.monotonic() + max(0.1, float(os.environ.get("T073_SEARCH_SECONDS", "45")))
    best, best_score = None, float("inf")
    while time.monotonic() < deadline:
        seq = np.array([rng.choice((-1, 1)) for _ in range(n)], dtype=np.int64)
        score, corr, neighbors = _state(seq)
        local_best, local_score = seq.copy(), score
        tabu_until = np.zeros(n, dtype=np.int64)
        iteration = 0
        stall = 0
        chain_end = time.monotonic() + 1.2
        while time.monotonic() < deadline and time.monotonic() < chain_end:
            # Exact energy change for flipping each bit, computed together.
            delta = 4 * np.sum(neighbors * neighbors, axis=0) - 4 * seq * (corr @ neighbors)
            admissible = np.flatnonzero((tabu_until <= iteration) | (score + delta < best_score))
            if not len(admissible):
                admissible = np.arange(n)
            idx = int(admissible[np.argmin(delta[admissible])])
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
            if score < local_score:
                local_best, local_score, stall = seq.copy(), score, 0
            else:
                stall += 1
            if score < best_score:
                checked, _, _ = _state(seq)
                if checked != score:
                    raise RuntimeError("incremental LABS score mismatch")
                best, best_score = seq.copy(), checked
            if stall >= 3*n:
                # Restart near the chain best to escape a long plateau.
                seq = local_best.copy()
                flips = max(2, n//20)
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
    return {"sequence": best.tolist()}
