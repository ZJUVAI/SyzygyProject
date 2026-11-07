"""Replay the checked best-known public witness for each T005 configuration."""
import os

from tasks.t005.human import SOLUTIONS


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T005-C01")
    n_by_config = {"T005-C01": 11, "T005-C02": 12, "T005-C03": 16}
    try:
        n = n_by_config[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported T005 configuration: {config_id}") from exc
    return SOLUTIONS[n]
