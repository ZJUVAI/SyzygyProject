"""Rebuild Mark Lewko's residue-class construction at N=42025."""

import os

N = 42025
MODULUS = 205
RESIDUES = (7, 21, 50, 64, 76, 83, 106, 120, 139, 182, 193, 199)


def build_human_set():
    return {
        "elements": sorted(
            1 + residue + MODULUS * block
            for residue in RESIDUES
            for block in range(MODULUS)
        )
    }


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T062-C01")
    if chosen != "T062-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return build_human_set()
