"""Independent reference witness loaded from task-local JSON data."""
import json
import os
from pathlib import Path


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T044-C01")
    filename = "public_29.json" if config_id == "T044-C01" else "public_30_32.json"
    data = json.loads((Path(__file__).parent / "data" / filename).read_text())
    if filename == "public_29.json":
        return data
    if config_id not in data:
        raise ValueError(f"unknown T044 configuration: {config_id}")
    return {"marks": data[config_id]["marks"]}
