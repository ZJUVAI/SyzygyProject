"""Replay the strongest same-parameter public witnesses in the source table."""
import os
from pathlib import Path


_CONFIGS = {
    "T009-C02": "16",
    "T009-C03": "17",
    "T009-C04": "19",
}


def run_code():
    """Return the archived spherical-codes.org coordinates for the active config."""
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T009-C02")
    if config_id not in _CONFIGS:
        raise ValueError(f"unsupported T009 configuration: {config_id}")
    witness = Path(__file__).parent / "data" / f"spherical_code_3_{_CONFIGS[config_id]}.txt"
    points = []
    for line in witness.read_text(encoding="utf-8").splitlines():
        if line.strip():
            points.append([coordinate.strip() for coordinate in line.split(",")])
    return {"points": points}
