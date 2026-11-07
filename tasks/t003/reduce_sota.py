"""Find minimal common radius shrink on a 1e-18 grid for Packomania witnesses."""
from fractions import Fraction
from pathlib import Path
import json

ROOT = Path(__file__).parent
STEP = Fraction(1, 10**18)


def load_public(n):
    """Read the archived Packomania centered-coordinate source snapshot."""
    path = ROOT / "data" / f"packomania{n}_source.txt"
    rows = []
    for line in path.read_text().splitlines():
        fields = line.split()
        if len(fields) == 4 and fields[0].isdigit():
            _, x, y, radius = fields
            rows.append((Fraction(x) + Fraction(1, 2),
                         Fraction(y) + Fraction(1, 2), Fraction(radius)))
    if len(rows) != n:
        raise ValueError(f"expected {n} circles in {path}, found {len(rows)}")
    return rows


def feasible(rows, shrink):
    circles = [(x, y, r - shrink) for x, y, r in rows]
    if any(r <= 0 or x-r < 0 or x+r > 1 or y-r < 0 or y+r > 1
           for x, y, r in circles):
        return False
    for i, (x1, y1, r1) in enumerate(circles):
        for x2, y2, r2 in circles[:i]:
            if (x1-x2)**2 + (y1-y2)**2 < (r1+r2)**2:
                return False
    return True


def find_minimum(rows):
    """Binary search integer grid units; feasible set is monotone in shrink."""
    lo, hi = 0, 10**9  # [0, 1e-9], known to contain a feasible endpoint
    assert feasible(rows, Fraction(hi) * STEP)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(rows, Fraction(mid) * STEP):
            hi = mid
        else:
            lo = mid
    shrink = Fraction(hi) * STEP
    assert feasible(rows, shrink)
    assert not feasible(rows, Fraction(lo) * STEP)
    return shrink


def main():
    for n in (26, 32):
        rows = load_public(n)
        shrink = find_minimum(rows)
        circles = [{"x": str(x), "y": str(y), "r": str(r-shrink)}
                   for x, y, r in rows]
        out = ROOT / "data" / f"sota{n}.json"
        out.write_text(json.dumps({"circles": circles}, indent=2) + "\n")
        score = sum((r-shrink for _, _, r in rows), Fraction())
        print(f"n={n} shrink={shrink} score={score} decimal={float(score):.15f}")


if __name__ == "__main__":
    main()
