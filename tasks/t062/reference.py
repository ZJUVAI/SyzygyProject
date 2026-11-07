"""Load the frozen reconstructed Lewko construction for T062."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T062-C01")
    if chosen != "T062-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).parent / "data" / "reference" / "lewko205_n42025.json"
    return json.loads(path.read_text(encoding="utf-8"))
