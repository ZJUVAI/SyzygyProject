import os

from tasks.t079.search_core import run_search


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T079-C01") != "T079-C01":
        raise ValueError("unsupported T079 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    return run_search(seed, sweeps=8, samples_per_line=16)
