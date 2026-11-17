"""Simple valid all-positive seed; self-contained for cold exports."""
import os

_LENGTH = 100


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T054-C01")
    if config_id != "T054-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    return {"sequence": [1] * _LENGTH}
