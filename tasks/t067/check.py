"""Exact feasibility checker for binary constant-weight codes."""

from collections.abc import Mapping
import re


CONFIG_ID = "T067-C01"
PARAMETERS = {
    "length": 17,
    "minimum_hamming_distance": 4,
    "constant_weight": 5,
    "objective": "codeword_count",
}
_WORD_RE = re.compile(r"[01]{17}\Z")


def _check_config(config):
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix A(17,4,5)")


def _parse_words(solution):
    raw_words = solution.get("codewords")
    if not isinstance(raw_words, (list, tuple)):
        raise ValueError("codewords must be a list of 17-character binary strings")
    words = []
    for index, value in enumerate(raw_words):
        if not isinstance(value, str) or not _WORD_RE.fullmatch(value):
            raise ValueError(f"codeword {index} must be a 17-character binary string")
        if value.count("1") != 5:
            raise ValueError(f"codeword {index} must have weight 5")
        words.append(int(value, 2))
    if len(set(words)) != len(words):
        raise ValueError("codewords must be distinct")
    return words


def validate(solution, config, strict=False):
    """Recompute size and every pairwise Hamming distance exactly."""
    _check_config(config)
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    words = _parse_words(solution)
    pair_count = 0
    minimum_distance = 17
    for i, word in enumerate(words):
        for other in words[:i]:
            distance = (word ^ other).bit_count()
            if distance < 4:
                raise ValueError("every pair of codewords must have Hamming distance at least 4")
            minimum_distance = min(minimum_distance, distance)
            pair_count += 1
    return {
        "objective": len(words),
        "verification_status": "exact",
        "details": {
            "codeword_count": len(words),
            "unordered_pairs_checked": pair_count,
            "minimum_pairwise_distance": minimum_distance if pair_count else None,
            "word_length": 17,
            "constant_weight": 5,
            "claimed_objective_ignored": True,
            "strict": bool(strict),
        },
    }
