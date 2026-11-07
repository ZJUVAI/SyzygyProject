# EVOLVE-BLOCK-START
from itertools import combinations


def run_code():
    # Every 20-bit vector with Hamming weight at most four.
    # For any four chosen columns and any pattern, its support gives one row.
    k = 20
    rows = []
    for weight in range(5):
        for support in combinations(range(k), weight):
            ones = set(support)
            rows.append([int(j in ones) for j in range(k)])
    return {"array": rows}
# EVOLVE-BLOCK-END
