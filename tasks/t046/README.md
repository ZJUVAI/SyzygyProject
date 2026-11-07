# T046: integer Chebyshev polynomial on `[0,1]`

## Definition

For the fixed degree limit `n=146`, find a nonzero polynomial
`P(x) in Z[x]` with `degree(P) <= 146` that minimizes

`||P||_[0,1] = max_{0 <= x <= 1} |P(x)|`.

This definition allows every nonzero integer polynomial through degree 146.
It does not restrict candidates to products of known factors. Published work
states that an optimizer has degree exactly `n` for `n >= 2`, but the checker
still accepts every valid degree-at-most-146 candidate.

The checker uses exact rational Bernstein coefficients and dyadic subdivision.
On each interval, the polynomial is a convex combination of its Bernstein
coefficients, so their largest absolute value is a rigorous upper bound. Exact
dyadic evaluations give a lower bound. The returned interval encloses the
whole-domain supremum norm. Sampling is used only by the search baseline.

The frozen human baseline is the weak same-parameter reconstruction
`P(x)=(x(1-x))^73`, with exact norm `2^-146`. Meichsner defines
`h1(x)=x(1-x)`; the exponent 73 and this n=146 witness are reconstructed for
this benchmark. The thesis's n=146 table row gives only a one-sided
reciprocal-root bound and no polynomial. The reported bound is converted to
the raw objective in `sota.json`; it is not the frozen human normalization.
See [source evidence](data/source/research_evidence.md).

## Open status and sources

Meichsner's 2009 thesis reports complete finite-degree results through 145;
its n=146 table row does not give an optimizer. Hare and Hodges (arXiv
1804.05985v2, 2018) added proved cases from degree 147 upward and reported
remaining unknown cases below 244. The latest checked 2026 paper proves new
bounds for the asymptotic integer Chebyshev constant, not for finite degree
146. We found no later n=146 completion in the sources checked by
2026-11-06. This is not an exhaustive survey claim.

- Meichsner (2009), thesis: <https://www.collectionscanada.gc.ca/obj/thesescanada/vol2/002/NR59810.PDF>
- Hare and Hodges, arXiv:1804.05985v2: <https://arxiv.org/abs/1804.05985v2>
- Niedbala Giraudin, arXiv:2610.00386v3: <https://arxiv.org/abs/2610.00386v3>

## Run and budget

Use Python 3.11 or newer. No non-standard package is required.

```sh
.venv/bin/python -m pytest tasks/t046 -q
.venv/bin/python -c 'from tasks.t046.init_program import run_code; from tasks.t046.check import validate; p={"degree_at_most":146,"interval":[0,1],"coefficient_domain":"nonzero integer polynomials"}; print(validate(run_code(), {"parameters":p}, strict=True))'
```

Generation has a 300 second limit. Verification has a separate 60 second
limit. The checker caps its subdivision work at 100,000 exact splits and raises
`ValueError` if it cannot complete a certificate. The shared runner applies
the 4 GiB memory limit and one-thread setting. The traditional search uses a
fixed limit of 74 factor-exponent trials by default; setting
`MATHBENCH_SEARCH_SECONDS` enables a wall-clock exploration cutoff.

The initial program is the simple monomial `x^146`. The traditional
baseline ranks products `h1^a h2^b`, where `h1=x(1-x)`, `h2=2x-1`, and
`2a+b=146`, on a 513-point dyadic grid. Neither program reads comparison data.
The fixed reference and human programs are external comparisons.

The task remains `accepted_by_sol`. Its objective is open; the checker
certifies feasible candidates and their scores, not global optimality.
