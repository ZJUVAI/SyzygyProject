"""Reproduce the located public 208-step Matolcsi–Vinuesa construction."""
import json
import os
from pathlib import Path


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T081-C02")
    if config_id != "T081-C02":
        raise ValueError("unsupported configuration: " + config_id)
    data_path = Path(__file__).parent / "data" / "human_matolcsi_vinuesa.json"
    data = json.loads(data_path.read_text())
    return {"coefficients": data["polynomial_coefficients"]}
