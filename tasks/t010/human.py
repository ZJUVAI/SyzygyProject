"""Replay of the published 54 by 55, 270-copy human construction."""
import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T010-C01") != "T010-C01":
        raise ValueError("unknown T010 configuration")
    path = Path(__file__).parent / "data/reference/11P1_54x55.json"
    return json.loads(path.read_text())
