"""Exact checker for binary length-10 radius-one covering codes."""

CONFIG_ID = "T068-C01"
LENGTH = 10
UNIVERSE_SIZE = 1 << LENGTH
UNIVERSE_MASK = (1 << UNIVERSE_SIZE) - 1
PARAMETERS = {
    "length": LENGTH,
    "alphabet": "{0,1}",
    "covering_radius": 1,
    "universe": "all 1024 binary words of length 10",
    "objective": "number of codewords",
}


def _check_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    if config.get("id") not in (None, CONFIG_ID):
        raise ValueError(f"unsupported configuration: expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix binary length 10 and covering radius 1")


def _ball_mask(center):
    mask = 1 << center
    for bit in range(LENGTH):
        mask |= 1 << (center ^ (1 << bit))
    return mask


def validate(solution, config, strict=False):
    """Verify complete coverage of the 10-cube using exact bitset arithmetic."""
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    codewords = solution.get("codewords")
    if not isinstance(codewords, list):
        raise ValueError("codewords must be a list of integers")
    seen = set()
    for index, word in enumerate(codewords):
        if type(word) is not int:
            raise ValueError(f"codeword {index} must be an integer (booleans are not accepted)")
        if not 0 <= word < UNIVERSE_SIZE:
            raise ValueError(f"codeword {word} is outside 0..1023")
        if word in seen:
            raise ValueError(f"duplicate codeword {word}")
        seen.add(word)

    covered = 0
    for word in seen:
        covered |= _ball_mask(word)
    if covered != UNIVERSE_MASK:
        missing_mask = UNIVERSE_MASK ^ covered
        first_missing = (missing_mask & -missing_mask).bit_length() - 1
        missing_count = missing_mask.bit_count()
        raise ValueError(
            f"code is not a radius-one cover: {missing_count} words uncovered; first is {first_missing:010b}"
        )

    return {
        "objective": len(seen),
        "verification_status": "exact",
        "details": {
            "length": LENGTH,
            "universe_size": UNIVERSE_SIZE,
            "codeword_count": len(seen),
            "covered_word_count": covered.bit_count(),
            "radius": 1,
            "claimed_objective_ignored": True,
        },
    }
