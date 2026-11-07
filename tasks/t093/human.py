"""Replay the published Shadoks 2304-value packing witness."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T093-C01")
    if chosen != "T093-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).resolve().parent / "data" / "source" / "shadoks2304.json"
    return json.loads(path.read_text(encoding="utf-8"))
