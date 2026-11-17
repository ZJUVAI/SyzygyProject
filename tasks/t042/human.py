"""Reproduce a seeded traditional 1-flip local-search baseline on G70."""

import os

from tasks.t042._search import repeated_local_search_with_metadata


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T042-C01") != "T042-C01":
        raise ValueError("unknown T042 configuration")
    # This external baseline is frozen at seed 0, independent of candidate seeds.
    labels, _, metadata = repeated_local_search_with_metadata(
        seed=0, restarts=4, max_flips=10000)
    return {"labels": labels, "search_metadata": metadata}
