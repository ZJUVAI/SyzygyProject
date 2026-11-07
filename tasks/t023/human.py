"""Reproduce NIST's IPOG-F covering array, completing '-' as zero."""
from pathlib import Path


def run_code():
    lines = (Path(__file__).parent / "data/nist_ca_t4_v2_k20.txt").read_text().splitlines()
    rows = [[0 if x == "-" else int(x) for x in line.split()]
            for line in lines[1:] if line.strip()]
    return {"array": rows}
