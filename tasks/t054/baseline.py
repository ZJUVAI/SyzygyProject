"""Fixed-budget simulated annealing for configured-length aperiodic PSL."""

import math
import os
import random
import time

from tasks.t054.check import CONFIG_ID, config_length, aperiodic_autocorrelations

def _length():
    return config_length()


def _check_config_id():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen not in ("T054-C01", "T054-C02", "T054-C03"):
        raise ValueError(f"unsupported configuration: {chosen}")


def _peak(correlations):
    return max(abs(value) for value in correlations)


def _flip(sequence, correlations, position):
    old = sequence[position]
    length = len(sequence)
    deltas = [0] * length
    for lag in range(1, length):
        neighbor_sum = 0
        if position >= lag:
            neighbor_sum += sequence[position - lag]
        if position + lag < length:
            neighbor_sum += sequence[position + lag]
        deltas[lag] = -2 * old * neighbor_sum
        correlations[lag - 1] += deltas[lag]
    sequence[position] = -old
    return deltas


def run_code():
    _check_config_id()
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    restarts = int(os.environ.get("T054_SEARCH_RESTARTS", "12"))
    iterations = int(os.environ.get("T054_SEARCH_ITERATIONS", "3000"))
    if restarts < 0 or iterations < 1:
        raise ValueError("restarts must be nonnegative and iterations positive")
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None
    if seconds is not None:
        duration = float(seconds)
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + duration

    rng = random.Random(seed)
    length = _length()
    best_sequence = [1] * length
    best_psl = _peak(aperiodic_autocorrelations(best_sequence))
    proposals = 0
    completed_restarts = 0
    for _ in range(restarts):
        if deadline is not None and time.monotonic() >= deadline:
            break
        sequence = [rng.choice((-1, 1)) for _ in range(length)]
        correlations = aperiodic_autocorrelations(sequence)
        current_psl = _peak(correlations)
        if current_psl < best_psl:
            best_psl, best_sequence = current_psl, sequence.copy()
        for step in range(iterations):
            if deadline is not None and time.monotonic() >= deadline:
                break
            position = rng.randrange(length)
            deltas = _flip(sequence, correlations, position)
            proposed_psl = _peak(correlations)
            proposals += 1
            if proposed_psl <= current_psl:
                accept = True
            else:
                temperature = 1.5 * (1.0 - step / iterations) + 0.05
                accept = rng.random() < math.exp((current_psl - proposed_psl) / temperature)
            if accept:
                current_psl = proposed_psl
                if current_psl < best_psl:
                    best_psl, best_sequence = current_psl, sequence.copy()
            else:
                sequence[position] = -sequence[position]
                for lag in range(1, length):
                    correlations[lag - 1] -= deltas[lag]
        completed_restarts += 1

    return {
        "sequence": best_sequence,
        "search": {
            "algorithm": "single-bit-flip simulated annealing using exact integer autocorrelations",
            "seed": seed,
            "restart_limit": restarts,
            "restarts_completed": completed_restarts,
            "iterations_per_restart": iterations,
            "proposals": proposals,
            "reference_data_read": False,
        },
    }
