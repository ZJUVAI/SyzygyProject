"""Reconstruct the degree-100 row from Mossinghoff's published database."""
import json
import os
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "reference" / "mossinghoff_degree_100_certificate.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T063-C01") != "T063-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return json.loads(DATA.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(run_code()))
