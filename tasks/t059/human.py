"""Replay the published 80-vertex C2000.9 clique from Grosso et al. (2005)."""

import json
import os
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data/reference/human_2005_clique80.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T059-C01") != "T059-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    data = json.loads(DATA.read_text(encoding="utf-8"))
    return {"vertices": data["vertices"], "method_metadata": {"seed": seed, "published_value": 80}}
