"""Exact checker for permutation codes with fixed parameters (12, 9)."""

LENGTH = 12
MINIMUM_DISTANCE = 9
PARAMETERS = {
    "length": LENGTH,
    "minimum_hamming_distance": MINIMUM_DISTANCE,
    "alphabet": "{0,...,11}",
    "object": "permutation_code",
}


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("parameters") != PARAMETERS:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict) or "codewords" not in solution:
        raise ValueError("solution must contain codewords")
    codewords = solution["codewords"]
    if not isinstance(codewords, (list, tuple)) or not codewords:
        raise ValueError("codewords must be a nonempty list or tuple")
    normalized = []
    alphabet = set(range(LENGTH))
    for index, word in enumerate(codewords):
        if not isinstance(word, (list, tuple)) or len(word) != LENGTH:
            raise ValueError(f"codeword {index} must contain exactly 12 symbols")
        if any(type(symbol) is not int for symbol in word):
            raise ValueError("symbols must be integers; bool and non-integer values are rejected")
        if set(word) != alphabet:
            raise ValueError(f"codeword {index} is not a permutation of 0 through 11")
        normalized.append(tuple(word))
    if len(set(normalized)) != len(normalized):
        raise ValueError("codewords must be distinct")

    objective = len(normalized)
    checked_pairs = 0
    minimum_distance = LENGTH
    for i, left in enumerate(normalized):
        for j in range(i + 1, objective):
            right = normalized[j]
            distance = sum(a != b for a, b in zip(left, right))
            checked_pairs += 1
            if distance < MINIMUM_DISTANCE:
                raise ValueError(f"codewords {i} and {j} have distance {distance}, below 9")
            minimum_distance = min(minimum_distance, distance)
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "length": LENGTH,
            "minimum_distance_required": MINIMUM_DISTANCE,
            "minimum_distance_observed": minimum_distance if checked_pairs else None,
            "codewords_checked": objective,
            "pairs_checked": checked_pairs,
            "claimed_objective_ignored": True,
        },
    }
