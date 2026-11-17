"""Reconstructed traditional triangulation plus greedy convex merging."""

import os

from tasks.t028.construction import greedy_merge


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T028-C01") != "T028-C01":
        raise ValueError("unknown T028 configuration")
    return greedy_merge(seed=0, weights=(1.0, 0.0, 0.0), shuffle_ties=False)
