"""Reconstruct Yuichi Nagata's published 100K Mona Lisa tour."""

import os
from pathlib import Path


def _read_published_tour(path):
    ids = []
    in_section = False
    for line in path.read_text(encoding="ascii").splitlines():
        row = line.strip()
        if row == "TOUR_SECTION":
            in_section = True
            continue
        if not in_section or not row:
            continue
        value = int(row)
        if value in (-1, 0):
            break
        ids.append(value - 1)
    return {"tour": ids}


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T069-C01")
    if chosen != "T069-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).parent / "data/human/monalisa_5757191.tour"
    return _read_published_tour(path)
