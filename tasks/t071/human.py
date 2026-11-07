"""Reconstruct the classical Varshamov-Tenengolts VT_0(16) code."""

import os

from tasks.t071.check import N


def build_vt0():
    words = []
    for word in range(1 << N):
        checksum = sum((N - bit) * ((word >> bit) & 1) for bit in range(N))
        if checksum % (N + 1) == 0:
            words.append(word)
    return {"codewords": words}


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T071-C01")
    if chosen != "T071-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return build_vt0()
