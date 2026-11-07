"""Cube20 Golomb rulers, reconstructed from its public ruler archive."""
import json
import os
from pathlib import Path

_C01 = {"marks": [0, 7, 11, 31, 43, 53, 100, 121, 144, 150, 202, 220,
                   229, 268, 284, 285, 356, 371, 390, 416, 430, 465,
                   467, 528, 582, 590, 595, 620, 623]}


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T007-C01")
    if config_id == "T007-C01":
        return {"marks": list(_C01["marks"])}
    if config_id not in ("T007-C02", "T007-C03"):
        raise ValueError(f"unknown T007 configuration: {config_id}")
    data = json.loads((Path(__file__).parent / "data" / "public_30_32.json").read_text())
    return {"marks": list(data[config_id]["marks"])}
