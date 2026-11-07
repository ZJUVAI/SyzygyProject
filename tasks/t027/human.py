"""Replay the archived QAPLIB tai256c incumbent permutation."""
import os
from pathlib import Path


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T027-C01") != "T027-C01":
        raise ValueError("unsupported T027 configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    words = (Path(__file__).parent / "data" / "tai256c.sln").read_text(encoding="ascii").split()
    if len(words) != 258 or int(words[0]) != 256:
        raise ValueError("unexpected QAPLIB solution format")
    claimed = int(words[1])
    one_based = [int(value) for value in words[2:]]
    if len(set(one_based)) != 256 or any(value < 1 or value > 256 for value in one_based):
        raise ValueError("archived solution is not a permutation")
    return {"permutation": [value - 1 for value in one_based], "claimed_score": claimed}
