"""Reconstruct the published 27-square quilt from its size row."""

import os
from pathlib import Path

from tasks.t070.construction import parse_published_sizes, skyline_decode


SOURCE_ROW = Path(__file__).resolve().parent / "data" / "source" / "pegg_2017_row_1000.txt"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T070-C01") != "T070-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return skyline_decode(parse_published_sizes(SOURCE_ROW))


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
