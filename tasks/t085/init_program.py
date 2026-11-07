"""Self-contained, deliberately simple seed: 21 coincident unit circles."""
import os


# EVOLVE-BLOCK-START
def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T085-C01")
    if config_id != "T085-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    return {"radius": "1", "centers": [["0", "0"] for _ in range(21)]}
# EVOLVE-BLOCK-END
