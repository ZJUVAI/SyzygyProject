"""Self-contained one-vertex seed for the C2000.9 maximum clique task."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T039-C01") != "T039-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    vertices = [0]
    # EVOLVE-BLOCK-END
    return {"vertices": vertices, "seed": seed}


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
