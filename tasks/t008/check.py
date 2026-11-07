"""Exact verifier for configured covering designs."""
from itertools import combinations
from math import comb


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or not isinstance(config.get("parameters"), dict):
        raise ValueError("unsupported configuration")
    params = config["parameters"]
    v, k, t = (params.get(key) for key in ("v", "k", "t"))
    if any(type(x) is not int for x in (v, k, t)) or not (0 < t <= k <= v):
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    blocks = solution.get("blocks")
    if not isinstance(blocks, (list, tuple)):
        raise ValueError("blocks must be a list")
    normalized, seen = [], set()
    for i, block in enumerate(blocks):
        if not isinstance(block, (list, tuple)) or len(block) != k:
            raise ValueError(f"block {i} must contain exactly {k} points")
        if any(type(x) is not int for x in block):
            raise ValueError("points must be integers; bool is rejected")
        b = tuple(sorted(block))
        if len(set(b)) != k or any(x < 0 or x >= v for x in b):
            raise ValueError(f"block {i} has repeated or out-of-range points")
        if b in seen:
            raise ValueError("duplicate blocks are not allowed")
        seen.add(b)
        normalized.append(b)
    covered = set()
    for b in normalized:
        covered.update(combinations(b, t))
    total = comb(v, t)
    if len(covered) != total:
        raise ValueError(f"covering misses {total-len(covered)} of {total} {t}-subsets")
    details = {
        "parameters": {"v": v, "k": k, "t": t}, "blocks": len(normalized),
        "covered_t_subsets": total, "total_t_subsets": total,
        "claimed_objective_ignored": True, "optimality_proved": False}
    if t == 4:
        details["covered_four_subsets"] = total
    return {"objective": len(normalized), "verification_status": "exact", "details": details}
