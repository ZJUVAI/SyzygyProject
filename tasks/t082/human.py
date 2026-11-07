"""Reconstruct the published n=30 chart from Kamenetsky's OEIS file."""

import os
from pathlib import Path


SOURCE = Path(__file__).resolve().parent / "data" / "source" / "kamenetsky_2019.txt"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T082-C01") != "T082-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    marker = "a(30)>=131"
    try:
        start = lines.index(marker) + 1
    except ValueError as exc:
        raise ValueError("source does not contain the n=30 131-queen layout") from exc
    board = lines[start:start + 30]
    if len(board) != 30 or any(len(row) != 30 for row in board):
        raise ValueError("the n=30 source layout must be a 30x30 board")
    positions = {"white": [], "black": []}
    for row, line in enumerate(board):
        for column, cell in enumerate(line):
            if cell == "W":
                positions["white"].append([row, column])
            elif cell == "B":
                positions["black"].append([row, column])
            elif cell != ".":
                raise ValueError("unknown board symbol in source layout")
    return positions


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
