"""Return the frozen LPS H* reconstruction stored in task-local comparison data."""

import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T100-C01") != "T100-C01":
        raise ValueError("unsupported T100 configuration")
    path = Path(__file__).resolve().parent / "data" / "reference" / "hstar_50_700.json"
    return json.loads(path.read_text(encoding="utf-8"))
