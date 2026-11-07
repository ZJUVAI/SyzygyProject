"""Reconstruct the finite m=6,L=5 projection construction from the paper."""

import os

from tasks.t077.construction import projected_simplex


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T077-C01") != "T077-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    values, _weights = projected_simplex(6, 5)
    return {"set": values}


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
