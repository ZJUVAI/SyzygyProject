"""Self-contained low-score seed; it does not read comparison files."""
import json
import os
import random


# EVOLVE-BLOCK-START
def run_code():
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T041-C01")
    if config != "T041-C01":
        raise ValueError("unsupported T041 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    # 17 equal squares form one horizontal row; this gives a simple score 1.
    squares = [{"x": f"{2*col+1}/34", "y": "1/34", "side": "1/17",
                "cos": "1", "sin": "0"} for col in range(17)]
    rng.random()  # Seed is part of the stable program interface.
    return {"squares": squares}
# EVOLVE-BLOCK-END


if __name__ == "__main__":
    print(json.dumps(run_code()))
