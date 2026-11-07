"""Rebuild Laderman's 23-product decomposition from Lille's Maple tensor source."""
import bz2
import re
from pathlib import Path

_SOURCE = Path(__file__).parent / "data" / "source" / "3x3x3_tensor.mpl.bz2"
_SYMBOLS = {"0": 0, "1": 1, "-1": -1, "l": 1, "-l": -1, "1/l": 1, "-1/l": -1}


def _matrix(block):
    rows = re.findall(r"\[([^\[\]]*)\]", block)
    if len(rows) != 3:
        raise ValueError("unexpected Maple matrix row count")
    out = []
    for row in rows:
        entries = [value.strip() for value in row.split(",")]
        if len(entries) != 3 or any(value not in _SYMBOLS for value in entries):
            raise ValueError("unexpected Maple matrix entry")
        out.extend(_SYMBOLS[value] for value in entries)
    return out


def run_code():
    source = bz2.decompress(_SOURCE.read_bytes()).decode("ascii")
    source = source[source.index("Tensor:="):]
    matrices = re.findall(r"Matrix\(3, 3, \[(.*?)\]\)", source)
    if len(matrices) != 69:
        raise ValueError("Lille tensor source must contain 69 factor matrices")
    factors = [_matrix(block) for block in matrices]
    terms = []
    for index in range(23):
        alpha, beta, third = factors[3 * index:3 * index + 3]
        # Lille writes scalar * Transpose(third) into the output matrix.
        gamma = [third[3 * col + row] for row in range(3) for col in range(3)]
        terms.append({"alpha": alpha, "beta": beta, "gamma": gamma})
    return {"terms": terms}
