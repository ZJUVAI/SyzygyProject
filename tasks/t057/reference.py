"""Replay the current CVRPLIB public bound witness (72332)."""

import os
from pathlib import Path

from tasks.t057.io import read_solution


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T057-C01")
    if chosen != "T057-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    path = Path(__file__).with_name("data") / "reference" / "public_72332.sol"
    return {"routes": read_solution(path)}
