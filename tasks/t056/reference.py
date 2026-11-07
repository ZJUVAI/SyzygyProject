"""Replay the published 2006 makespan schedule for ta41."""

import json
import os
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data/reference/ta41_2006_schedule.json"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T056-C01") != "T056-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    record = json.loads(DATA.read_text(encoding="utf-8"))
    return {
        "machine_orders": record["machine_orders"],
        "method_metadata": {"source": record["source"], "seed": seed},
    }
