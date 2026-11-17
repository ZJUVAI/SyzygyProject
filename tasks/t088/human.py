"""Reproduced public P-192 chain from Clift's downloadable text file."""
import json
import os
from pathlib import Path

FILES = {
    "T088-C01": "human_t088.json",
}

def run_code():
    name = FILES.get(os.environ.get("MATHBENCH_CONFIG_ID", "T088-C01"))
    if name is None:
        raise ValueError("unsupported T088 configuration")
    return json.loads((Path(__file__).parent / "data" / name).read_text())
