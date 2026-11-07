"""Fixed seeded coordinate search in a three-axis zonal harmonic basis."""
import os
from tasks.t092.search_core import search


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T092-C01") != "T092-C01":
        raise ValueError("unsupported configuration")
    return search(16)
