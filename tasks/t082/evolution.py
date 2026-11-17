"""Fixed seeded harmonic-basis population search."""
import os
from tasks.t082.search_core import search


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T082-C01") != "T082-C01":
        raise ValueError("unsupported configuration")
    return search(24, evolutionary=True)
