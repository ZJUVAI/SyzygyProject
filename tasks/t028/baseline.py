"""Traditional randomized greedy convex-face merging."""

from __future__ import annotations

import os

from tasks.t028.construction import run_greedy_trials


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T028-C01") != "T028-C01":
        raise ValueError("unknown T028 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    return run_greedy_trials(seed=seed, trials=4)
