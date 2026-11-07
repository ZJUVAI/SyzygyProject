"""Exact checker for binary length-16 single-deletion-correcting codes."""

N = 16
ALPHABET_SIZE = 1 << N
CONFIG_ID = "T071-C01"
PARAMETERS = {
    "length": N,
    "alphabet": "{0,1}",
    "correctable_errors": "one deletion",
    "decoding_condition": "distinct codewords have disjoint sets of length-15 deletion outputs",
    "objective": "number of codewords",
}


def deletion_outputs(word):
    """Return distinct length-(N-1) strings after one bit is deleted."""
    return {
        (word & ((1 << bit) - 1)) | ((word >> (bit + 1)) << bit)
        for bit in range(N)
    }


def _check_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    if config.get("id") not in (None, CONFIG_ID):
        raise ValueError(f"unsupported configuration: expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix binary length 16 and one deletion")


def validate(solution, config, strict=False):
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    codewords = solution.get("codewords")
    if not isinstance(codewords, list):
        raise ValueError("codewords must be a list of 16-bit integers")
    seen_words = set()
    used_outputs = set()
    for index, word in enumerate(codewords):
        if type(word) is not int:
            raise ValueError(f"codeword {index} must be an integer (booleans are not accepted)")
        if not 0 <= word < ALPHABET_SIZE:
            raise ValueError(f"codeword {word} is outside 0..{ALPHABET_SIZE - 1}")
        if word in seen_words:
            raise ValueError(f"duplicate codeword {word}")
        seen_words.add(word)
        outputs = deletion_outputs(word)
        if outputs & used_outputs:
            raise ValueError(f"codeword {word} shares a deletion output with an earlier codeword")
        used_outputs.update(outputs)
    return {
        "objective": len(seen_words),
        "verification_status": "exact",
        "details": {
            "length": N,
            "alphabet_size": ALPHABET_SIZE,
            "codeword_count": len(seen_words),
            "distinct_deletion_outputs": len(used_outputs),
            "possible_deletion_outputs": 1 << (N - 1),
            "pairwise_disjoint_deletion_outputs": True,
            "claimed_objective_ignored": True,
        },
    }
