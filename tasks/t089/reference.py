"""Frozen reproduced human reference for T089-C01."""

import os


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T089-C01")
    if config_id != "T089-C01":
        raise ValueError(f"unknown T089 configuration: {config_id}")
    return {
        "coefficients": ["-1/1000", "-3/2", "1"],
        "reference": "H4 Gaussian plus a rational negative H0 term",
    }
