"""Simple valid all-positive seed; self-contained for cold exports."""
import os

_LENGTHS = {"T054-C01": 100, "T054-C02": 101, "T054-C03": 102}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T054-C01")
    try:
        length = _LENGTHS[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported configuration: {config_id}") from exc
    return {"sequence": [1] * length}
