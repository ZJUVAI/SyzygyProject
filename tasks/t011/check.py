"""Exact checker for independent words in strong powers of C7."""

CONFIG_POWER = {"T011-C01": 5, "T011-C02": 4, "T011-C03": 6}


def validate(solution, config, strict=False):
    del strict
    if not isinstance(config, dict) or config.get("id") not in CONFIG_POWER:
        raise ValueError("unsupported configuration")
    power = CONFIG_POWER[config["id"]]
    if config.get("parameters") != {"q": 7, "power": power}:
        raise ValueError("configuration parameters do not match the registered T011 configuration")
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    words = solution.get("words")
    if not isinstance(words, (list, tuple)):
        raise ValueError("words must be a list")
    seen = set()
    for i, word in enumerate(words):
        if not isinstance(word, (list, tuple)) or len(word) != power:
            raise ValueError(f"word {i} must contain exactly {power} symbols")
        if any(type(x) is not int or not 0 <= x < 7 for x in word):
            raise ValueError(f"word {i} symbols must be integers from 0 through 6")
        item = tuple(word)
        if item in seen:
            raise ValueError(f"duplicate word at index {i}")
        seen.add(item)
    for i, word in enumerate(words):
        for j in range(i):
            if all(min((a-b) % 7, (b-a) % 7) <= 1 for a, b in zip(word, words[j])):
                raise ValueError(f"words {j} and {i} are adjacent in the strong power")
    return {"objective": len(words), "verification_status": "exact", "details": {
        "word_count": len(words), "power": power, "all_pairs_checked": True,
        "claimed_objective_ignored": True, "optimality_proved": False}}
