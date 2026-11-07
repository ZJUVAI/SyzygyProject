"""Rebuild a classical fourth-Hermite polynomial-Gaussian example."""

import os


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T089-C01")
    if config_id != "T089-C01":
        raise ValueError(f"unknown T089 configuration: {config_id}")
    # In t=pi*x^2, H_4(sqrt(2t))/64 = t^2 - 3t/2 + 3/16.
    # Subtracting 3/16 + 1/1000 keeps the function self-Fourier and makes
    # both values at the origin strictly negative.
    return {
        "coefficients": ["-1/1000", "-3/2", "1"],
        "method": "published Hermite-Gaussian eigenfunction, reconstructed with exact rational coefficients",
    }
