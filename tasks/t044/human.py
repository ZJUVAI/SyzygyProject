"""Replay the published 70-vertex Alegre-Fiol-Yebra graph witness."""

from pathlib import Path

from tasks.t044.witness import load_upper_triangle as _load_upper_triangle


def run_code():
    path = Path(__file__).parent / "data" / "reference" / "afy_70_adjlist_nx.txt"
    return _load_upper_triangle(path)
