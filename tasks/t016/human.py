"""Reproduced admissible 208-step nonnegative human construction."""
import json
import os
from pathlib import Path


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T016-C01")
    if config_id != "T016-C01":
        raise ValueError("unsupported configuration: " + config_id)
    data = json.loads((Path(__file__).parent / "data" / "human_matolcsi_vinuesa.json").read_text())
    return {"coefficients": data["polynomial_coefficients"]}
