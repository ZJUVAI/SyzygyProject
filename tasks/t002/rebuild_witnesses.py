"""Offline reconstruction of staged T002 human witnesses.

Run from the repository root with the standard library:
    .venv/bin/python tasks/t002/rebuild_witnesses.py
An alternate retained Schadt corner witness may be supplied as the first argument.
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

from tasks.t002.check import Q

TASK_DIR = Path(__file__).resolve().parent
DEFAULT_SCHADT_SOURCE = TASK_DIR / "data" / "source_schadt_n029_rational.yaml"


def yaml_scalar(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] == "'":
        text = text[1:-1]
    return Fraction(text)


def read_schadt_corners(path):
    """Read only corner coordinate pairs from the source's simple YAML sequence."""
    lines = Path(path).read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == "squares:")
    squares = []
    current = []
    in_squares = False
    for line in lines[start + 1:]:
        if line.startswith("  - id:"):
            if current:
                if len(current) != 4:
                    raise ValueError("source square does not have four corner pairs")
                squares.append(current)
            current = []
            in_squares = True
            continue
        if in_squares and line.startswith("  ") and not line.startswith("    "):
            break
        if line.startswith("    - - "):
            current.append([yaml_scalar(line[len("    - - "):])])
        elif line.startswith("      - ") and current and len(current[-1]) == 1:
            current[-1].append(yaml_scalar(line[len("      - "):]))
    if current:
        if len(current) != 4:
            raise ValueError("source square does not have four corner pairs")
        squares.append(current)
    if len(squares) != 29:
        raise ValueError(f"expected 29 source squares, found {len(squares)}")
    return squares


def write_schadt(path):
    squares = []
    for corners in read_schadt_corners(path):
        x = sum((p[0] for p in corners), Fraction()) / 4
        y = sum((p[1] for p in corners), Fraction()) / 4
        dx = corners[1][0] - corners[0][0]
        dy = corners[1][1] - corners[0][1]
        t = dy / (1 + dx)
        squares.append({"x": str(x), "y": str(y), "t": str(t)})
    out = TASK_DIR / "data" / "human_schadt_2025.json"
    out.write_text(json.dumps({"squares": squares}, indent=2) + "\n")


def write_gobel():
    q = Q.parse
    root = Q(0, 1)
    half = q("1/2")
    a = 5
    side = q(a + 1) + root / 2
    squares = []
    for i in range(a):
        for j in range(a - i):
            squares.append({"x": str(q(i) + half), "y": str(q(j) + half), "t": "0"})
    for i in range(a):
        for j in range(a - i):
            squares.append({"x": str(side - q(i) - half), "y": str(side - q(j) - half), "t": "0"})
    squares.extend([
        {"x": str(side - half), "y": str(half), "t": "0"},
        {"x": str(half), "y": str(side - half), "t": "0"},
    ])
    m = 6
    for k in range(m):
        d = q(2 * k - (m - 1)) * root / 2
        squares.append({"x": str((side + d) / 2), "y": str((side - d) / 2), "t": str(root - 1)})
    if len(squares) != 38:
        raise ValueError("Göbel family reconstruction produced the wrong count")
    out = TASK_DIR / "data" / "human_gobel_figure1.json"
    out.write_text(json.dumps({"squares": squares}, indent=2) + "\n")


if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SCHADT_SOURCE
    write_schadt(source)
    write_gobel()
