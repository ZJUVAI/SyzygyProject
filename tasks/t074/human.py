"""Rebuild the archived Cantrell n=12 result via the site's decimal coordinates."""

import os

from tasks.t074.construction import reconstruct_rational_points


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T074-C01") != "T074-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    return reconstruct_rational_points()


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
