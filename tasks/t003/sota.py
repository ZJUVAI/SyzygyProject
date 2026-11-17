"""Fixed exact witnesses for the best public upper bounds checked for T003."""
import json
import os
import gzip
from pathlib import Path


_WITNESSES = {
    "T003-C01": "data/human_friedman_1997.json",
}


def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T003-C01")
    try:
        name = _WITNESSES[cid]
    except KeyError as exc:
        raise ValueError(f"unknown T003 configuration: {cid}") from exc
    path = Path(__file__).parent / name
    data = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
    return json.loads(data)
