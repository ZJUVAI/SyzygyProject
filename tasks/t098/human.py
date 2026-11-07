"""Rebuild the published order-38 Williams construction from its B-code."""
import os
from pathlib import Path
from tasks.t098.builder import tile_bouwkamp_line


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T098-C01") != "T098-C01":
        raise ValueError("unsupported T098 configuration")
    path = Path(__file__).parent / "data" / "source" / "williams_38_352A.bkp"
    return tile_bouwkamp_line(path.read_text(encoding="utf-8").strip())
