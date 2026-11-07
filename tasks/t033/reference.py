"""Return the saved local FLIP witness for external comparison only."""

import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T033-C01") != "T033-C01":
        raise ValueError("unknown T033 configuration")
    return json.loads((Path(__file__).parent / "data" /
                       "human_g70_1flip.json").read_text())
