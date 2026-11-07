"""Traditional bounded search over the self-generated seed tiling."""

from __future__ import annotations

import os

from tasks.t099.construction import run_search
from tasks.t099.init_program import run_code as initial_solution


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T099-C01") != "T099-C01":
        raise ValueError("unknown T099 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    return run_search(initial_solution(), seed=seed, trials=4)
