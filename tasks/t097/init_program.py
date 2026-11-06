"""Deterministic binary-method seed; no reference witness is read."""
import os

TARGETS = {
    "T097-C01": 2**192 - 2**64 - 3,
    "T097-C02": 2**221 - 5,
    "T097-C03": 2**521 - 3,
}


def run_code():
    target = TARGETS.get(os.environ.get("MATHBENCH_CONFIG_ID", "T097-C01"))
    if target is None:
        raise ValueError("unsupported T097 configuration")
    # EVOLVE-BLOCK-START
    bits = bin(target)[2:]
    chain = [1]
    for bit in bits[1:]:
        chain.append(2 * chain[-1])
        if bit == "1":
            chain.append(chain[-1] + 1)
    # EVOLVE-BLOCK-END
    return {"chain": chain}
