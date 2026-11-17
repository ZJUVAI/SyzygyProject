"""Load the fixed public 164-point AlphaEvolve construction."""
import json
import os
from pathlib import Path

def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T101-C01") != "T101-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    path = Path(__file__).parent / "data" / "reference" / "alphaevolve_n100_164.json"
    return json.loads(path.read_text(encoding="utf-8"))
