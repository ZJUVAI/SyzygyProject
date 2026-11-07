"""Self-contained valid seed with six elements in one color."""

import os


# EVOLVE-BLOCK-START
def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T034-C01") != "T034-C01":
        raise ValueError("unsupported configuration id")
    return {"n": 6, "colors": [0, 0, 0, 0, 0, 0]}
# EVOLVE-BLOCK-END
