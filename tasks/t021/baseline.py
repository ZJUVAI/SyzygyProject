"""Deterministic perturb-and-keep search baseline; no reference data access."""

import json
import math
import os
import random

from mathbench.search import search_steps


def _xyz(pair):
    u, v = pair
    d = 1.0 + u * u + v * v
    return (2.0 * u / d, 2.0 * v / d, (1.0 - u * u - v * v) / d)


def _energy(points):
    xyz = [_xyz(p) for p in points]
    total = 0.0
    for i in range(len(xyz)):
        for j in range(i):
            d2 = sum((xyz[i][k] - xyz[j][k]) ** 2 for k in range(3))
            total += 1.0 / math.sqrt(d2)
    return total


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T021-C01")
    lengths = {"T021-C01": 32, "T021-C02": 40, "T021-C03": 50}
    if config_id not in lengths: raise ValueError(f"unsupported configuration: {config_id}")
    n = lengths[config_id]
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    requested_seconds_value = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    requested_seconds = float(requested_seconds_value) if requested_seconds_value is not None else None
    points = []
    golden = math.pi * (3.0 - math.sqrt(5.0))
    for k in range(n):
        z = 1.0 - 2.0 * (k + 0.5) / n
        theta = k * golden
        r = math.sqrt(1.0 - z * z)
        points.append([r * math.cos(theta) / (1.0 + z), r * math.sin(theta) / (1.0 + z)])
    current = points
    current_energy = _energy(current)
    best = [p[:] for p in current]
    best_energy = current_energy
    # Fixed 600-step coordinate perturbation. The ambient coordinates are
    # reprojected by the exact checker; energy here is search feedback only.
    actual_iterations = 0
    for step in search_steps(600):
        actual_iterations += 1
        candidate = [p[:] for p in current]
        index = rng.randrange(n)
        temperature = 0.03 * (1.0 - step / 700.0)
        candidate[index][0] += rng.gauss(0.0, temperature)
        candidate[index][1] += rng.gauss(0.0, temperature)
        score = _energy(candidate)
        if score < best_energy:
            best, best_energy = [p[:] for p in candidate], score
        if score < current_energy or rng.random() < math.exp(min(0.0, (current_energy - score) / max(temperature, 1e-9))):
            current, current_energy = candidate, score
    return {
        "points": best,
        "search_metadata": {
            "algorithm": "seeded coordinate perturbation with simulated-annealing acceptance and best-witness retention",
            "seed": seed,
            "actual_iterations": actual_iterations,
            "iteration_budget": 600,
            "requested_seconds": requested_seconds,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run_code()))
