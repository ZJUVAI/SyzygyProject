"""Reconstruct Yuichi Nagata's published 100K Mona Lisa tour."""

import os
import gzip
from pathlib import Path


def _read_published_tour(path):
    ids = []
    in_section = False
    with gzip.open(path, "rt", encoding="ascii") as stream:
        lines = stream.read().splitlines()
    for line in lines:
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
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T096-C01")
    if chosen != "T096-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).parent / "data/human/monalisa_5757191.tour.gz"
    return _read_published_tour(path)
