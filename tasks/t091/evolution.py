"""Small seeded population of row-deletion proposals from the simple OA seed."""
import os
from tasks.t091.search_core import search


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T091-C01") != "T091-C01":
        raise ValueError("unsupported configuration")
    return search(16)
