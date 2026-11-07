"""Self-contained, deliberately small valid construction for T042."""

import os


# EVOLVE-BLOCK-START
def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T042-C01") != "T042-C01":
        raise ValueError("unsupported configuration id")
    return {"elements": [1]}
# EVOLVE-BLOCK-END
