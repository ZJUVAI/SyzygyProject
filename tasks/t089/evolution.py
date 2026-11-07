"""Expanded fixed-iteration search entry for the shared runner."""

import os

from tasks.t089.baseline import run_search


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T089-C01")
    if config_id != "T089-C01":
        raise ValueError(f"unknown T089 configuration: {config_id}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    coefficients, metadata = run_search(seed=seed, steps=300)
    return {"coefficients": [str(value) for value in coefficients],
            **metadata,
            "search_method": "evolutionary seeded perturbation of H4 and H8 Gaussian modes"}
