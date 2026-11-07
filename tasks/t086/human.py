"""Traditional identity-matrix construction giving ratio exactly one."""

import os

from tasks.t086.init_program import _identity


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T086-C01") != "T086-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return {"matrices": [_identity(), _identity(), _identity(), _identity()]}


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
