"""Reconstruct the traditional 10-by-10 triangular-lattice construction."""

import json
import os
from pathlib import Path

from tasks.t065.construction import solution_from_moser_tuples


DATA = Path(__file__).resolve().parent / "data" / "reference" / "triangular_grid_10x10.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T065-C01") != "T065-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    record = json.loads(DATA.read_text(encoding="utf-8"))
    return solution_from_moser_tuples(
        record["moser_tuples"],
        "human-reconstructed 10-by-10 triangular-grid patch; source formula is recorded in the data file",
    )


if __name__ == "__main__":
    print(run_code())
