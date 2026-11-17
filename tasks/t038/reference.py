"""Reproduce the verified public 82-color Titiloye-Crispin witness."""

from pathlib import Path


def run_code():
    path = Path(__file__).parent / "data" / "source" / "DSJC1000.5_K82_col.txt"
    colors = [int(value) for value in path.read_text().split()]
    return {"colors": colors, "claimed_objective": 82}
