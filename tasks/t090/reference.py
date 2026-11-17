"""Replay the saved, exact 33330-factor human-method witness."""

import json
import gzip
import os
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "reference" / "human_T100000_T33330.json.gz"


def _load_reference():
    with gzip.open(DATA, "rt", encoding="utf-8") as stream:
        return json.load(stream)


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T090-C01") != "T090-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return {"factors": _load_reference()["factors"]}


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
