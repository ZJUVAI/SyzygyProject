"""Rebuild the classic Ashlock–Tillotson recursive construction."""

from math import factorial


def _append_with_maximum_overlap(word, permutation):
    overlap = min(len(word), len(permutation))
    while overlap and word[-overlap:] != permutation[:overlap]:
        overlap -= 1
    return word + permutation[overlap:]


def _recursive_word(n):
    if n == 1:
        return "1"
    previous = _recursive_word(n - 1)
    order = []
    seen = set()
    width = n - 1
    for start in range(len(previous) - width + 1):
        permutation = previous[start : start + width]
        if len(set(permutation)) == width and permutation not in seen:
            seen.add(permutation)
            order.append(permutation)
    if len(order) != factorial(width):
        raise RuntimeError("recursive source word did not expose every smaller permutation")
    word = ""
    for smaller in order:
        current = smaller + str(n)
        for _ in range(n):
            word = _append_with_maximum_overlap(word, current)
            current = current[1:] + current[0]
    return word


def run_code():
    return {"word": _recursive_word(7)}
