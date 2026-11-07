"""Simple valid fan triangulation of the fixed regular 120-gon."""

# EVOLVE-BLOCK-START
def run_code():
    n = 120
    edges = [[i, i + 1] for i in range(n - 1)] + [[0, n - 1]]
    edges.extend([[0, i] for i in range(2, n - 1)])
    return {"edges": edges}
# EVOLVE-BLOCK-END
