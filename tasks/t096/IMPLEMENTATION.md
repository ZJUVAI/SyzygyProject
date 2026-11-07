# T096 implementation and verification

## Scope and sources

- Configuration: `T096-C01`, planar smooth strictly convex simple closed curves, perimeter `2*pi`.
- Objective: minimize the joint Rayleigh quotient over a curve and a nonzero periodic real trial function. Taking the infimum over trial functions for each curve gives its first eigenvalue, so the joint infimum is the Ovals constant.
- Benguria and Loss (2004) introduced the conjecture that this infimum is 1. The circle gives an exact feasible value 1.
- Denzler (arXiv:1301.6322; published 2015) proves existence and regularity for the relaxed problem. Its minimizer is either the digon, whose value is 1, or a positive-curvature analytic strictly convex curve. Since the circle gives value 1, restricting the encoded family to positive curvature does not change the infimum.
- Suragan (arXiv:2609.10775v1, 2026-09-09) gives a lower bound approximately `0.96183165233528` and states the sharp bound remains open. This lower bound is reported separately; it is not reproduced by this checker.

## Representation and checker

The curve is encoded by its curvature radius `rho(theta)=ds/dtheta`. The checker requires exact mean 1 and zero first harmonics, which give perimeter `2*pi` and closure. It requires a positive rational lower bound `delta` and proves `rho-delta >= 0` on the full circle. The tangent-half-angle substitution reduces this to a rational polynomial nonnegativity check. Exact square-free factorization and Sturm real-root counts verify that check; no angle sampling is used.

For the trial function, the checker performs exact rational Fourier arithmetic. It bounds `rho` above by its coefficient norm `M`. With `u=1-rho/M`, the claimed lower bound gives `0 <= u <= 1-delta/M`. A finite geometric sum gives a rational lower bound for the Rayleigh numerator; the tail bound `q^(K+1)/delta`, where `q=1-delta/M`, gives its rational upper bound. Dividing by the exact positive denominator gives `details.objective_interval`. The reported minimization score is the conservative upper endpoint. This interval is for the trial Rayleigh quotient; it is not a two-sided interval for the first eigenvalue.

Rational trigonometric polynomials preserve the full infimum. Fejér approximation of a smooth positive curvature radius preserves its mean and first harmonics, and uniform approximation preserves positivity. Rational coefficient approximation can preserve those linear constraints. Periodic trial functions are dense in `H^1` under trigonometric approximation. The Rayleigh quotient is continuous under these approximations when `rho` stays positive.

## Programs and results

- `init_program.py` returns the circle and constant trial function. It is self-contained and has the required EVOLVE-BLOCK markers.
- `human.py` encodes the classical exact unit-circle construction.
- `reference.py` replays `data/reference/circle.json`.
- `baseline.py` evaluates 24 seeded rational perturbations of `rho=1+epsilon*cos(2 theta)` and small first-harmonic trial perturbations. It retains the best exact certificate.
- `evolution.py` evaluates 32 seeded mutations of the same generated rational family. It reads no comparison data.

At default seed 0, all five programs return objective `1/1`. The saved reference has `rho=1`, `f=1`, and exact quotient 1. The circle spectrum is `1+k^2`, so its first eigenvalue is also exactly 1.

## Validation

Environment: Python 3.13.12, local `.venv`, SymPy 1.14.0, pytest 9.2.0.

Command:

```sh
.venv/bin/python -m pytest tasks/t096/test_task.py -q
```

Result: 7 passed in 3.18 seconds. Tests run all five program entries, check the circle, certify a nonconstant-radius case against the exact identity `Q=2/sqrt(3)`, accept sine terms in both the curve and trial function, reject a false lower bound whose cleared polynomial has negative leading coefficient, test closure and malformed numeric inputs, confirm forged scores do not affect validation, and exercise worker error and timeout reporting through `mathbench.evaluate._run`.

All task-local JSON files pass `python -m json.tool`. Status: `accepted_by_sol`.
