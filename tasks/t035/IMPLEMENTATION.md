# T035 implementation handoff

Status: **已通过 Sol 验收（2026-11-06）** (`accepted_by_sol`).

## Delivered

- Fixed configuration T035-C01: forbid a convex 7-gon; maximize the number of points. The objective is the witness size, not `ES(7)`.
- An exact integer/rational-string checker. It rejects floats, duplicate points, and collinear triples. It checks convex seven-subsets by an exact search over convex four-subsets. Claimed scores are ignored.
- A standalone six-point parabola seed and a fixed-seed greedy point-addition baseline. The baseline does not read reference files.
- A reconstruction of the published recursive 32-point construction, a saved witness, a replay reference, bilingual task notes, source hashes, and public-result records.

## Verification evidence

- The reconstructed witness contains 32 integer points. The largest absolute coordinate is 39,321,600.
- Exact checker result: objective 32; general position holds; no convex 7-gon exists.
- Fixed-seed baseline replay: objective 19 after 250 candidate additions, seed 0, 13.261466 seconds on the recorded local environment. Its point set is saved in `best/greedy-seed-0.json`; replay details are in `data/baseline_seed0_metadata.json`.
- Trusted worker round trip: the `human.py` `run_code()` generation subprocess returned the 32-point construction, and a separate checker subprocess recomputed objective 32 with exact status. `reference.py` uses a task-qualified import of this entry.
- Environment used for reconstruction: Python 3.13.12 on Linux x86_64. Search seed: 0. Baseline default: 250 candidate-addition attempts. Generation limit: 300 seconds. Verification limit: 60 seconds. CPU, one thread, and 4 GiB are the shared defaults.
- Reproduction command: `.venv/bin/python -c 'from tasks.t035.human import build_points; from tasks.t035.check import validate; print(validate(build_points(), {"forbidden_convex_polygon_vertices": 7}))'`.
- Source archive hashes are saved in `data/source_hashes.json`. The generated witness is from the formula and not digitized from a paper figure.
- Task tests after review fixes: `.venv/bin/python -m pytest tasks/t035 -q` — 17 passed in 3.37 seconds. JSON syntax checks passed for `task.json`, `sota.json`, `records.json`, both saved witnesses, `data/source_hashes.json`, and `data/baseline_seed0_metadata.json`.

## Checks and limits

The test suite includes the saved and generated witness, worker execution of the human `run_code()` entry, a legal initial program, a convex-seven rejection, duplicate and collinearity failures, booleans, finite floats, NaN, infinity, rational strings, the empty boundary, malformed data, and claimed-score tampering. It checks candidate errors and timeouts through the shared worker. The checker is exact but may exceed 60 seconds on large candidate sets; the trusted runner then reports verification timeout and does not record a score. No size cap prevents valid submissions above 32.

The reported upper bound 81 is cited but has not been reproduced here. The `ES(7)=33` conjecture remains open in the cited 2026-09-19 source snapshot. Sol should independently verify the construction's key claims, run the human program, inspect the starting point and greedy baseline, and review the public-result record before acceptance.
