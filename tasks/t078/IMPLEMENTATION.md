# T078 implementation record

Status: accepted by Sol on 2026-11-06.

## Fixed objective and validation

`T078-C01` accepts an exact rational symmetric positive definite 10 by 10
matrix `G`, requires `z^T G z >= 4` for every nonzero integer vector, and
minimizes `det(G)`. Rational entries are integers or normalized fraction
strings. The checker validates symmetry, computes exact LDL factors, and
derives each integer-coordinate range from the remaining exact ellipsoid
radius. It enumerates the full ellipsoid below norm 4 and has no coordinate or
coefficient cap. It returns an exact integer or rational determinant. Candidate
objective and score fields do not affect the result.

The rational domain preserves the global optimum: a minimizing lattice form
is a perfect form by Voronoi theory. Its minimal-vector equations have integer
coefficients and right side 4. Perfection makes the solution unique, so the
matrix entries are rational. This task therefore does not bound Gram
coefficients or restrict the target to an artificial finite box.

## Source and reproduced public construction

The author-hosted LAMBDA10 catalogue page was independently downloaded on
2026-11-06. Raw source file:
`data/source/lambda10.html`, 10,728 bytes, SHA-256
`10a1fa86d38c92c30d4df0f95169d0fee64e3584bc7316e35b19d0c325229c1a`.
Its page states dimension 10, determinant 768, minimum norm 4, kissing number
336, and includes the exact integer Gram matrix. `human.py` parses this saved
source's GRAM section. `reference.py` loads the separate transcription in
`data/reference/lambda10_gram.json`.

The source Gram file hash is
`b515415581cb5044212b611d12ef3cf7cdc396b0f07d1c8cd7c605ae3750e886`.
The exact checker reports determinant 768 and no nonzero vector below squared
norm 4. A second full enumeration of vectors with norm at most 4 found exactly
336, all of norm 4. The saved list in
`data/human/lambda10_minimal_vectors.json` has SHA-256
`5499f6ee57683d10f366ce1f50a787b44e4baec94ff7169a4852ef5017144ea9`.

## Current optimality evidence

The 2026 v2 paper by Dutour Sikirić and van Woerden enumerates all perfect
forms in dimension 9 and proves the Lambda9 optimum. It does not close the
10-dimensional case. A 2022 SIAM paper reports exact Hermite constants only
in dimensions 1–8 and 24; it predates the 2026 dimension-9 result. The
2009 Cohn-Kumar paper also notes dimension 10 was unresolved then. A search of
current results checked on 2026-11-06 found no later proof for dimension 10.
The 768 determinant is recorded as a public feasible upper bound. It is not
recorded as an established minimum.

## Programs and saved search result

- `init_program.py` returns `4I`, a feasible form with determinant 1,048,576.
- `baseline.py` runs 32 seeded trials over scaled classical Cartan Gram forms
  for A10, D10, E8+A2, and 4I. It reads no human or reference data.
- `human.py` reconstructs the published LAMBDA10 matrix from the frozen
  catalogue HTML.
- `reference.py` loads the fixed, locally transcribed catalogue witness.
- `evolution.py` invokes the task search baseline.

The seed-0 baseline returned E8+A2 with exact determinant 3,072 in 0.00025
seconds on Python 3.13.12 / Linux. Its witness and run metadata are saved in
`best/seed-0.json` and `best/seed-0.metadata.json`. The run uses 32 fixed trials;
the recorded evaluator budget is 300 seconds generation, 60 seconds
verification, 4 GiB, and one thread.

## Tests

Command:

```sh
.venv/bin/python -m pytest tasks/t078/test_task.py -q
```

Result: 16 passed in 0.53 seconds. Tests exercise all five program entries,
recompute the 768 public result and the 3,072 root-system baseline, compare the
full set of 336 shortest vectors, reject non-positive forms, asymmetry,
short vectors, wrong shapes, booleans, floats, NaN and malformed fractions,
accept a 5,001-digit integer entry, confirm claimed-score invariance, and
check subprocess error and timeout handling through `mathbench.evaluate._run`.
All task JSON files and saved result JSON files parse. `git diff --check` passes.

## Sources checked on 2026-11-06

- [Nebe and Sloane, LAMBDA10 catalogue entry](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/LAMBDA10.html), page last modified 2014-07-18.
- [Dutour Sikirić and van Woerden, dimension 9 by Voronoi's algorithm](https://arxiv.org/abs/2508.20719), v2, 2026-02-07.
- [Dutour Sikirić et al., Dense Generic Well-Rounded Lattices](https://epubs.siam.org/doi/10.1137/22M1532779).
- [Cohn and Kumar, Optimality and uniqueness of the Leech lattice among lattices](https://annals.math.princeton.edu/wp-content/uploads/annals-v170-n3-p01-p.pdf), 2009, §1.
