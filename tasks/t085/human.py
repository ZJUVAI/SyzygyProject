"""Published human witness reproduced from Orrick et al. (2003)."""
import json
import os
from pathlib import Path


def _config_n():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T085-C01")
    if cid != "T085-C01":
        raise ValueError(f"unknown T085 configuration: {cid}")
    return 29


def run_code():
    n = _config_n()
    data = json.loads((Path(__file__).parent / "data" / f"human_order{n}.json").read_text())
    return {"matrix": [[1 if c == "+" else -1 for c in row] for row in data["matrix"]]}
