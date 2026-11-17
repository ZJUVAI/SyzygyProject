# T025 implementation notes

Status: accepted by Sol on 2026-11-06.

## Configuration and sources

- `T025-C01` fixes the affine space `F_3^7` and maximizes cap cardinality. The checker limits candidates to 288 points because Thackeray proves that no 289-cap 7-flat exists. This is a theorem-derived candidate ceiling, not a reported construction.
- Edel and Bierbrauer (2001), Table 2 and Theorem 5, give a 236-cap in `AG(7,3)` and identify it as the Calderbank–Fishburn cap. Calderbank and Fishburn (1994) are credited with the first 236-cap.
- The public matrix page `https://www.yvesedel.de/Matritzen/CAPs/Matrizen/(248,7,3).html` was retrieved on 2026-11-06. Its eight rows each have 248 ternary entries. The eighth row has 236 entries equal to 1. `human.py` extracts those columns, drops the eighth coordinate, and rebuilds the affine point list.
- The saved matrix has SHA-256 `0e3ad612ca8ee9259290f4748af505cf6184c2107e77859d3ae6117fe24545eb`. The saved point witness has SHA-256 `40e588a2a8b17cacb2443a60bd9cfd1c94ded78fdfdde13adee4d74af59c9159`.
- Thackeray, arXiv:2206.09804 (2022), proves the upper bound 288. The literature check found no proof of the exact maximum. Current located bounds are 236 to 288.

## Programs and exact verification

- `init_program.py` returns all 128 binary vectors in `F_3^7`. This is a valid cap and uses no comparison data.
- `baseline.py` uses Python's seeded random generator to order candidate points and greedily add each point whose addition preserves the cap property. It has a fixed 100,000-candidate budget by default. `MATHBENCH_SEARCH_SECONDS` enables the shared optional wall-clock cutoff. Search metadata records the seed, fixed budget, actual iteration count, restart count, and whether reference data was read.
- `human.py` reconstructs the published affine slice from the saved public matrix. `reference.py` loads the fixed point witness.
- `check.py` validates each coordinate and duplicate, then checks every distinct pair. For a pair `a,b`, the only possible third point is `-a-b` modulo 3. A candidate score field is ignored. The integer arithmetic covers the full domain exactly. No sampling is used.

## Validation performed

Command:

```sh
.venv/bin/python -m pytest tasks/t025/test_task.py -q
```

Result: 16 passed in 4.50 seconds under Python 3.13.12. The suite rebuilds and checks the 236-point matrix slice, independently recalculates its cardinality, validates the simple seed, rejects a collinear triple, duplicate points, wrong shapes, bool, noninteger, out-of-range, NaN, and infinite coordinates, ignores a claimed score, checks the 288-point theorem cutoff, tests seeded search reproducibility and zero-second fallback, and exercises the shared process runner's program-error and timeout handling.

The automated test uses the deterministic local matrix snapshot. No network fetch is performed by tests. The main reviewer must independently replay the human baseline and compare the local source row interpretation against the cited paper and the author's page.

## Open items for review

- The exact maximum in `F_3^7` remains unproved. The 288 limit is an upper bound only.
- The public matrix is projective; the affine witness is the slice with last coordinate 1. Sol should check this extraction convention and the affine no-line proof.
- The repository's shared evaluator registry has not yet been updated for T025. End-to-end `evaluate(program_path)` testing must follow main-agent integration. This task does not change shared files.
