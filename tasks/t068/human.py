"""Rebuild the 3,703-term Rabung power-residue coloring reported in 2007."""


def run_code():
    prime = 617
    n = 6 * prime + 1
    quadratic_residues = {value * value % prime for value in range(1, prime)}
    colors = []
    for position in range(n):
        residue = position % prime
        if residue == 0:
            color = 0
        else:
            color = 0 if residue in quadratic_residues else 1
        colors.append(color)
    # The endpoint is 6p. It must differ from position 0 or step p gives a 7-AP.
    colors[-1] = 1
    return {"n": n, "colors": colors}
