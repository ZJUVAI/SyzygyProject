# T092 implementation and verification

Status: `accepted_by_sol`.

## Source review

- Stanton and Weinstein, *On the L4 norm of spherical harmonics*, 1981, DOI [10.1017/S0305004100058229](https://doi.org/10.1017/S0305004100058229). The first-party Cambridge abstract says the highest-weight function locally maximizes the L4 norm among L2-normalized spherical harmonics of each degree. The theorem is local. Section 6 gives an O(l log l) upper bound and does not state a degree-20 global best constant.
- Sogge's 1986 spherical harmonic estimate gives sharp asymptotic order, not this finite degree-20 constant.
- The October 2026 Rudin result, [arXiv:2610.14160](https://arxiv.org/abs/2610.14160), concerns uniformly bounded orthonormal bases of homogeneous holomorphic polynomials on complex spheres. It does not solve this real fixed-degree maximization.
- Searches through 2026-11-06 for a degree-20 global L4/L2 result found no closure.

## Exact construction and score

`human.py` rebuilds `Re((x+i y)^20)`. Its harmonicity follows from the opposite x and y second derivatives; the checker also verifies every rational Laplacian coefficient. The checker uses 231 rational monomial coefficients, computes P² and P⁴ exactly, and integrates each monomial using exact normalized sphere moments. It derives M2 `137438953472/1412926920405` and M4 `37778931862957161709568/725673658950019191115935`. The resulting exact objective is `fourth_root(58188232951867590/10575651537777253)` with the rational interval saved in `records.json`.

The real coefficient space is finite-dimensional and is the kernel of a rational matrix. Rational vectors span a dense subset of its real kernel. The objective is continuous on nonzero polynomials and invariant under nonzero scaling, so this formal rational domain has the same supremum. No degree, coefficient, or denominator cap is imposed.

The initial program builds the homogenized Legendre zonal harmonic P20(z). Search uses a three-axis rational zonal-harmonic basis and sampled sphere points for feedback only. The trusted checker recomputes exact moments for the final construction. Human and reference data remain under `data/`; the task's own best remains under `best/`.

## Validation commands

- `.venv/bin/python -m pytest tasks/t092 -q`
- `.venv/bin/python -m json.tool tasks/t092/task.json > /dev/null`
- `.venv/bin/python -m json.tool tasks/t092/sota.json > /dev/null`
- `.venv/bin/python -m json.tool tasks/t092/records.json > /dev/null`

Tests cover exact human moments, harmonic and nonharmonic examples, zero and malformed inputs, huge rational coefficients, claimed-score invariance, scale invariance, all five `run_code()` entries, cold-start isolation, deterministic search, runner errors/timeouts, and evaluator execution with a temporary registry patch. Use Python 3.13.12 and one numerical thread. The recorded run uses seed 0 and 16 fixed proposals.
