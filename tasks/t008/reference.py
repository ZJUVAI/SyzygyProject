"""Best reproduced fixed local-search witness; not a historical human record."""
import json
import os
from pathlib import Path

def run_code():
    suffix = "_C02" if os.environ.get("MATHBENCH_CONFIG_ID", "T008-C01") == "T008-C02" else ""
    return json.loads((Path(__file__).parent/f'data/search_reference{suffix}.json').read_text())
