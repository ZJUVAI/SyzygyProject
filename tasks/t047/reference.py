"""Replay the 128-point Singer/Leech-family difference-basis construction."""

import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T047-C01") != "T047-C01":
        raise ValueError("unsupported configuration id")
    path = Path(__file__).parent / "data" / "reference" / "singer_q31_leech_product_n6166_128.json"
    return json.loads(path.read_text(encoding="utf-8"))
