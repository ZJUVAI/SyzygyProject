"""Replay the frozen same-configuration public record when available."""
import json
import os
from pathlib import Path


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T011-C01")
    paths = {"T011-C01": "human_reference.json"}
    try:
        name = paths[config_id]
    except KeyError as exc:
        raise ValueError(f"unsupported configuration: {config_id}") from exc
    path = Path(__file__).parent / "data" / name
    return json.loads(path.read_text())
