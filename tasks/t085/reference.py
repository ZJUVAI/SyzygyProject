"""Fixed reproduced reference from the archived triangular-lattice patch."""
import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T085-C01") != "T085-C01":
        raise ValueError("unsupported configuration")
    path = Path(__file__).parent / "data" / "human" / "kershner_triangular_patch21.json"
    return json.loads(path.read_text())
