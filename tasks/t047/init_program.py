"""Self-contained valid seed for the fixed interval difference-basis task."""

import os


# EVOLVE-BLOCK-START
def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T047-C01") != "T047-C01":
        raise ValueError("unsupported configuration id")
    # Any two integers at distance d represent d. This deliberately simple
    # seed covers the full fixed interval and does not load comparison data.
    return {"basis": list(range(6167)), "claimed_objective": 6167}
# EVOLVE-BLOCK-END
