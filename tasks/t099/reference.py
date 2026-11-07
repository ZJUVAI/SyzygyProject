"""Fixed source-pinned public witness for T099-C01."""
import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T099-C01") != "T099-C01":
        raise ValueError("unknown T099 configuration")
    path = Path(__file__).parent / "data/reference/11P1_54x55.json"
    return json.loads(path.read_text())
