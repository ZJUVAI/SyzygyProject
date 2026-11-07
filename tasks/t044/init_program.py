"""Self-contained, deliberately simple connected graph seed."""

import os


# EVOLVE-BLOCK-START
def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T044-C01") != "T044-C01":
        raise ValueError("unsupported configuration id")
    return {"n": 1, "edges": []}
# EVOLVE-BLOCK-END
