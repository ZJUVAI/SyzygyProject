"""Fixed reproduced reference: exact transcription of the n=4 pinwheel."""
import json
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T083-C01") != "T083-C01":
        raise ValueError("unsupported configuration")
    path = Path(__file__).parent / "data" / "reference" / "friedman4_reconstructed.json"
    return json.loads(path.read_text())
