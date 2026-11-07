"""Seeded iterated 1-flip search for the fixed Gset G70 configuration."""

import os

from tasks.t033._search import repeated_local_search_with_metadata


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T033-C01") != "T033-C01":
        raise ValueError("unknown T033 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    steps = max(1, int(os.environ.get("MATHBENCH_SEARCH_STEPS", "40")))
    labels, _, metadata = repeated_local_search_with_metadata(
        seed, restarts=steps, max_flips=10000)
    return {"labels": labels, "search_metadata": metadata}
