"""Exact verifier for a (24,14,4) covering design."""
from itertools import combinations

V, K, T = 24, 14, 4
CONFIG = {"v": V, "k": K, "t": T}


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("parameters") != CONFIG:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    blocks = solution.get("blocks")
    if not isinstance(blocks, (list, tuple)):
        raise ValueError("blocks must be a list")
    normalized, seen = [], set()
    for i, block in enumerate(blocks):
        if not isinstance(block, (list, tuple)) or len(block) != K:
            raise ValueError(f"block {i} must contain exactly 14 points")
        if any(type(x) is not int for x in block):
            raise ValueError("points must be integers; bool is rejected")
        b = tuple(block)
        if len(set(b)) != K:
            raise ValueError(f"block {i} contains repeated points")
        if any(x < 0 or x >= V for x in b):
            raise ValueError("points must be in 0..23")
        b = tuple(sorted(b))
        if b in seen:
            raise ValueError("duplicate blocks are not allowed")
        seen.add(b)
        normalized.append(b)
    covered = set()
    for b in normalized:
        covered.update(combinations(b, T))
    total = 10626
    if len(covered) != total:
        raise ValueError(f"covering misses {total-len(covered)} of {total} four-subsets")
    claimed = solution.get("objective")
    mismatch = claimed is not None and (type(claimed) is not int or claimed != len(normalized))
    return {"objective": len(normalized), "verification_status": "exact", "details": {
        "parameters": CONFIG, "blocks": len(normalized), "covered_four_subsets": total,
        "total_four_subsets": total, "claimed_objective_mismatch": mismatch,
        "optimality_proved": False}}
