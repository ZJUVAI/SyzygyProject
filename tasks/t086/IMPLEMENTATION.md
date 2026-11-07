# T086 implementation and verification

Status: `accepted_by_sol`.

## Definition and source review

- Duchi's inside-sum formulation is in his COLT 2012 commentary, *Commentary on “Towards a Noncommutative Arithmetic-Geometric Mean Inequality”*: <https://citeseerx.ist.psu.edu/document?doi=619325d9c18b896b94f4de0bd5be63a749a1f21c&repid=rep1&type=pdf>. The commentary introduces the norm of each product as the summand and defines with- and without-replacement expectations.
- Current problem scope: *Mathematical exploration and discovery at scale*, arXiv:2511.02864 v1, §6.47: <https://arxiv.org/html/2511.02864v1>. The checked text states that `m>=4` remains open, includes `(4,4,3)` in its tested parameter choices, includes Schatten 2 among its norms, and reports that AlphaEvolve did not find a construction below the identity upper bound. The repository's extracted source text SHA-256 is `4934ab062476162665dcb49606c35387289447c1a194ef2d2198a9ffe2b3daf8`.
- The human/reference tuple is four copies of `I3`. All 256 and 24 products are exactly `I3`, each Frobenius norm is `sqrt(3)`, and the ratio is exactly 1. This is the standard traditional witness giving the upper bound 1, not a proof of the lower bound.
- The 2020 refutation by Lai and Lim addresses the Recht–Ré statement with the norm outside the sum: <https://proceedings.mlr.press/v119/lai20a.html>. The 2026 Evidence Press low-length Recht–Ré release is an unrefereed candidate and itself reports no unaffiliated rerun: <https://www.evidencepress.org/releases/exact-low-length-recht-re-inequalities/>. Both concern the outside-sum statement, so neither closes the Duchi inside-sum objective. No proof resolving this fixed `(4,4,3)`, Schatten-2 configuration was found in the sources checked on 2026-11-06.

## Exact input and checker

Each entry is `[real,imaginary]`; components are exact integers or rational strings. Floats are rejected. There is no coefficient precision cap. The checker verifies Hermitian symmetry and all one-, two-, and three-dimensional principal minors with exact `Fraction` arithmetic. This is the exact PSD criterion for 3x3 Hermitian matrices.

All 256 replacement products and all 24 distinct ordered products are multiplied with exact Gaussian rationals. Each squared Frobenius norm is an exact nonnegative rational. Integer `isqrt` bounds every square root by rational endpoints. The denominator lower bound is kept positive by choosing an interval scale from the smallest positive denominator norm. The ratio uses the lower numerator and upper denominator for its lower endpoint, and upper numerator and lower denominator for its upper endpoint. The upper endpoint is returned for minimization. If all four matrices are equal, all product norms are identical and their ratio is exactly 1; the checker proves this equality directly and confirms the common product norm is nonzero.

Rational inputs have the same infimum as complex PSD inputs. For each Hermitian PSD `A`, `A+epsilon I` is positive definite. Complex-rational Hermitian matrices are dense in Hermitian matrices, and sufficiently close approximants to this positive-definite matrix stay positive definite. Letting epsilon tend to zero gives rational PSD approximants to `A`. The objective is continuous wherever the without-replacement denominator is positive, and that positivity persists under sufficiently small perturbation. This preserves the infimum without excluding a better real or complex PSD tuple.

## Search isolation and recorded runs

`init_program.py` uses four identity matrices. `baseline.py` and `evolution.py` start from that simple construction and search only over positive diagonal integer matrices. They do not read human/reference data. The checker accepts arbitrary complex rational Hermitian PSD matrices. `human.py` independently constructs four identities; `reference.py` replays `data/reference/identity_psd_n4_d3.json`, SHA-256 `ed32b4e108875d14fdb1aec7308b6ebe902c95c9004bb3bdc5a155a1d0018eb7`.

Environment: repository `.venv/bin/python` (Python 3.13), seed 0, default fixed search budgets. The five entries returned exact checker scores `1`, `1`, `1`, `1`, `1`. The baseline ran 250 steps in about 1.51 seconds; evolution ran 50 generations with population 6 in about 0.02 seconds. Their `0.9999999999999999` heuristic value is floating-point search feedback only; exact checking returned 1.

Commands run:

- `.venv/bin/python -m pytest tasks/t086 -q` — 10 passed.
- Ran `init_program`, `baseline`, `evolution`, `human`, and `reference` through their module entry points, then checked each output.
- Validated task, SOTA, records, source notes, and reference JSON with `python -m json.tool` — passed.
- `git diff --check -- tasks/t086` — passed.

Task tests include the exact identity score, an independent decimal recomputation for a nonidentical diagonal tuple, a complex Hermitian PSD example, negative diagonal/2x2/full determinants, malformed shapes, booleans, floats, NaN, denominator zero, 100-digit rational entries, score-field tampering, all five programs, record consistency, and runner error/timeout paths.

Full AlphaEvolve search reproduction and external model comparisons have not been run. The AI-assisted paper result is recorded separately from the human identity baseline; it is not presented as a new AI construction or an optimality proof.
