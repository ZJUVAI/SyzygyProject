"""Cold-start local search for a binary [68, 15] linear code.

The search keeps the generator systematic, so every returned matrix has full
rank.  It enumerates all nonzero codewords exactly and uses one-coordinate
parity mutations with incremental weight updates.
"""
import os
import random
import time

import numpy as np


N, K = 68, 15
WORDS = 1 << K


def _initial(seed):
    rng = random.Random(seed)
    rows = []
    for i in range(K):
        row = 1 << i
        for col in range(K, N):
            if rng.getrandbits(1):
                row |= 1 << col
        rows.append(row)
    return rows


def _state(rows):
    """Return bit values by word/coordinate, word weights, and histogram."""
    values = np.zeros((WORDS, N), dtype=np.uint8)
    for index in range(1, WORDS):
        bit = index & -index
        previous = index ^ bit
        row = rows[bit.bit_length() - 1]
        for col in range(N):
            values[index, col] = values[previous, col] ^ ((row >> col) & 1)
    weights = values.sum(axis=1, dtype=np.uint16)
    histogram = np.bincount(weights, minlength=N + 1).astype(np.int32)
    return values, weights, histogram


def _lex_key(histogram):
    # A weight-count vector is the complete low-weight spectrum.  Minimize
    # counts in increasing weight order, which first maximizes minimum distance.
    return tuple(int(x) for x in histogram[1:])


def _energy(histogram):
    # Metropolis guidance: distance dominates, then the number of words at d.
    d = next(w for w in range(1, N + 1) if histogram[w])
    return -100.0 * d + float(histogram[d]) / WORDS


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T066-C01") != "T066-C01":
        raise ValueError("unsupported configuration: T066-C01")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    try:
        budget = max(0.0, min(45.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45"))))
    except (TypeError, ValueError):
        budget = 45.0
    deadline = time.monotonic() + budget
    rng = random.Random(seed)

    rows = _initial(seed)
    values, weights, histogram = _state(rows)
    best_rows = rows[:]
    best_key = _lex_key(histogram)
    current_energy = _energy(histogram)
    iteration = 0

    while time.monotonic() < deadline:
        # Restart occasionally to preserve broad coverage of the matrix space.
        if iteration and iteration % 1800 == 0:
            rows = _initial(rng.getrandbits(64))
            values, weights, histogram = _state(rows)
            current_energy = _energy(histogram)

        row = rng.randrange(K)
        col = rng.randrange(K, N)
        affected = np.arange(1 << row, WORDS, 1 << (row + 1))
        affected = np.concatenate([affected + offset for offset in range(1 << row)])
        old_bits = values[affected, col]
        old_weights = weights[affected]
        new_weights = old_weights + (1 - 2 * old_bits.astype(np.int16))

        trial_hist = histogram.copy()
        trial_hist += np.bincount(new_weights, minlength=N + 1).astype(np.int32)
        trial_hist -= np.bincount(old_weights, minlength=N + 1).astype(np.int32)
        trial_key = _lex_key(trial_hist)
        trial_energy = _energy(trial_hist)

        # Cool within each restart.  Equal-score moves are useful for escaping
        # plateaus; occasional one-step distance losses permit basin changes.
        temperature = max(0.25, 2.5 * (1.0 - (iteration % 1800) / 1800.0))
        delta = trial_energy - current_energy
        take = trial_key < _lex_key(histogram)
        if not take and delta <= 0:
            take = True
        elif not take and rng.random() < np.exp(-delta / temperature):
            take = True

        if take:
            values[affected, col] ^= 1
            weights[affected] = new_weights
            rows[row] ^= 1 << col
            histogram = trial_hist
            current_energy = trial_energy
            if trial_key < best_key:
                best_rows = rows[:]
                best_key = trial_key
        iteration += 1

    matrix = [[(row >> col) & 1 for col in range(N)] for row in best_rows]
    return {"generator_matrix": matrix}


if __name__ == "__main__":
    print(run_code())
