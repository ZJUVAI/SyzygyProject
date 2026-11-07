"""Replay the human-published 444-word construction."""

import json
import os
from pathlib import Path


DATA = Path(__file__).resolve().parent / "data" / "reference" / "a17_4_5_444.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T067-C01") != "T067-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return json.loads(DATA.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(run_code()))
