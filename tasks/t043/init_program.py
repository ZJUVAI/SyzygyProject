"""Self-contained simple seed: the coordinate 3-space in F_2^7."""
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T043-C01") != "T043-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))  # Read the fixed runner seed; this seed is deterministic.
    # EVOLVE-BLOCK-START
    codewords = [[1, 2, 4]]
    # EVOLVE-BLOCK-END
    return {"codewords": codewords, "objective": 1}


if __name__ == "__main__":
    print(run_code())
