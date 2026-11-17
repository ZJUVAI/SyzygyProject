"""Fixed search counts by default; optional wall-clock cutoffs for exploration."""
import os
import time


def search_deadline():
    value = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    return float("inf") if value is None else time.monotonic() + max(0., min(240., float(value)))


def search_steps(count):
    deadline = search_deadline()
    for step in range(count):
        if time.monotonic() >= deadline:
            break
        yield step


def linear_polish(x, deadline, signed=False):
    """Refine a sequence by minimizing its convolution peak."""
    import numpy as np
    from scipy.optimize import linprog

    n = len(x)
    radius = 0.002 if n > 100 else 0.03
    while time.monotonic() < deadline and radius > 1e-10:
        conv = np.convolve(x, x)
        idx = np.arange(2*n-1)[:, None] - np.arange(n)[None, :]
        jac = 2*x[np.clip(idx, 0, n-1)] * ((idx >= 0) & (idx < n))
        a = np.c_[jac, -np.ones(2*n-1)]
        b = -conv
        if signed:
            a = np.r_[a, np.c_[-jac, -np.ones(2*n-1)]]
            b = np.r_[b, conv]
        bounds = [(max(-radius, -v) if not signed else -radius, radius) for v in x] + [(None, None)]
        result = linprog(np.r_[np.zeros(n), 1.0], A_ub=a, b_ub=b,
                         A_eq=np.r_[np.ones(n), 0.0][None, :], b_eq=[0.0],
                         bounds=bounds, method='highs', options={'time_limit': max(.01, deadline-time.monotonic()), 'threads': 1})
        if not result.success:
            break
        trial = x + result.x[:n]
        old = np.max(np.abs(conv)) if signed else np.max(conv)
        newconv = np.convolve(trial, trial)
        new = np.max(np.abs(newconv)) if signed else np.max(newconv)
        if new < old:
            x = trial
            radius = min(radius*1.15, .01)
        else:
            radius *= .5
    return x
