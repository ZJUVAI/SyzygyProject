"""Replay the fixed m=6,L=5 finite witness."""

import json
import os
from pathlib import Path


DATA = Path(__file__).resolve().parent / "data" / "reference" / "gyarmati_hennecart_ruzsa_m6_l5.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T080-C01") != "T080-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return {"set": json.loads(DATA.read_text(encoding="utf-8"))["set"]}


if __name__ == "__main__":
    print(json.dumps(run_code()))
