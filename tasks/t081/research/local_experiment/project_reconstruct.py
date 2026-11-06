"""Rebuild the T081 208-bin project candidate from AlphaEvolve's signed 150-bin witness.

The cell-average projection is exact. SLSQP then minimizes the maximum absolute
full discrete convolution coefficient with the coefficient sum fixed at 208.
The floating-point optimizer is a heuristic; the saved decimal witness is
separately checked with exact Fraction arithmetic by check.py.
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).parent
N = 208
SOURCE = ROOT / "alphaevolve_signed150.json"
OUTPUT = ROOT / "project_refined208.json"


def project_cell_averages(values, target_n=N):
    source_n = len(values)
    projected = []
    for j in range(target_n):
        left, right = Fraction(j, target_n), Fraction(j + 1, target_n)
        integral = Fraction(0)
        for i, height in enumerate(values):
            overlap_left = max(left, Fraction(i, source_n))
            overlap_right = min(right, Fraction(i + 1, source_n))
            if overlap_right > overlap_left:
                integral += height * (overlap_right - overlap_left)
        projected.append(integral * target_n)
    return projected


def main():
    source = json.loads(SOURCE.read_text())
    values = [Fraction(value) for value in source["coefficients"]]
    projected = project_cell_averages(values)
    # Preserve total mass while fixing the SLSQP equality at sum(x)=208.
    initial = np.array([float(value) for value in projected], dtype=float)
    initial *= N / initial.sum()

    indices = np.arange(2 * N - 1)[:, None] - np.arange(N)[None, :]
    valid = (indices >= 0) & (indices < N)
    clipped = np.clip(indices, 0, N - 1)

    def conv(x):
        return np.convolve(x, x)

    def conv_jac(x):
        return np.where(valid, 2 * x[clipped], 0.0)

    def inequalities(x):
        values = conv(x[:-1])
        return np.r_[x[-1] - values, x[-1] + values]

    def inequality_jac(x):
        jac = conv_jac(x[:-1])
        return np.r_[np.c_[-jac, np.ones(2 * N - 1)],
                     np.c_[jac, np.ones(2 * N - 1)]]

    start = np.r_[initial, np.max(np.abs(conv(initial)))]
    result = minimize(
        lambda x: x[-1], start,
        jac=lambda x: np.r_[np.zeros(N), 1.0],
        constraints=[
            {"type": "eq", "fun": lambda x: x[:-1].sum() - N,
             "jac": lambda x: np.r_[np.ones(N), 0.0]},
            {"type": "ineq", "fun": inequalities, "jac": inequality_jac},
        ],
        method="SLSQP",
        options={"maxiter": 300, "ftol": 1e-11, "disp": True},
    )
    if not result.success:
        raise RuntimeError(f"SLSQP failed: {result.message}")
    coefficients = [format(float(value), ".15g") for value in result.x[:-1]]
    payload = {
        "provenance": "project_reconstruction",
        "source_witness": "alphaevolve_signed150.json",
        "method": "exact cell-average projection to 208 bins, then deterministic SLSQP min-max refinement",
        "coefficients": coefficients,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"iterations={result.nit}; approximate objective={result.fun:.16g}; output={OUTPUT}")


if __name__ == "__main__":
    main()
