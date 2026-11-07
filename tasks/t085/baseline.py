"""Fixed-iteration seeded center mutation baseline."""
import os
from tasks.t085.search_core import search


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T085-C01") != "T085-C01":
        raise ValueError("unsupported configuration")
    return search(12)
