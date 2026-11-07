# T049: minimum distinct distances for 91 points

## Objective

Choose 91 distinct points in the Euclidean plane and minimize the number of
distinct positive distances between unordered pairs. Points may have arbitrary
real coordinates. A score counts equal distances exactly; approximate numeric
comparison is not accepted.

The input represents all coordinates in one real algebraic number field
`Q(alpha)`. It gives an irreducible primitive integer polynomial for `alpha`,
a rational interval containing exactly one real root, and rational
polynomials for each coordinate. The checker uses exact rational polynomial
arithmetic modulo the minimal polynomial. It counts distinct squared distances,
which has the same equality relation as positive Euclidean distances.

This format does not change the infimum or minimum value for finite point
sets. Every finite equality/inequality pattern among squared distances is a
finite system of polynomial equalities and strict inequalities over `Q`. If
that system has a real solution, it has a solution over the real algebraic
numbers because the real algebraic numbers form a real closed field. A finite
set of algebraic coordinates lies in one number field, which has a primitive
element. Thus the checker can represent a minimizer whenever one exists.

## Human construction and open status

Erdős and Fishburn's Table 1 reports a regular hexagonal subset of the
triangular lattice with `n=91`, `s=6`, and `k=34`. The reconstructed points
are

```text
(x,y) = (i + j/2, sqrt(3) j/2)
max(|i|, |j|, |i+j|) <= 5,
```

which gives exactly 91 points. For a displacement `(a,b)`, the squared
distance is `a^2 + a*b + b^2`; exact enumeration gives 34 values. The saved
reference uses `alpha=sqrt(3)`, minimal polynomial `alpha^2-3`, and isolating
interval `(1,2)`. The public construction is reproduced exactly in
`human.py` and `reference.py`.

The checked exact-value sequence OEIS A186704 currently gives its full list
only through `n=13`. The current Erdős Problems database keeps the general
minimum-distinct-distances problem open, and we found no exact optimum result
for `n=91` in the sources checked on 2026-11-06. This is a bounded source
survey, not a proof that no result exists. The value 34 is a verified
construction (an upper bound on the minimum), not an optimum claim.

Sources:

- Erdős and Fishburn, “Maximum planar sets that determine k distances,”
  *Discrete Mathematics* 160 (1996), Table 1, p. 124:
  <https://doi.org/10.1016/0012-365X(95)00153-N>
- Public copy of the paper:
  <https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Erdos2.pdf>
- OEIS A186704, exact values currently listed through 13:
  <https://oeis.org/A186704>
- Erdős Problem #89, the distinct-distances lower-bound problem, marked open
  in the current maintained database:
  <https://erdosproblems.ai/problems/89>
- Guth and Katz, “On the Erdős distinct distance problem in the plane,”
  *Annals of Mathematics* 181 (2015):
  <https://annals.math.princeton.edu/wp-content/uploads/annals-v181-n1-p02-p.pdf>
- Erdős Problem #91, open non-uniqueness question for minimizers:
  <https://www.erdosproblems.com/91>
- Erdős Problem #89, the distinct-distances lower-bound problem, marked open
  in the maintained database:
  <https://erdosproblems.ai/problems/89>

## Programs and budgets

Run from the repository root with Python 3.11 or newer:

```sh
.venv/bin/python -m pytest tasks/t049 -q
.venv/bin/python -c 'from tasks.t049.human import run_code; from tasks.t049.check import validate; c={"id":"T049-C01","parameters":{"point_count":91,"ambient_space":"Euclidean plane R^2","coordinate_domain":"real algebraic coordinates in a common real algebraic number field"}}; print(validate(run_code(), c, strict=True))'
```

Generation has a 300 second limit. Verification has a separate 60 second
limit, 4 GiB memory limit, and one numerical thread. SymPy is a declared
project dependency; its exact polynomial routines verify irreducibility and
the rational root-isolation interval. The baseline has 128 fixed seeded
samples of 91-point subsets of a 10 by 10 integer grid. Setting
`MATHBENCH_SEARCH_SECONDS` enables a wall-clock exploration cutoff.

The initial program is 91 equally spaced collinear integer points. The search
baseline builds its own square-grid candidates and does not read comparison
data. Human and fixed-reference programs are external comparisons. The
checker validates one feasible construction and its exact score; it does not
prove global optimality.

The task remains `accepted_by_sol`.
