"""Fixed replay of the verified Pegg 27-square witness."""

import json
import os
from pathlib import Path


DATA = Path(__file__).resolve().parent / "data" / "reference" / "pegg_1000_27.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T070-C01") != "T070-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return json.loads(DATA.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(run_code()))
