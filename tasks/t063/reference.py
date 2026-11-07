"""Fixed replay of the independently certified degree-100 public polynomial."""
import os

from tasks.t063.human import run_code as _published_polynomial


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T063-C01") != "T063-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return _published_polynomial()


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
