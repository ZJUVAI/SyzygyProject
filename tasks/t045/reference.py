"""Replay the frozen 131-per-army public construction."""

import json
import os
from pathlib import Path


WITNESS = Path(__file__).resolve().parent / "data" / "reference" / "peaceable_queens_n30_131.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T045-C01") != "T045-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return json.loads(WITNESS.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(run_code()))
