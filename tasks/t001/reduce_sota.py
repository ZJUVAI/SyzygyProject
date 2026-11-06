"""Create maximally large exactly feasible T001 radii on a 1e-18 grid."""
from fractions import Fraction
from pathlib import Path
import json

ROOT = Path(__file__).parent
STEP = Fraction(1, 10**18)
COUNTS = (26, 32, 50)


def load_public(n):
    """Read archived Packomania coordinates in its centered-square convention."""
    path = ROOT / "data" / f"packomania_n{n}_source.txt"
    rows = []
    for line in path.read_text().splitlines():
        fields = line.split()
        if len(fields) == 4 and fields[0].isdigit():
            _, x, y, radius = fields
            rows.append((Fraction(x) + Fraction(1, 2),
                         Fraction(y) + Fraction(1, 2), Fraction(radius)))
    if len(rows) != n:
        raise ValueError(f"expected {n} circles in {path}, found {len(rows)}")
    if len({r for _, _, r in rows}) != 1:
        raise ValueError("public coordinates do not have one common radius")
    return rows


def feasible(rows, radius):
    if radius <= 0:
        return False
    if any(x-radius < 0 or x+radius > 1 or y-radius < 0 or y+radius > 1
           for x, y, _ in rows):
        return False
    required = (2 * radius) ** 2
    for i, (x1, y1, _) in enumerate(rows):
        for x2, y2, _ in rows[:i]:
            if (x1-x2)**2 + (y1-y2)**2 < required:
                return False
    return True


def find_minimum_shrink(rows):
    """Find minimum public-radius decrement that passes exact constraints."""
    public_radius = rows[0][2]
    lo, hi = 0, 10**9  # [0, 1e-9], observed to contain a feasible endpoint
    assert not feasible(rows, public_radius - Fraction(lo) * STEP)
    assert feasible(rows, public_radius - Fraction(hi) * STEP)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(rows, public_radius - Fraction(mid) * STEP):
            hi = mid
        else:
            lo = mid
    shrink = Fraction(hi) * STEP
    assert feasible(rows, public_radius - shrink)
    assert not feasible(rows, public_radius - Fraction(lo) * STEP)
    return shrink


def main():
    for n in COUNTS:
        rows = load_public(n)
        public_radius = rows[0][2]
        shrink = find_minimum_shrink(rows)
        radius = public_radius - shrink
        witness = {
            "radius": str(radius),
            "centers": [[str(x), str(y)] for x, y, _ in rows],
        }
        out = ROOT / "data" / f"sota_n{n}.json"
        out.write_text(json.dumps(witness, indent=2) + "\n")
        print(f"n={n} public={public_radius} shrink={shrink} "
              f"reproduced={radius} feasible={feasible(rows, radius)} "
              f"previous_grid_feasible={feasible(rows, radius + STEP)}")


if __name__ == "__main__":
    main()
