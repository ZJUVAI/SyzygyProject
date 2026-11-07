"""Seeded single-bit annealing search; does not load human data."""
import math
import os
import random

from tasks.t013.init_program import run_code as initial
from tasks.t013.check import aperiodic_autocorrelations


def _energy(sequence):
    return sum(c * c for c in aperiodic_autocorrelations(sequence))


def run_code():
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    current = initial()["sequence"]
    current_energy = _energy(current)
    best, best_energy = current[:], current_energy
    steps = int(os.environ.get("MATHBENCH_SEARCH_STEPS", "4000"))
    start_temp, end_temp = 12.0, 0.15
    for step in range(max(0, steps)):
        candidate = current[:]
        index = rng.randrange(len(candidate))
        candidate[index] *= -1
        value = _energy(candidate)
        fraction = step / max(1, steps - 1)
        temperature = start_temp * (end_temp / start_temp) ** fraction
        delta = value - current_energy
        if delta <= 0 or rng.random() < math.exp(-delta / temperature):
            current, current_energy = candidate, value
        if current_energy < best_energy:
            best, best_energy = current[:], current_energy
    return {"sequence": best}
