"""Generic seeded placement search. It has no comparison-data dependencies."""
from fractions import Fraction
import os
import random
import time

from tasks.t083.check import Q, _max, _min, _triangle, validate


CONFIG = {"id": "T083-C01", "parameters": {
    "triangle_count": 4, "triangle_side": 1,
    "container": "axis-aligned square with lower-left corner (0,0)",
    "pose_domain": "dense Q(sqrt(3)) translations and rational unit directions",
}}


def _seed():
    anchors = [(0, 0), (1, 0), (0, 1), (1, 1)]
    return {"side": ["2", "0"], "triangles": [
        {"anchor": [[str(x), "0"], [str(y), "0"]], "direction": ["1", "0"]}
        for x, y in anchors
    ]}


def _serialize_q(value):
    def f(x):
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return [f(value.a), f(value.b)]


def _normalize(records):
    tris = [_triangle(r) for r in records]
    xs = [p[0] for tri in tris for p in tri]
    ys = [p[1] for tri in tris for p in tri]
    xmin, ymin = _min(xs), _min(ys)
    xmax, ymax = _max(xs), _max(ys)
    side = _max([xmax - xmin, ymax - ymin])
    out = []
    for r in records:
        anchor = [Q.parse(c) for c in r["anchor"]]
        out.append({"anchor": [_serialize_q(anchor[0] - xmin), _serialize_q(anchor[1] - ymin)],
                    "direction": r["direction"]})
    return {"side": _serialize_q(side), "triangles": out}


def search(iterations, *, evolutionary=False):
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    incumbent = _seed()
    best = Q.parse(incumbent["side"])
    tested = valid = improved = 0
    directions = [("1", "0"), ("0", "1"), ("-1", "0"), ("0", "-1"),
                  ("3/5", "4/5"), ("4/5", "-3/5"), ("-3/5", "4/5"), ("-4/5", "-3/5")]
    cutoff = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None if cutoff is None else time.monotonic() + max(0.0, float(cutoff))
    for step in range(iterations):
        if deadline is not None and time.monotonic() >= deadline:
            break
        candidate = {"side": incumbent["side"], "triangles": [dict(t) for t in incumbent["triangles"]]}
        idx = rng.randrange(4)
        if evolutionary and step % 3 == 0:
            # A small population-style mutation changes two independently selected poses.
            changed = {idx, rng.randrange(4)}
        else:
            changed = {idx}
        for j in changed:
            x, y = rng.randrange(-1, 3), rng.randrange(-1, 3)
            candidate["triangles"][j] = {
                "anchor": [[str(x), "0"], [str(y), "0"]],
                "direction": list(rng.choice(directions)),
            }
        candidate = _normalize(candidate["triangles"])
        tested += 1
        try:
            validate(candidate, CONFIG)
            score = Q.parse(candidate["side"])
            valid += 1
        except ValueError:
            continue
        if score < best:
            incumbent, best = candidate, score
            improved += 1
    incumbent["search_metadata"] = {
        "algorithm": "seeded random anchor and rational-direction mutation with exact feasibility checks",
        "fixed_iterations": iterations,
        "candidate_count": tested,
        "valid_candidate_count": valid,
        "improvement_count": improved,
        "seed": int(os.environ.get("MATHBENCH_SEED", "0")),
        "comparison_data_read": False,
        "starting_side": 2,
    }
    return incumbent
