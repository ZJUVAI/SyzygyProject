"""Fixed-iteration generic seeded placement search."""
import os
from tasks.t083.search_core import search


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T083-C01") != "T083-C01":
        raise ValueError("unsupported configuration")
    return search(80)
