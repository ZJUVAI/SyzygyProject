"""Simple valid C4-free seed: a 41-vertex star."""

def run_code():
    # EVOLVE-BLOCK-START
    return {"adjacency": [[*range(1, 41)]] + [[0] for _ in range(40)]}
    # EVOLVE-BLOCK-END
