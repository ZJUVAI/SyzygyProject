"""Uniform nonnegative step function on the fixed 480-cell support."""

import os


def run_code():
    # EVOLVE-BLOCK-START
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T087-C01")
    if config_id != "T087-C01":
        raise ValueError(f"unknown T087 configuration: {config_id}")
    heights = [1] * 480
    # EVOLVE-BLOCK-END
    return {"heights": heights}
