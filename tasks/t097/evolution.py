"""Bounded deterministic search for ordinary addition chains.

The search uses several binary window schedules, then removes unused
precomputation entries. It reads only the selected public target.
"""
import os
import time

TARGETS = {
    "T097-C01": 2**192 - 2**64 - 3,
    "T097-C02": 2**221 - 5,
    "T097-C03": 2**521 - 3,
}


def _chain_for_widths(target, widths):
    bits = bin(target)[2:]
    # Start with the leading run of one-bits. This permits a monotone odd
    # precomputation table whose final entry is also the accumulator prefix.
    prefix_len = 1
    while prefix_len < min(max(widths), len(bits)) and bits[prefix_len] == "1":
        prefix_len += 1
    prefix = (1 << prefix_len) - 1
    chain = [1]
    odd = {1: 0}
    if prefix_len > 1:
        chain.append(2)
        for value in range(3, prefix + 1, 2):
            chain.append(chain[odd[value - 2]] + 2)
            odd[value] = len(chain) - 1
    current = prefix
    i = prefix_len
    segment = 0
    while i < len(bits):
        w = widths[segment % len(widths)]
        segment += 1
        if bits[i] == "0":
            current *= 2
            chain.append(current)
            i += 1
            continue
        end = min(i + w, len(bits))
        while bits[end - 1] == "0":
            end -= 1
        digit = int(bits[i:end], 2)
        for _ in range(end - i):
            current *= 2
            chain.append(current)
        current += chain[odd[digit]]
        chain.append(current)
        i = end
    return chain


def _prune(chain):
    """Keep a valid dependency closure for the endpoint, dropping dead nodes."""
    needed = {len(chain) - 1}
    index = {value: i for i, value in enumerate(chain)}
    for i in range(len(chain) - 1, 0, -1):
        if i not in needed:
            continue
        value = chain[i]
        # Prefer a balanced witness; each operand is strictly earlier.
        witness = None
        for j in range(i - 1, -1, -1):
            k = index.get(value - chain[j])
            if k is not None and k <= j:
                witness = (j, k)
                break
        if witness is None:
            return chain
        needed.update(witness)
    return [v for i, v in enumerate(chain) if i in needed]


def _mersenne_chain(exponent):
    """Build 2**exponent-1 from the binary addition chain of exponent."""
    chain = [1]
    current_exponent = 1
    for bit in bin(exponent)[3:]:
        base = chain[-1]
        value = base
        for _ in range(current_exponent):
            value *= 2
            chain.append(value)
        value += base
        chain.append(value)
        current_exponent *= 2
        if bit == "1":
            value *= 2
            chain.append(value)
            value += 1
            chain.append(value)
            current_exponent += 1
    return chain


def _structured_candidate(cid):
    """Use 2**(a+b)-1 = 2**b*(2**a-1) + (2**b-1)."""
    if cid == "T097-C03":
        chain = _mersenne_chain(519)
        for _ in range(2):
            chain.append(chain[-1] * 2)
        chain.append(chain[-1] + 1)
        return chain
    if cid == "T097-C02":
        chain = _mersenne_chain(218)
        for _ in range(3):
            chain.append(chain[-1] * 2)
        chain.append(chain[-1] + 3)
        return chain
    # 2**192-2**64-3 = 2**65*(2**127-1) + (2**64-3),
    # and 2**64-3 = 8*(2**61-1)+5. Merge the two independently
    # constructed chains in increasing order; their addition witnesses remain.
    m61 = _mersenne_chain(61)
    m61_value = m61[-1]
    # Build the smaller addend and M127 from the same M61 prefix. These
    # independent monotone paths can be merged by value while retaining every
    # addition witness.
    small_part = [m61_value * 2, m61_value * 4, m61_value * 8,
                  m61_value * 8 + 5]
    m63_path = [m61_value * 2, m61_value * 4]
    m63_path.append(m63_path[-1] + 3)
    m126_path = []
    value = m63_path[-1]
    for _ in range(63):
        value *= 2
        m126_path.append(value)
    value += m63_path[-1]
    m126_path.append(value)
    m127_path = [value * 2, value * 2 + 1]
    value = m127_path[-1]
    merged = sorted(set(m61) | {1, 2, 3, 5} | set(small_part) |
                    set(m63_path) | set(m126_path) | set(m127_path))
    base = value
    # The final scale terms are larger than every merged entry.
    for _ in range(65):
        base *= 2
        merged.append(base)
    merged.append(base + small_part[-1])
    return merged


def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T097-C01")
    target = TARGETS.get(cid)
    if target is None:
        raise ValueError("unsupported T097 configuration")
    try:
        budget = max(0.01, min(45.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45"))))
    except ValueError:
        budget = 45.0
    deadline = time.monotonic() + budget
    best = _prune(_chain_for_widths(target, (1,)))
    candidates_considered = 1
    structured = _prune(_structured_candidate(cid))
    candidates_considered += 1
    if structured[-1] == target and len(structured) < len(best):
        best = structured
    # Constant-width schedules cover the usual sliding-window tradeoff.
    schedules = [(w,) for w in range(2, 10)]
    # Mixed schedules reduce precomputation cost while retaining wide windows
    # in alternating regions. Order is fixed, so the same budget is reproducible.
    schedules += [(a, b) for a in range(2, 8) for b in range(2, 8) if a != b]
    for schedule in schedules:
        if time.monotonic() >= deadline:
            break
        candidate = _prune(_chain_for_widths(target, schedule))
        candidates_considered += 1
        if len(candidate) < len(best):
            best = candidate
    return {"chain": best, "search_metadata": {
        "candidates_considered": candidates_considered,
        "addition_count": len(best) - 1,
        "chain_entries": len(best),
    }}
