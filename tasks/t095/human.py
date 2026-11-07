"""Reconstructed traditional triangulation plus greedy convex merging."""

import os

from tasks.t095.construction import greedy_merge


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T095-C01") != "T095-C01":
        raise ValueError("unknown T095 configuration")
    return greedy_merge(seed=0, weights=(1.0, 0.0, 0.0), shuffle_ties=False)
