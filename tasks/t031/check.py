"""Exact checker for seven-symbol superpermutations."""

from itertools import permutations


CONFIG_ID = "T031-C01"
ALPHABET = frozenset("1234567")
REQUIRED = {"".join(p) for p in permutations("1234567")}


def validate(solution, config, strict=False):
    """Check every length-seven window and report its exact string length."""
    if config.get("id") != CONFIG_ID:
        raise ValueError("unsupported configuration id")
    if config.get("parameters") != {
        "symbols": ["1", "2", "3", "4", "5", "6", "7"],
        "permutations_required": 5040,
        "containment": "contiguous_substring",
    }:
        raise ValueError("unsupported configuration parameters")
    if not isinstance(solution, dict) or "word" not in solution:
        raise ValueError("solution must contain a word string")
    word = solution["word"]
    if not isinstance(word, str):
        raise ValueError("word must be a string")
    if any(symbol not in ALPHABET for symbol in word):
        raise ValueError("word contains a symbol outside 1 through 7")
    found = set()
    for start in range(max(0, len(word) - 6)):
        window = word[start : start + 7]
        if len(set(window)) == 7:
            found.add(window)
    missing = REQUIRED - found
    if missing:
        raise ValueError(f"word is missing {len(missing)} required contiguous permutations")
    return {
        "objective": len(word),
        "verification_status": "exact",
        "details": {
            "symbols": 7,
            "required_permutations": 5040,
            "distinct_permutations_found": len(found),
            "windows_checked": max(0, len(word) - 6),
            "claimed_score_ignored": True,
            "containment": "contiguous_substring",
        },
    }
