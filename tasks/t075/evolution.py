"""Task-qualified evolution entry point for T075."""

import os

from tasks.t075 import baseline


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T075-C01")
    if chosen != "T075-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return baseline.run_code()
