"""Cold start for Gset G70. This file has no task-package dependencies."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T033-C01") != "T033-C01":
        raise ValueError("unknown T033 configuration")
    # EVOLVE-BLOCK-START
    labels = [0] * 10000
    # EVOLVE-BLOCK-END
    return {"labels": labels}
