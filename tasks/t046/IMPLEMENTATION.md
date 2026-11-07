# T046 implementation notes

Status: `accepted_by_sol`.

The selected configuration is T046-C01: minimize the full-domain supremum
norm of a nonzero integer polynomial of degree at most 146 on `[0,1]`. The
checker does not limit the candidate class to a factor library.

The checker converts the exact integer power coefficients to exact rational
Bernstein coefficients. It adaptively bisects intervals with the largest
current upper bound. Bernstein convexity proves each upper bound over the full
interval; dyadic evaluations are lower bounds only. It stops when the rational
enclosure has relative width at most `1e-10`, or raises an error at 100,000
splits. The reported objective is the conservative upper endpoint, so a
candidate is credited with a safe score for this minimization task.

The simple cold start is `x^146`, with exact norm 1. The frozen weak human
baseline is reconstructed from the published factor `h1=x(1-x)`: `h1^73`,
degree 146, with exact norm `2^-146`. The exponent is our benchmark choice,
not a witness copied from the thesis's n=146 table row. The thesis reports
only `>=2.346298` in its reciprocal-nth-root column for n=146, with no
polynomial in that row. The reported value is converted to an upper bound on
the raw norm in `sota.json` and marked as not locally certified. See
`data/source/research_evidence.md`.

The traditional baseline enumerates all 74 products `h1^a h2^b` with
`h2=2x-1`, `2a+b=146`, in a seeded order. It ranks them by a 513-point dyadic
sample. This sample is search guidance only. The checker always recomputes a
rigorous enclosure before scoring.

## Local verification

Ran `.venv/bin/python -m pytest tasks/t046 -q`: 17 tests passed in 28.37
seconds. The tests cover the cold start, human/reference reconstruction,
degree boundary, constant and linear examples, exact `x(1-x)` norm, trailing
zero normalization, zero polynomial, bool/float/NaN/infinity rejection,
configuration rejection, forged objective invariance, deterministic search,
zero-second search cutoff, and `_run` program-error and timeout behavior.

All four `run_code()` programs were replayed and passed strict validation.
The human and fixed reference return exact norm
`1/89202980794122492566142873090593446023921664` with a one-split exact
enclosure. The cold start `x^146` has exact norm 1. The saved traditional
search result uses `h1^58 h2^30`, with `h2=2x-1`; its exact certificate used
38 dyadic interval splits and returned a rational enclosure of relative width
at most `1e-10` in 13.624 seconds. JSON syntax checks passed for `task.json`, `sota.json`, and
`records.json`. Runtime was Python 3.13.12 on Linux x86_64; the ordinary task
test command was run without claiming an additional memory cap outside the
shared evaluator.

The mathematical source check used Meichsner's thesis and the fixed v2 version
of Hare–Hodges' arXiv paper for finite degrees, plus arXiv:2610.00386v3
(2026-10-12) for the newest checked asymptotic bounds. The finite n=146 status
and the scope limits are in `data/source/research_evidence.md`.

No shared files or public task registry were changed. This implementation is
submitted accepted by Sol on 2026-11-06.
