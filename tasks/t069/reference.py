"""Load the frozen public best-known Nagata tour."""

import os
from pathlib import Path

from tasks.t069.human import _read_published_tour


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T069-C01")
    if chosen != "T069-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).parent / "data/reference/monalisa_5757191.tour"
    return _read_published_tour(path)
