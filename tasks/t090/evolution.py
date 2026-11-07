"""Task-qualified evolution entry point for T090."""

import os

from tasks.t090 import baseline


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T090-C01")
    if chosen != "T090-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return baseline.run_code()
