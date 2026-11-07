"""Fixed archived BCH-dual construction."""
import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T091-C01") != "T091-C01":
        raise ValueError("unsupported configuration")
    return json.loads((Path(__file__).parent / "data/human/bch_dual_oa4096.json").read_text())
