"""Return the frozen, independently replayable human D5 construction."""

import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T013-C01") != "T013-C01":
        raise ValueError("unknown T013 configuration")
    return json.loads((Path(__file__).parent / "data" / "d5_roots.json").read_text())
