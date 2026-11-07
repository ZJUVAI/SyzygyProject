"""Construct the product of the binary [7,4,3] Hamming code and F_2^3."""

import os


def _hamming7_words():
    # The seven columns of a parity-check matrix are all nonzero 3-bit vectors.
    columns = tuple(range(1, 8))
    words = []
    for word in range(1 << 7):
        syndrome = 0
        for bit, column in enumerate(columns):
            if (word >> bit) & 1:
                syndrome ^= column
        if syndrome == 0:
            words.append(word)
    return words


def build_human_code():
    return {
        "codewords": sorted(
            (word7 << 3) | suffix
            for word7 in _hamming7_words()
            for suffix in range(1 << 3)
        )
    }


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T068-C01")
    if chosen != "T068-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return build_human_code()
