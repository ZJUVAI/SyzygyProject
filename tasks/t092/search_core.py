"""Seeded search in a small exact zonal-harmonic basis; samples are feedback only."""
from fractions import Fraction
import math
import os
import random

from tasks.t092.init_program import run_code as init_run


def _bases():
    pz = [Fraction(v) for v in init_run()["coefficients"]]
    exponents = [(a, b, 20 - a - b) for a in range(20, -1, -1) for b in range(20 - a, -1, -1)]
    index = {exp: i for i, exp in enumerate(exponents)}
    px = [Fraction(0)] * len(exponents)
    py = [Fraction(0)] * len(exponents)
    for value, (a, b, c) in zip(pz, exponents):
        px[index[(c, b, a)]] = value
        py[index[(a, c, b)]] = value
    return [px, py, pz]


def _legendre20(x):
    prev, cur = 1.0, x
    for n in range(1, 20):
        prev, cur = cur, ((2 * n + 1) * x * cur - n * prev) / (n + 1)
    return cur


def _feedback(weights, count=3072):
    sums2 = sums4 = 0.0
    golden = math.pi * (3.0 - math.sqrt(5.0))
    for i in range(count):
        z = 1.0 - 2.0 * (i + 0.5) / count
        radius = math.sqrt(max(0.0, 1.0 - z * z))
        theta = golden * i
        x, y = radius * math.cos(theta), radius * math.sin(theta)
        value = weights[0] * _legendre20(x) + weights[1] * _legendre20(y) + weights[2] * _legendre20(z)
        square = value * value
        sums2 += square
        sums4 += square * square
    m2, m4 = sums2 / count, sums4 / count
    return (m4 / (m2 * m2)) ** 0.25 if m2 > 0 else 0.0


def _combine(bases, weights):
    coeffs = [sum((basis[i] * weight for basis, weight in zip(bases, weights)), Fraction(0))
              for i in range(len(bases[0]))]
    return [str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
            for value in coeffs]


def search(iterations, evolutionary=False):
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    bases = _bases()
    current = [0, 0, 1]
    current_score = _feedback(current)
    best, best_score = current[:], current_score
    accepted = proposals = 0
    for step in range(int(iterations)):
        proposals += 1
        if evolutionary and step % 4 == 3:
            trial = [rng.randint(-4, 4) for _ in range(3)]
        else:
            trial = current[:]
            coordinate = rng.randrange(3)
            trial[coordinate] += rng.choice((-4, -3, -2, -1, 1, 2, 3, 4))
        if not any(trial):
            continue
        score = _feedback(trial)
        if score > best_score:
            best, best_score = trial[:], score
        if score >= current_score or rng.random() < 0.05:
            current, current_score = trial, score
            accepted += 1
    return {
        "coefficients": _combine(bases, best),
        "search_metadata": {
            "seed": seed,
            "basis": "rotated degree-20 Legendre zonal harmonics along x, y, and z axes",
            "iterations_requested": int(iterations),
            "proposals_evaluated": proposals,
            "moves_accepted": accepted,
            "sphere_sample_points_for_feedback_only": 3072,
            "comparison_data_read": False,
            "objective_certificate": "Trusted checker recomputes exact sphere moments."
        }
    }
