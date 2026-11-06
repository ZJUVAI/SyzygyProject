"""Exact checker for independent words in C7's fifth strong power."""


def validate(solution, config, strict=False):
    expected = {"id": "N001-C01", "parameters": {"q": 7, "power": 5}}
    if not isinstance(config, dict) or config.get("id") != expected["id"] or config.get("parameters") != expected["parameters"]:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    words = solution.get("words")
    if not isinstance(words, (list, tuple)):
        raise ValueError("words must be a list")
    seen = set()
    for i, word in enumerate(words):
        if not isinstance(word, (list, tuple)) or len(word) != 5:
            raise ValueError(f"word {i} must contain exactly five symbols")
        if any(isinstance(x, bool) or not isinstance(x, int) or not 0 <= x < 7 for x in word):
            raise ValueError(f"word {i} symbols must be integers from 0 through 6")
        item = tuple(word)
        if item in seen:
            raise ValueError(f"duplicate word at index {i}")
        seen.add(item)
    for i, word in enumerate(words):
        for j in range(i):
            other = words[j]
            if all(min((a-b) % 7, (b-a) % 7) <= 1 for a, b in zip(word, other)):
                raise ValueError(f"words {j} and {i} are adjacent in the strong power")
    claimed = solution.get("objective")
    mismatch = claimed is not None and (isinstance(claimed, bool) or claimed != len(words))
    return {"objective": len(words), "verification_status": "exact", "details": {
        "word_count": len(words), "all_pairs_checked": True,
        "claimed_objective_mismatch": mismatch, "optimality_proved": False}}
