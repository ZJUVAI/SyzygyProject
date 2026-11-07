"""Reconstruct the length-64 sequence printed by Tyler and Loftsson."""

import json
import os
from pathlib import Path


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T090-C01")
    if chosen != "T090-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    asset = Path(__file__).resolve().parent / "data" / "source" / "tyler_loftsson_64.json"
    encoded = json.loads(asset.read_text(encoding="utf-8"))["hex_sequence"]
    bits = bin(int(encoded, 16))[2:].zfill(64)
    sequence = [1 if bit == "1" else -1 for bit in bits]
    return {
        "sequence": sequence,
        "source_metadata": {
            "hex_sequence": encoded,
            "encoding": "64-bit hexadecimal, most-significant bit first; 1 maps to +1, 0 maps to -1",
            "reported_energy": 240,
            "reported_peak_sidelobe": 4,
        },
    }
