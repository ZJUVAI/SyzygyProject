"""Small deterministic valid seed for the (5,5)-Ramsey graph task."""


def run_code():
    # EVOLVE-BLOCK-START
    n = 5
    adjacency = [[(v - 1) % n, (v + 1) % n] for v in range(n)]
    return {"adjacency": adjacency}
    # EVOLVE-BLOCK-END
