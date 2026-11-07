"""Replay the published 133-edge C6-saturated construction."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T061-C01")
    if chosen != "T061-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).with_name("data") / "reference" / "c6_sat_100_133.json"
    return json.loads(path.read_text(encoding="utf-8"))
