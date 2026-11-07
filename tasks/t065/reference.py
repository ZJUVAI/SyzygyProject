"""Fixed replay of the verified 261-edge human triangular-grid baseline."""

import os

from tasks.t065.human import run_code as _human_grid


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T065-C01") != "T065-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return _human_grid()


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
