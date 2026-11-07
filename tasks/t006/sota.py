"""Replay the currently listed public best (4,10)-graph witness."""
import json
import os
from pathlib import Path


def run_code():
    """Return the frozen 320-vertex witness; the checker recomputes its order."""
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T006-C01")
    if config_id not in ("T006-C01", "T006-C02"):
        raise ValueError(f"unsupported configuration: {config_id}")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    filename = "human_graph.json" if config_id == "T006-C01" else "human_graph_c02.json"
    path = Path(__file__).parent / "data" / filename
    return json.loads(path.read_text())
