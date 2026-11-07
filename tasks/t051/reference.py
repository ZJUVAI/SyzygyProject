"""Frozen same-parameter public comparison witness."""

from pathlib import Path


def run_code():
    path = Path(__file__).with_name("data") / "reference" / "sequence_130000.txt"
    signs = path.read_text(encoding="ascii").strip()
    if len(signs) != 130000 or set(signs) - {"+", "-"}:
        raise ValueError("reference witness must contain exactly 130000 signs")
    return {"sequence": [1 if sign == "+" else -1 for sign in signs]}
