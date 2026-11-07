"""Published human witness reproduced from Orrick et al. (2003)."""
import json
import os
from pathlib import Path


def _config_n():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T018-C01")
    try:
        return {"T018-C01": 29, "T018-C02": 27}[cid]
    except KeyError:
        raise ValueError(f"unknown T018 configuration: {cid}") from None


def run_code():
    n = _config_n()
    data = json.loads((Path(__file__).parent / "data" / f"human_order{n}.json").read_text())
    return {"matrix": [[1 if c == "+" else -1 for c in row] for row in data["matrix"]]}
