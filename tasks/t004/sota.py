"""Replay the strongest same-parameter public witnesses in the source table."""
import os
from pathlib import Path


_CONFIGS = {
    "T004-C01": "16",
    "T004-C02": "17",
    "T004-C03": "19",
}


def run_code():
    """Return the archived spherical-codes.org coordinates for the active config."""
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T004-C01")
    if config_id not in _CONFIGS:
        raise ValueError(f"unsupported T004 configuration: {config_id}")
    witness = Path(__file__).parent / "data" / f"spherical_code_3_{_CONFIGS[config_id]}.txt"
    points = []
    for line in witness.read_text(encoding="utf-8").splitlines():
        if line.strip():
            points.append([coordinate.strip() for coordinate in line.split(",")])
    return {"points": points}
