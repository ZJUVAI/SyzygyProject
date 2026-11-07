# T028 implementation notes

Status: accepted by Sol on 2026-11-06.

## Configuration and source data

- `T028-C01` fixes Taillard Ta051: 50 jobs, 20 machines, one common job permutation, and makespan minimization.
- The official `tai50_20.txt` snapshot has Ta051 seed 1539989115 and original header bounds 3480–3875. The Ta051 processing-time matrix was extracted from that snapshot into `data/ta051.json`. The JSON contains only the matrix. Its SHA-256 is `57e114d970f7af11c64a3280068ef2ee1cfc037afd312e30d0d176900df564de`. The full original source has SHA-256 `cc139745dece17a2538e74ad2eaed232cc97321293f6b121883a6e3c69c8f8ba`.
- Taillard's live bounds page, read 2026-11-06, reports Ta051 bounds 3771–3846 and says that only permutation schedules are allowed. Its dated header is 03.06.2026. The table attributes the upper bound to RRMRP and the lower bound to Va.
- The public upper-bound witness is the Ta051 permutation archived in Olivier Brunner's Zenodo v8 dataset and associated with Ravetti et al. (2012). Exact replay on the official input returns 3846. `data/source/` preserves the official data and bounds snapshots. The candidate input allowlist must contain only `data/ta051.json`.
- Gmys et al. (2022) list Ta051 among instances that remained open. The later Zenodo v11 page (2026-07-31) cautions readers about its `Optimal` field. We do not rely on that field to assert open status.

## Programs and exact verification

- `init_program.py` is self-contained and returns jobs 1 through 50 in identity order. It does not import task modules or read comparison data.
- `baseline.py` builds an NEH permutation, then runs a seeded swap/insertion local search with 2,000 fixed iterations by default. `MATHBENCH_SEARCH_SECONDS` enables the shared optional wall-clock cutoff. The result records the seed, iteration count, budget, algorithm, and that no reference data was read.
- `evolution.py` starts from an NEH order and uses order crossover, swap mutation, and a fixed population/generation budget. It records the seed, population, generations, cutoff, and comparison-data access status.
- `human.py` rebuilds the public reference from task-local witness data. `reference.py` is the fixed reference interface.
- `check.py` validates exactly one copy of each job label 1–50. It reads its fixed input independently of candidate output and recomputes the makespan with integer arithmetic for every operation. No float arithmetic or heuristic penalty is used. Claimed scores are ignored.

## Validation performed

Command:

```sh
.venv/bin/python -m pytest tasks/t028/test_task.py -q
```

Result: 9 passed in 4.35 seconds under Python 3.13.12. Tests independently extract the matrix from the official Taillard source snapshot, check both SHA-256 values, replay the 50-job reference, validate the identity seed, reject incomplete, duplicate, out-of-range, bool, noninteger, NaN, infinite, and non-permutation payloads, ignore altered and nonfinite claimed scores, check seeded baseline and evolution reproducibility, and verify generation error and timeout handling.

The reference permutation was independently recomputed as 3846. The fixed seed-0 NEH/local-search baseline returned 4078 in 2,000 iterations (about 1.40 seconds for generation in this run), then passed the exact checker. This run is saved under `best/T028-C01/` with a replay command. Full `evaluate_candidate` integration awaits the main reviewer adding T028 to shared registries.

## Open review items

- Sol must confirm the saved permutation matches the Ta051 row in the cited Zenodo v8 file and the RRMRP publication, then independently replay the human program.
- Sol must independently verify a key matrix quantity and exercise one valid result, one damaged permutation, a changed claimed score, a program error, and a timeout.
- Sol must review the open-status sources and confirm the candidate export contains only the matrix JSON, not the saved witness or source records.
- The exact optimum is unknown within the currently recorded interval 3771–3846. This task does not prove optimality.
