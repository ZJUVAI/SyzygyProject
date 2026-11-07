"""Fixed-iteration seeded steepest 1-flip local search."""

import os

from tasks.t033._search import repeated_local_search_with_metadata
from tasks.t033.init_program import run_code as initial


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T033-C01") != "T033-C01":
        raise ValueError("unknown T033 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    steps = max(1, int(os.environ.get("MATHBENCH_SEARCH_STEPS", "8")))
    labels, _, metadata = repeated_local_search_with_metadata(
        seed, restarts=steps, max_flips=10000, start=initial()["labels"])
    return {"labels": labels, "search_metadata": metadata}
