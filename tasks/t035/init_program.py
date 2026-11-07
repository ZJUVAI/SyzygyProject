"""Small standalone seed for the T035 search interface."""


def run_code():
    # Six integer points on y=x^2 are in general position and cannot contain
    # a seven-point subset. The model can grow or replace this construction.
    return {"points": [[x, x * x] for x in range(6)], "claimed_objective": 6}
