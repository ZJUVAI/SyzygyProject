"""Load the conservatively scaled, source-derived reference witness."""
import json
import os
from pathlib import Path

def run_code():
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T005-C01")
    filename = "human26.json" if config == "T005-C01" else "human32.json"
    return json.loads((Path(__file__).parent / "data" / filename).read_text())
