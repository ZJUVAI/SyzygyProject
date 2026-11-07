"""Seeded simulated annealing on a rational perturbation grid."""

from fractions import Fraction
import math
import os
import random


SCALE = 64
ITERATIONS = 12_000
POINT_COUNT = 12


def _ratio_parts(points):
    minimum = None
    maximum = 0
    for i in range(POINT_COUNT):
        for j in range(i + 1, POINT_COUNT):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            distance_squared = dx * dx + dy * dy
            if distance_squared == 0:
                return None
            minimum = distance_squared if minimum is None else min(minimum, distance_squared)
            maximum = max(maximum, distance_squared)
    return maximum, minimum


def _better(left, right):
    return left[0] * right[1] < right[0] * left[1]


def _accept(current, candidate, temperature, rng):
    current_value = current[0] / current[1]
    candidate_value = candidate[0] / candidate[1]
    if candidate_value < current_value:
        return True
    return rng.random() < math.exp((current_value - candidate_value) / temperature)


def _serialize(points):
    result = []
    for x, y in points:
        pair = []
        for coordinate in (x, y):
            value = Fraction(coordinate, SCALE)
            pair.append(value.numerator if value.denominator == 1 else str(value))
        result.append(pair)
    return result


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T081-C01")
    if chosen != "T081-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    try:
        seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    except ValueError as exc:
        raise ValueError("MATHBENCH_SEED must be an integer") from exc
    rng = random.Random(seed)
    current = [(x * SCALE, y * SCALE) for y in range(3) for x in range(4)]
    current_value = _ratio_parts(current)
    best = list(current)
    best_value = current_value
    completed = 0
    step_sizes = (1, 2, 4, 8, 16)
    for step in range(ITERATIONS):
        proposal = list(current)
        point_index = rng.randrange(POINT_COUNT)
        axis = rng.randrange(2)
        delta = rng.choice(step_sizes) * rng.choice((-1, 1))
        x, y = proposal[point_index]
        proposal[point_index] = (x + delta, y) if axis == 0 else (x, y + delta)
        candidate_value = _ratio_parts(proposal)
        completed += 1
        if candidate_value is None:
            continue
        if _better(candidate_value, best_value):
            best, best_value = list(proposal), candidate_value
        cycle_step = step % 2_000
        temperature = 0.01 + 0.12 * (1 - cycle_step / 2_000)
        if _accept(current_value, candidate_value, temperature, rng):
            current, current_value = proposal, candidate_value
    return {
        "points": _serialize(best),
        "search_metadata": {
            "algorithm": "single-point coordinate simulated annealing on the 1/64 rational grid",
            "seed": seed,
            "iterations_completed": completed,
            "grid_denominator": SCALE,
            "reference_data_read": False,
        },
    }
