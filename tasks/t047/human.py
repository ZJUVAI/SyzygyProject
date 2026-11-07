"""Rebuild a classical Wichmann restricted-difference-basis construction."""

import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T047-C01") != "T047-C01":
        raise ValueError("unsupported configuration id")
    # Wichmann's complete sparse ruler W(38, 3) has 157 gaps and 158 marks.
    # Its length is 4*r*(r+s+2)+3*(s+1)=6548, so it covers [1,6166].
    # This restricted ruler is a valid witness for the task's unrestricted
    # integer-difference model. It is a weak human baseline, not the 128 record.
    r, s = 38, 3
    gaps = (
        [1] * r
        + [r + 1]
        + [2 * r + 1] * r
        + [4 * r + 3] * s
        + [2 * r + 2] * (r + 1)
        + [1] * r
    )
    basis = [0]
    for gap in gaps:
        basis.append(basis[-1] + gap)
    return {"basis": basis, "claimed_objective": len(basis)}
