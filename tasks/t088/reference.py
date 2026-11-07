"""Fixed best-reproduced comparison witness, separate from the public bound."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T088-C01")
    if chosen != "T088-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    witness = Path(__file__).resolve().parent / "data" / "reference" / "grasp_reconstruction_229.json"
    return json.loads(witness.read_text(encoding="utf-8"))
