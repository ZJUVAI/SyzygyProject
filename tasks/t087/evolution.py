"""Extend the independent local-search baseline with a fixed mutation budget."""

import os

from tasks.t087.baseline import run_search


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T087-C01")
    if config_id != "T087-C01":
        raise ValueError(f"unknown T087 configuration: {config_id}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    heights, info = run_search(seed, steps=1400)
    return {"heights": heights,
            "search_method": "seeded block mutation with exact final checking",
            "random_seed": seed, **info}
