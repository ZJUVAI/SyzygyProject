"""Reconstructed Giffler-Thompson active-schedule construction with LPT rule."""

import os
from tasks.t056.dispatch import generate_active_schedule


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T056-C01") != "T056-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    return {
        "machine_orders": generate_active_schedule(seed=seed, rule="lpt"),
        "method_metadata": {
            "algorithm": "Giffler-Thompson active schedule generation; longest processing time within the conflict set",
            "seed": seed,
            "iterations": 1,
        },
    }
