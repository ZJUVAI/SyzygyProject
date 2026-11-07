"""
verify_standalone.py - self-contained verifier for an APPARENT Zarankiewicz floor crossing.

THIS FILE IS NOT A CLAIM. It records an apparent crossing of a padding-honest monotone-floor bar
found by an automated CLASSICAL local search (no LLM). A human must independently confirm the
published bound and the literature frontier before any claim is made anywhere.

Zero engine imports - pure Python stdlib only. Embeds THE MATRIX and brute-forces K_{3,3}-freeness
(a fresh triple-nested check over every 3 rows x 3 columns, independent of how the matrix was
produced). Exit code 0 == the embedded matrix is a valid m-by-n 0/1 matrix, K_{3,3}-free, with the
recorded number of 1s strictly above the recorded bar. Any failure exits non-zero and prints why.

Run:  python verify_standalone.py
"""
from itertools import combinations

M = [[1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0], [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1], [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0], [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0], [0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0], [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0], [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1], [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1]]
M_ROWS = 14
M_COLS = 19
BAR = 124            # honest bar = max(published lb, monotone floor)
CLAIMED_ONES = 126  # number of 1s the automated search found (recount below, do not trust this)
CELL = (14, 19)


def _fail(msg):
    print("FAIL: " + msg)
    raise SystemExit(1)


def main():
    # 1. shape + binary
    if not isinstance(M, list) or len(M) != M_ROWS:
        _fail("matrix is not a list of %d rows" % M_ROWS)
    for i, row in enumerate(M):
        if not isinstance(row, list) or len(row) != M_COLS:
            _fail("row %d is not a list of %d entries" % (i, M_COLS))
        for j, v in enumerate(row):
            if v not in (0, 1):
                _fail("entry (%d,%d)=%r is not 0/1" % (i, j, v))
    # 2. recount ones (never trust the embedded CLAIMED_ONES)
    ones = sum(int(x) for row in M for x in row)
    if ones != CLAIMED_ONES:
        _fail("recount mismatch: embedded says %d ones, actual is %d" % (CLAIMED_ONES, ones))
    # 3. brute-force K_{3,3}-freeness: no 3 rows x 3 columns all-ones (fresh, independent check)
    for rs in combinations(range(M_ROWS), 3):
        for cs in combinations(range(M_COLS), 3):
            if all(M[i][j] == 1 for i in rs for j in cs):
                _fail("K_{3,3} witness at rows %s cols %s (matrix is NOT K_{3,3}-free)" % (rs, cs))
    # 4. the apparent crossing: ones strictly above the honest bar
    if not (ones > BAR):
        _fail("ones=%d does not exceed the honest bar=%d (no apparent crossing)" % (ones, BAR))
    print("OK: Z%s valid K_{3,3}-free matrix, ones=%d > bar=%d (APPARENT crossing; NOT a claim)."
          % (CELL, ones, BAR))
    print("A human must independently confirm the published bound and the literature before any claim.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
