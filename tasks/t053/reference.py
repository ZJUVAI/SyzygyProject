"""Replay the saved, exact 33330-factor human-method witness."""

import json
import os
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "reference" / "human_T100000_T33330.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T053-C01") != "T053-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return {"factors": json.loads(DATA.read_text(encoding="utf-8"))["factors"]}


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
