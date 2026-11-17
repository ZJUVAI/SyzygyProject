"""Read Comellas's fixed 2024 Coxeter-graph construction of order 70."""

from pathlib import Path

from tasks.t031.witness import load_upper_triangle as _load_upper_triangle


def run_code():
    path = Path(__file__).parent / "data" / "reference" / "coxeter_70_adjlist_nx.txt"
    return _load_upper_triangle(path)
