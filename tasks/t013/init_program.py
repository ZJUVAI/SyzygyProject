"""Small, self-contained feasible starting configuration."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T013-C01") != "T013-C01":
        raise ValueError("unknown T013 configuration")
    # EVOLVE-BLOCK-START
    directions = [[1, 0, 0, 0, 0], [-1, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0], [0, -1, 0, 0, 0],
                  [0, 0, 1, 0, 0], [0, 0, -1, 0, 0],
                  [0, 0, 0, 1, 0], [0, 0, 0, -1, 0],
                  [0, 0, 0, 0, 1], [0, 0, 0, 0, -1]]
    # EVOLVE-BLOCK-END
    return {"directions": directions}
