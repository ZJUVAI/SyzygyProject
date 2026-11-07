"""Rebuild selected published decimal coordinates as exact sphere points."""
from fractions import Fraction
from pathlib import Path
from tasks.t040.init_program import configured_size


def run_code():
    n = configured_size()
    fields = (Path(__file__).parent / "data" / f"maxvol.3.{n}.txt").read_text(encoding="ascii").split()
    if len(fields) != 3 * n:
        raise ValueError(f"expected {n} archived triples")
    parameters = []
    for i in range(0, len(fields), 3):
        x, y, z = (Fraction(s) for s in fields[i:i+3])
        denominator = 1 + z
        if denominator == 0:
            raise ValueError("source point is at the omitted south-pole chart singularity")
        # Reconstruct the chart point on S² from the source's displayed
        # decimals; this exact map is not the original unrounded coordinate.
        parameters.append([str(x/denominator), str(y/denominator)])
    return {"stereographic": parameters}


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
