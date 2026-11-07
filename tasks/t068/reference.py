"""Load the frozen 120-word public length-10 code from OEIS A000983."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T068-C01")
    if chosen != "T068-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).parent / "data" / "reference" / "oeis_a000983_n10.json"
    words = json.loads(path.read_text(encoding="utf-8"))["codewords"]
    return {"codewords": [int(word, 2) for word in words]}
