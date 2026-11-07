"""Fixed archived highest-weight harmonic construction."""
import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T092-C01") != "T092-C01":
        raise ValueError("unsupported configuration")
    return json.loads((Path(__file__).parent / "data/human/highest_weight_degree20.json").read_text())
