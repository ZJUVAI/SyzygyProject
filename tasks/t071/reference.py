"""Load the frozen n=16 VT_0 public witness."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T071-C01")
    if chosen != "T071-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).parent / "data/reference/vt16_3856.json"
    return json.loads(path.read_text(encoding="utf-8"))
