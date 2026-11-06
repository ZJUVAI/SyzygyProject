"""Reproduced public P-192 chain from Clift's downloadable text file."""
import json
import os
from pathlib import Path

FILES = {
    "T097-C01": "human_t097.json",
    "T097-C02": "human_t097_c02.json",
    "T097-C03": "human_t097_c03.json",
}

def run_code():
    name = FILES.get(os.environ.get("MATHBENCH_CONFIG_ID", "T097-C01"))
    if name is None:
        raise ValueError("unsupported T097 configuration")
    return json.loads((Path(__file__).parent / "data" / name).read_text())
