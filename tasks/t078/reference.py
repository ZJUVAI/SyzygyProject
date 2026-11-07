"""Load the frozen, independently transcribed Lambda_10 Gram witness."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T078-C01")
    if chosen != "T078-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).parent / "data/human/lambda10_gram.json"
    return {"gram": json.loads(path.read_text(encoding="utf-8"))["gram"]}
