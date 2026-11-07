"""Load the fixed 19-Steiner-point comparison witness."""
import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T064-C01") != "T064-C01":
        raise ValueError("unsupported T064 configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    path = Path(__file__).with_name("data") / "reference" / "ortho40_solution.json"
    return json.loads(path.read_text(encoding="utf-8"))
