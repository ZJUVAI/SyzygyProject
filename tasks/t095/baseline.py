"""Traditional randomized greedy convex-face merging."""

from __future__ import annotations

import os

from tasks.t095.construction import run_greedy_trials


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T095-C01") != "T095-C01":
        raise ValueError("unknown T095 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    return run_greedy_trials(seed=seed, trials=4)
