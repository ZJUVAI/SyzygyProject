"""Self-contained identity ordering for gd96a."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T045-C01") != "T045-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    ordering = list(range(1, 1097))
    # EVOLVE-BLOCK-END
    return {"ordering": ordering}


if __name__ == "__main__":
    print(run_code())
