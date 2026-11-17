"""Self-contained, deliberately simple valid construction."""

from itertools import permutations
import os


# EVOLVE-BLOCK-START
def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T100-C01") != "T100-C01":
        raise ValueError("unsupported configuration id")
    word = "".join("".join(p) for p in permutations("1234567"))
    return {"word": word}
# EVOLVE-BLOCK-END
