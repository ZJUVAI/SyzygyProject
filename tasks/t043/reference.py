"""Fixed replay entry for the verified published human construction."""

import os

from tasks.t043.human import run_code as reconstruct_published_code


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T043-C01") != "T043-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return reconstruct_published_code()


if __name__ == "__main__":
    print(run_code())
