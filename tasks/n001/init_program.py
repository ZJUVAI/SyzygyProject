"""Deterministic product construction for C7^5."""


def run_code():
    # EVOLVE-BLOCK-START
    words = [[a, b, c, d, e] for a in (0, 2, 4) for b in (0, 2, 4)
             for c in (0, 2, 4) for d in (0, 2, 4) for e in (0, 2, 4)]
    # EVOLVE-BLOCK-END
    return {"words": words}
