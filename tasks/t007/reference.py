"""Independent reference witness loaded from task-local JSON data."""
import json
import os
from pathlib import Path


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T007-C01")
    if config_id != "T007-C01":
        raise ValueError(f"unknown T007 configuration: {config_id}")
    filename = "public_29.json"
    data = json.loads((Path(__file__).parent / "data" / filename).read_text())
    return data
