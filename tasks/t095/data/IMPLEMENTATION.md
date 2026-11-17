# T095 implementation and verification

## Frozen instance and sources

- Configuration: `T095-C01`, CG:SHOP 2020 `uniform-0000500-1`, 500 points.
- Input SHA-256: `c8ea5c524c52a6d7e0188f566482c124856a8cbd0318e518ff4419f09844c31a`.
- Archived solution SHA-256: `f3de71a8fa4f98adf3314ccc2aa780e594e933b051e3d7cc715d1944eeb01190`.
- The source archive supplies a 770-edge feasible partition. The exact checker finds 271 bounded faces. Its metadata gives a date but no producing method, solver, or AI provenance. The score is not an optimality proof.
- Hadrien Cambazard's project page reports optimality results for 100-point data sets and lower bounds up to 300 points. It does not give a proof for this 500-point instance. The source audit date is 2026-11-06.
- An exact determinant scan checked all 20,708,500 triples of input points and found no collinear triple.
- `data/source/source_notes.json` records URLs, hashes, provenance, and the checks above.

## Programs

- `init_program.py` returns the SciPy Delaunay triangulation. It reads only the fixed public input and has no imports from this task package.
- `human.py` reconstructs the traditional Delaunay-plus-convex-edge-removal method described by Eder, Held, de Lorenzo, and Palfrader (SoCG 2020, section 2.2, pages 85:2-3). The local deterministic implementation was built with AI assistance; it is not the paper's code or score. Exact validation gives 384 faces.
- `baseline.py` runs four seeded greedy trials over fixed merge policies.
- `evolution.py` mutates greedy merge-policy weights for a fixed number of steps. Its search starts from the input and does not load human or public comparison data.
- `reference.py` loads the pinned public 770-edge construction.

Observed objectives at the saved defaults were: initial Delaunay 979, human-method reconstruction 384, traditional search 398, evolution search 368, and public reference 271. Search scores may vary when the documented seed or iteration settings change. The reference and human values are fixed and replayable.

## Exact validation

`check.py` reads coordinate literals as `Decimal`, accepts only exact finite integer coordinates, and performs all geometric predicates with integers. It checks every edge endpoint and every pair of edges, then verifies vertex coverage, connectivity, the convex-hull boundary, planar face walks, simple convex empty bounded faces, Euler's face count, and exact area coverage. The objective is recomputed from bounded faces. Candidate fields named `objective`, `score`, or `claimed_score` do not affect the result.

The maximum possible simple planar edge count bounds the pairwise checks. The expected verification budget is 60 seconds on one CPU thread. Strict mode uses the same exact geometric checks; it does not substitute sampling or floating-point tolerances.

## Validation run

Environment: Python 3.13.12, NumPy 2.4.3, SciPy 1.17.0, local `.venv`.

Command:

```sh
.venv/bin/python -m pytest tasks/t095/test_task.py -q
```

The task tests replay the pinned input and official solution, run the human baseline and all five program entries, reject a missing hull edge, duplicate edge, self-loop, invalid endpoint, and a crossing edge, check strict fixed parameters, confirm forged score fields do not alter the validation result, and exercise worker error and timeout reporting through `mathbench.evaluate._run`.

All task-local JSON files are checked with `python -m json.tool` as part of delivery. Status: `accepted_by_sol`.
