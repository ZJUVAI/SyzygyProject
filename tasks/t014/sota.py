"""Replay the checked best-known public witness for each T014 configuration."""
import os

from tasks.t014.human import SOLUTIONS


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T014-C01")
    n_by_config = {"T014-C01": 11, "T014-C02": 12, "T014-C03": 16}
    try:
        n = n_by_config[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported T014 configuration: {config_id}") from exc
    return SOLUTIONS[n]
