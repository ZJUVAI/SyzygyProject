# T029 implementation notes

Status: accepted by Sol on 2026-11-06.

## Configuration and sources

- `T029-C01` fixes 3×3 matrix multiplication over Q, exact bilinear terms, and a 27-term resource cap. Its objective is the number of nonzero simple tensor terms, equal to the scalar multiplication count in a bilinear algorithm.
- Tomar, arXiv:2610.11823v3, Section 1 (19 October 2026) states characteristic-zero rank remains unknown between 19 and 23. The paper proves rank 23 over F2 and the corollary for integer coefficients. This does not give a lower bound of 23 for arbitrary rational coefficients.
- The public Lille page identifies its ⟨3×3×3:23⟩ data as Laderman's 1976 algorithm and links to a Maple tensor representation. The original compressed file `data/source/3x3x3_tensor.mpl.bz2` has SHA-256 `c145cff7708b8472de23e0112c0722cae05f08bed2d9883b8dbf98cbb843169e`. Its decompressed text SHA-256 is `0ee5814978ec6b35d2041d00b976b8c3a6b2a0f391836184d803b89c91b97c08`.
- `human.py` parses 69 matrices from that source, groups them into 23 triples, sets λ=1 (all occurrences are λ or λ⁻¹, so this is a valid nonzero rational specialization), and transposes the third factor as shown by the source's `Transpose(op(...,3))` evaluation expression. The normalized witness SHA-256 is `c1debbeebc30dd64034ae83e1cbe9f5f7f3f112cbe7fe8db54cb152313994977`.
- `best_human`, `best_public`, and `best_reproduced` are distinct in `records.json`; the witness is labelled human-authored and no optimality claim is made.

## Programs and exact verification

- `init_program.py` is self-contained schoolbook multiplication with 27 rank-one tensor terms. It does not import task code or read comparison data.
- `baseline.py` removes the eight schoolbook products inside the upper-left 2×2-by-2×2 restriction and adds the seven standard Strassen terms, for 19+7=26 terms. It does not read human/reference data.
- `evolution.py` exposes `run_code()`. It performs seeded bounded randomized greedy deletion trials on the 27 schoolbook terms. Each deletion is retained only after exact tensor validation. This search only explores subsets of the seed and does not evolve rational coefficients; it is a deliberately narrow traditional search baseline.
- `human.py` rebuilds the public factor triples from the archived source. `reference.py` returns the fixed normalized witness.
- `check.py` accepts integers, rational strings, and exact `Fraction` objects. It rejects floats, bools, zero factors, malformed vectors, and more than 27 terms. It evaluates the full 9×9×9 tensor identity with `Fraction`; no candidate score field is read.

## Validation performed

Command: `.venv/bin/python -m pytest tasks/t029/test_task.py -q` — 9 passed in 4.25 seconds. Tests replay all five program interfaces, verify the exact Laderman witness, validate the 27-term seed and 26-term Strassen construction, accept rational noninteger coefficients including a `Fraction`, reject a replaced/duplicated term and malformed/nonfinite coefficients, ignore altered claimed scores, and check `evolution.run_code()`. The suite also exercises shared-runner program-error and timeout handling. The fixed evolution baseline returned 27 terms after 108 seeded deletion attempts; the exact checker accepted it. A separate direct replay returned 23 terms for `human.py`, 26 for `baseline.py`, and 27 for `init_program.py`. JSON syntax checks passed for `task.json`, `records.json`, and `sota.json`.

## Open review items

- Sol must independently replay the human parser and verify the output transpose against the Lille page's evaluation expression.
- Sol must independently recompute at least one key tensor coefficient and exercise a valid example, a damaged example, and a changed claimed score.
- Rank over Q remains unknown in the cited interval 19–23. The reproduced 23-term construction is an upper bound only.
- Full shared-runner registry integration is owned by the main reviewer; this task does not edit shared files.
