"""Bounded sliding-window addition-chain search; no human data is read."""
import os
from mathbench.search import search_steps

TARGETS = {
    "T097-C01": 2**192 - 2**64 - 3,
    "T097-C02": 2**221 - 5,
    "T097-C03": 2**521 - 3,
}


def _window_chain(width, target):
    bits = bin(target)[2:]
    if width == 1:
        chain = [1]
        for bit in bits[1:]:
            chain.append(chain[-1] * 2)
            if bit == "1":
                chain.append(chain[-1] + 1)
        return chain
    # The target starts with at least width one-bits. Build all odd window
    # addends, ending at 2**width-1; this also gives the accumulator prefix.
    chain = [1, 2]
    odd = {1: 0}
    chain.append(3)
    odd[3] = 2
    for value in range(5, (1 << width), 2):
        chain.append(chain[odd[value-2]] + 2)
        odd[value] = len(chain)-1
    current = (1 << width) - 1
    i = width
    while i < len(bits):
        if bits[i] == "0":
            current *= 2
            chain.append(current)
            i += 1
            continue
        end = min(i + width, len(bits))
        while bits[end-1] == "0":
            end -= 1
        digit = int(bits[i:end], 2)
        for _ in range(end-i):
            current *= 2
            chain.append(current)
        current += chain[odd[digit]]
        chain.append(current)
        i = end
    return chain


def run_code():
    target = TARGETS.get(os.environ.get("MATHBENCH_CONFIG_ID", "T097-C01"))
    if target is None:
        raise ValueError("unsupported T097 configuration")
    # Fixed work count is reproducible; MATHBENCH_SEARCH_SECONDS can cut it short.
    best = _window_chain(1, target)
    widths = (2, 3, 4, 5, 6)
    for step in search_steps(len(widths)):
        candidate = _window_chain(widths[step], target)
        if len(candidate) < len(best):
            best = candidate
    return {"chain": best}
