"""Small deterministic seed; the optimizer can mutate it."""
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T057-C01") != "T057-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    values = [0, 2, 3, 4, 7, 11, 12, 14]
    if seed % 2:
        values = [14, 12, 11, 7, 4, 3, 2, 0]
    # EVOLVE-BLOCK-END
    return {"set": values}
