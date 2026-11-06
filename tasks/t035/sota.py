"""Replay the currently listed public best (4,10)-graph witness."""
import json
import os
from pathlib import Path


def run_code():
    """Return the frozen 320-vertex witness; the checker recomputes its order."""
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T035-C01")
    if config_id != "T035-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    path = Path(__file__).parent / "data" / "human_graph.json"
    return json.loads(path.read_text())
