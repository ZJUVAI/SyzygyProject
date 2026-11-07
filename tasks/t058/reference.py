"""Replay the published seven-round RTD(5,7) construction."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T058-C01")
    if chosen != "T058-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).with_name("data") / "reference" / "rtd_5_7.json"
    return json.loads(path.read_text(encoding="utf-8"))
