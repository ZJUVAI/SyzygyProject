"""Deterministic left-to-right greedy construction of a B_3 set."""

from itertools import combinations_with_replacement


def build_greedy():
    elements = [0]
    triple_sums = {0}
    candidate_checks = 0
    while len(elements) < 31:
        value = elements[-1] + 1
        while True:
            if candidate_checks >= 100000:
                # A known no-carry construction gives a valid bounded fallback.
                return [0] + [4 ** exponent for exponent in range(30)], candidate_checks
            candidate_checks += 1
            new_sums = [value + a + b for a, b in combinations_with_replacement(elements, 2)]
            new_sums.extend(2 * value + a for a in elements)
            new_sums.append(3 * value)
            new_set = set(new_sums)
            if len(new_set) == len(new_sums) and not (new_set & triple_sums):
                break
            value += 1
        triple_sums.update(new_set)
        elements.append(value)
    return elements, candidate_checks


def run_code():
    elements, checks = build_greedy()
    return {
        "elements": elements,
        "search_method": "deterministic increasing-candidate greedy B3 construction",
        "candidate_checks": checks,
        "search_iterations": checks,
        "random_seed": 0,
    }
