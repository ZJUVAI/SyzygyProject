"""Self-contained, deliberately simple 2-by-2 unit-triangle packing."""
import os


# EVOLVE-BLOCK-START
def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T083-C01")
    if config_id != "T083-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    return {
        "side": ["2", "0"],
        "triangles": [
            {"anchor": [[str(x), "0"], [str(y), "0"]], "direction": ["1", "0"]}
            for x, y in ((0, 0), (1, 0), (0, 1), (1, 1))
        ],
    }
# EVOLVE-BLOCK-END
