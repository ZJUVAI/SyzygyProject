from .check import validate

TASK = {
    "id": "T014-C01",
    "parameters": {"n": 11},
    "direction": "maximize",
    "human_reference": "1/27",
}


def run_code():
    """Return a deterministic, distinct, non-collinear rational seed."""
    return {"points": [[f"{i}/10", f"{i*i}/100"] for i in range(11)]}
