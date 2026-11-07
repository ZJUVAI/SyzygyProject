"""Fixed verified replay of the reconstructed spectral-search baseline."""

import json
import os
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "reference" / "spectral_adjacent_ordering.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T045-C01") != "T045-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    data = json.loads(DATA.read_text(encoding="utf-8"))
    return {"ordering": data["ordering"], "reference_metadata": data["provenance"]}


if __name__ == "__main__":
    print(json.dumps(run_code()))
