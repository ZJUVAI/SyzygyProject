"""Self-contained binary Horner seed; no task or reference imports."""
import os

TARGET = 2**61 - 1


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T060-C01") != "T060-C01":
        raise ValueError("unsupported T060 configuration")
    # EVOLVE-BLOCK-START
    bits = bin(TARGET)[2:]
    expression = "1"
    for bit in bits[1:]:
        expression = f"({expression}*(1+1))"
        if bit == "1":
            expression = f"({expression}+1)"
    # EVOLVE-BLOCK-END
    return {"expression": expression}
