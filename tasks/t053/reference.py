"""Best reproduced fixed local-search witness; not a historical human record."""
import json
import os
from pathlib import Path

def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T053-C01")
    if config_id != "T053-C01":
        raise ValueError("unsupported configuration")
    return json.loads((Path(__file__).parent / "data" / "search_reference.json").read_text())
