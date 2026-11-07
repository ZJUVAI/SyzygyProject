"""Fast exact-delta single-spin simulated annealing for periodic energy."""

import math
import random

from tasks.t090.check import LENGTH


def correlations(sequence):
    return [
        sum(sequence[index] * sequence[(index + shift) % LENGTH] for index in range(LENGTH))
        for shift in range(LENGTH)
    ]


def energy(corr):
    return sum(value * value for value in corr[1:])


def flip_deltas(sequence, corr, index):
    deltas = [0] * LENGTH
    for shift in range(1, LENGTH):
        left = sequence[index] * sequence[(index + shift) % LENGTH]
        right = sequence[(index - shift) % LENGTH] * sequence[index]
        deltas[shift] = -2 * (left + right)
    delta_energy = sum(
        2 * corr[shift] * deltas[shift] + deltas[shift] * deltas[shift]
        for shift in range(1, LENGTH)
    )
    return deltas, delta_energy


def anneal(sequence, rng, steps=6000, start_temperature=20.0, end_temperature=0.2):
    current = list(sequence)
    corr = correlations(current)
    current_energy = energy(corr)
    best = list(current)
    best_energy = current_energy
    for step in range(steps):
        fraction = step / max(1, steps - 1)
        temperature = start_temperature * (end_temperature / start_temperature) ** fraction
        index = rng.randrange(LENGTH)
        deltas, change = flip_deltas(current, corr, index)
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current[index] = -current[index]
            for shift in range(1, LENGTH):
                corr[shift] += deltas[shift]
            current_energy += change
            if current_energy < best_energy:
                best, best_energy = list(current), current_energy
    # Deterministic exact one-bit descent from the best state found.
    improved = True
    while improved:
        improved = False
        best_move = None
        for index in range(LENGTH):
            deltas, change = flip_deltas(best, correlations(best), index)
            if change < 0 and (best_move is None or change < best_move[0]):
                best_move = (change, index, deltas)
        if best_move is not None:
            change, index, deltas = best_move
            best[index] = -best[index]
            corr = correlations(best)
            best_energy += change
            improved = True
    return best, best_energy
