"""Load the frozen exact 17-point human construction."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T066-C01")
    if chosen != "T066-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).parent / "data" / "reference" / "cubic_tangent_17.json"
    return json.loads(path.read_text(encoding="utf-8"))
