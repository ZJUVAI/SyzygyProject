"""Evolution-style exact-feasibility mutation search."""
import os
from tasks.t005.search_core import search


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T005-C01") != "T005-C01":
        raise ValueError("unsupported configuration")
    return search(160, evolutionary=True)
