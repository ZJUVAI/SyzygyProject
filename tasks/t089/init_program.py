"""Small exact polynomial-Gaussian starting point."""

import os


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T089-C01")
    if config_id != "T089-C01":
        raise ValueError(f"unknown T089 configuration: {config_id}")
    # EVOLVE-BLOCK-START
    return {
        "coefficients": ["-1/4", "-3/2", "1"],
        "method": "self-Fourier fourth Hermite mode with a negative constant",
    }
    # EVOLVE-BLOCK-END
