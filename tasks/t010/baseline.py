"""Traditional bounded search over the self-generated seed tiling."""

from __future__ import annotations

import os

from tasks.t010.construction import run_search
from tasks.t010.init_program import run_code as initial_solution


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T010-C01") != "T010-C01":
        raise ValueError("unknown T010 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    return run_search(initial_solution(), seed=seed, trials=4)
