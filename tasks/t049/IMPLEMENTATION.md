# T049 implementation record

Status: `accepted_by_sol`.

## Fixed configuration

- Configuration: `T049-C01`, 91 distinct points in the Euclidean plane.
- Objective: minimize the number of distinct positive pairwise Euclidean distances.
- Direction: minimize. A lower objective is better.
- Frozen human reference: `H=34`.
- Published lower bound: `m(91)>=9`, from the inequality `n-1<=k(k+1)` in
  Erdős (1946), Theorem 1.
- Human source: Erdős and Fishburn (1996), Table 1, `L_delta`, `n=91`,
  `k=34`, `s=6`. The coordinate reconstruction is in `human.py`.
- Fixed reference: `data/reference/hexagon_n91.json`.
- Reference SHA-256:
  `0ad19d47fe6dbfb77f7456119cd1a09e80c05b20d900eb4e59f1dc2583b167ac`.
- Source evidence and the bounded open-status check:
  `data/source/research_evidence.md`.

## Verification method

The checker verifies an irreducible primitive integer minimal polynomial and
uses an exact Sturm root count to confirm one real root in the supplied
rational interval. It reduces rational coordinate polynomials modulo that
minimal polynomial. It then computes every one of the 4095 squared distances
in `Q(alpha)` and counts equal reduced coefficient tuples. This is exact; no
floating-point coordinate or distance comparison is used. Any optional
candidate score is ignored, and the complete validation result is invariant
under changes to `objective`, `score`, or `claimed_score`.

An independent direct enumeration of the lattice displacement form
`a^2+ab+b^2` also returned 34 values from 91 points. The task checker returned
34 for both the independently rebuilt human construction and the frozen
reference.

## Initial program and traditional search

The initial program is 91 collinear integer points and has 90 distinct
distances. The traditional baseline samples 91-point subsets of the 10 by 10
integer square grid, keeps its best exact integer squared-distance count, and
uses seed 0 by default. It has 128 fixed attempts. Its saved seed-0 result is
in `best/baseline_seed_0.json`; it has objective 49. It does not read the
human or reference witness.

## Validation performed

Commands run with the repository `.venv`:

```sh
.venv/bin/python -m pytest tasks/t049 -q
.venv/bin/python -m json.tool tasks/t049/task.json >/dev/null
.venv/bin/python -m json.tool tasks/t049/records.json >/dev/null
.venv/bin/python -m json.tool tasks/t049/sota.json >/dev/null
```

Results:

- Task tests after the coordinate-domain, open-problem source, and lower-bound
  updates: 18 passed in 13.36 seconds.
- Human reconstruction and frozen reference: exact objective 34.
- Initial collinear seed: exact objective 90.
- Traditional baseline, seed 0, 128 iterations: exact objective 49.
- Independent triangular-lattice formula enumeration: 91 points and 34
  squared-distance values.
- Runner candidate-error and timeout cases use `mathbench.evaluate._run`;
  both passed in the task tests. The task ID remains unregistered until Sol
  admission, so no shared registry change was made.

## Source and optimality limits

Table 1 supports a 34-distance construction. OEIS A186704 currently lists
the exact sequence only through 13, and the checked sources did not report an
exact value for 91. This does not prove that no exact result exists. The
configuration is an open candidate based on the checked survey; Sol should
recheck this status before admission. The checker certifies feasible scores,
not global optimality.
