"""Rebuild the seven-round resolvable transversal design RTD(5, 7)."""

import os


def build_schedule():
    # Player (a,b) is encoded as 7*a+b, with a in F_7 and b in F_7.
    rounds = []
    for t in range(7):
        groups = []
        for c in range(7):
            groups.append([7 * a + ((t * a + c) % 7) for a in range(5)])
        rounds.append(groups)
    return rounds


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T058-C01")
    if chosen != "T058-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return {"rounds": build_schedule(), "construction": {"method": "RTD(5,7) over F_7"}}
