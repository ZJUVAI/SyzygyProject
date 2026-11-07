"""Simple valid seed: give each vertex its own color."""

import os


# EVOLVE-BLOCK-START
def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T030-C01") != "T030-C01":
        raise ValueError("unsupported configuration id")
    return {"colors": list(range(1000))}
# EVOLVE-BLOCK-END
