"""A small valid code consisting of the 12 cyclic shifts of the identity."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T052-C01") != "T052-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    codewords = [[(symbol + shift) % 12 for symbol in range(12)] for shift in range(12)]
    # EVOLVE-BLOCK-END
    return {"codewords": codewords}


if __name__ == "__main__":
    print(run_code())
