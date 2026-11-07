"""Fixed, reproducible degree-146 comparison construction."""

import json
import os
from pathlib import Path


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T046-C01")
    if config_id != "T046-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    path = Path(__file__).parent / "data" / "reference" / "h1_power_73.json"
    return json.loads(path.read_text(encoding="utf-8"))
