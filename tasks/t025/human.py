"""Rebuild the affine Calderbank–Fishburn cap from Edel's public matrix."""

from pathlib import Path


def run_code():
    rows = (Path(__file__).parent / "data" / "edel_bierbrauer_248_projective_matrix.txt").read_text().splitlines()
    if len(rows) != 8 or any(len(row) != 248 or set(row) - set("012") for row in rows):
        raise ValueError("the saved public projective matrix has an invalid format")
    return {
        "points": [[int(rows[i][column]) for i in range(7)]
                   for column, last_coordinate in enumerate(rows[7])
                   if last_coordinate == "1"]
    }
