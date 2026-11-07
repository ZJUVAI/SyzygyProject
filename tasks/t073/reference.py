"""Load the frozen rational D4 24-cell witness."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T073-C01")
    if chosen != "T073-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).parent / "data/human/d4_24cell.json"
    return json.loads(path.read_text(encoding="utf-8"))
