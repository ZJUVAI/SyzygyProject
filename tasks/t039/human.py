"""Replay the published FPGA-search construction archived with this task."""
from pathlib import Path


def run_code():
    path = Path(__file__).resolve().parent / "data" / "shehadeh_kingsford_kschischang_7_5_112.txt"
    rows = [[int(value) for value in line.split()]
            for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {"rows": rows}
