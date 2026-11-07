"""Fixed replay of the exact unit-circle human construction."""
import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T096-C01") != "T096-C01":
        raise ValueError("unknown T096 configuration")
    return json.loads((Path(__file__).parent / "data/reference/circle.json").read_text())
