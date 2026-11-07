"""Traditional 26-product baseline: apply Strassen to the upper-left 2x2 block."""

from tasks.t029.init_program import run_code as schoolbook


def _linear(entries):
    result = [0] * 9
    for row, col, coefficient in entries:
        result[3 * row + col] += coefficient
    return result


def run_code():
    # Keep the 19 schoolbook products outside the upper-left 2x2 restriction.
    terms = [t for t in schoolbook()["terms"] if sum(t["alpha"]) == 1 and sum(t["beta"]) == 1
             and sum(t["gamma"]) == 1 and not (
                 next(i for i, x in enumerate(t["alpha"]) if x) // 3 < 2
                 and next(i for i, x in enumerate(t["alpha"]) if x) % 3 < 2
                 and next(i for i, x in enumerate(t["beta"]) if x) // 3 < 2
                 and next(i for i, x in enumerate(t["beta"]) if x) % 3 < 2
                 and next(i for i, x in enumerate(t["gamma"]) if x) // 3 < 2
                 and next(i for i, x in enumerate(t["gamma"]) if x) % 3 < 2)]
    # (A11+A22)(B11+B22)
    specs = [
        ([(0, 0, 1), (1, 1, 1)], [(0, 0, 1), (1, 1, 1)], [(0, 0, 1), (1, 1, 1)]),
        ([(1, 0, 1), (1, 1, 1)], [(0, 0, 1)], [(1, 0, 1), (1, 1, -1)]),
        ([(0, 0, 1)], [(0, 1, 1), (1, 1, -1)], [(0, 1, 1), (1, 1, 1)]),
        ([(1, 1, 1)], [(1, 0, 1), (0, 0, -1)], [(0, 0, 1), (1, 0, 1)]),
        ([(0, 0, 1), (0, 1, 1)], [(1, 1, 1)], [(0, 0, -1), (0, 1, 1)]),
        ([(1, 0, 1), (0, 0, -1)], [(0, 0, 1), (0, 1, 1)], [(1, 1, 1)]),
        ([(0, 1, 1), (1, 1, -1)], [(1, 0, 1), (1, 1, 1)], [(0, 0, 1)]),
    ]
    terms.extend({"alpha": _linear(a), "beta": _linear(b), "gamma": _linear(g)} for a, b, g in specs)
    return {"terms": terms, "search_metadata": {
        "algorithm": "schoolbook outside upper-left 2x2 block plus Strassen's seven products",
        "seed": 0, "iterations": 1, "reference_data_read": False,
    }}
