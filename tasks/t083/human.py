"""Replay the published unrestricted discrepancy-3 construction."""

from pathlib import Path
import gzip


def run_code():
    path = Path(__file__).with_name("data") / "source" / "sequence_130000.txt.gz"
    with gzip.open(path, "rt", encoding="ascii") as stream:
        signs = stream.read().strip()
    if len(signs) != 130000 or set(signs) - {"+", "-"}:
        raise ValueError("source witness must contain exactly 130000 signs")
    return {"sequence": [1 if sign == "+" else -1 for sign in signs]}
