"""Reproduced public P-192 chain from Clift's downloadable text file."""
import json
import os
from pathlib import Path

FILES = {
    "T020-C01": "human_t020.json",
    "T020-C02": "human_t020_c02.json",
    "T020-C03": "human_t020_c03.json",
}

def run_code():
    name = FILES.get(os.environ.get("MATHBENCH_CONFIG_ID", "T020-C01"))
    if name is None:
        raise ValueError("unsupported T020 configuration")
    return json.loads((Path(__file__).parent / "data" / name).read_text())
