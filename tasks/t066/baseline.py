import os

from tasks.t066.search_core import run_search


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T066-C01") != "T066-C01":
        raise ValueError("unsupported T066 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    return run_search(seed, sweeps=1, samples_per_line=8)
