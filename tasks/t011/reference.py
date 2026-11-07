"""Replay the frozen same-configuration public record when available."""
import json
import os
from pathlib import Path


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T011-C01")
    paths = {
        "T011-C01": "human_reference.json",
        "T011-C02": "reference_C7_4_100.json",
        "T011-C03": "CC_6_7_1120.txt",
    }
    try:
        name = paths[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported configuration: {config_id}") from exc
    path = Path(__file__).parent / "data" / ("reference" if config_id == "T011-C03" else "") / name
    if config_id != "T011-C03":
        path = Path(__file__).parent / "data" / name
        return json.loads(path.read_text())
    words = [list(map(int, line.split())) for line in path.read_text().splitlines() if line.strip()]
    return {"words": words}
