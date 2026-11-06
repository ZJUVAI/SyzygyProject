"""Fixed exact witnesses for the best public upper bounds checked for T002."""
import json
import os
from pathlib import Path


_WITNESSES = {
    "T002-C01": "data/human_friedman_1997.json",
    "T002-C03": "data/sota_n029_pingyou_2026.json",
    "T002-C04": "data/human_gobel_figure1.json",
}


def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T002-C01")
    try:
        name = _WITNESSES[cid]
    except KeyError as exc:
        raise ValueError(f"unknown T002 configuration: {cid}") from exc
    return json.loads((Path(__file__).parent / name).read_text())
