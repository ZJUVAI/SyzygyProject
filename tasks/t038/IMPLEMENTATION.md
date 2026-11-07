# T038 implementation record

Status: accepted by Sol on 2026-11-06.

Configuration `T038-C01` fixes order 12, maximizes the number of mutually orthogonal Latin squares, and uses the verified five-square human witness as its frozen reference. `sota.json` pins Sage 10.10 to tag commit `cb359e4c6e3b52e1bfc7f4f152e7db3ebd5f5d03` and records the raw source, function-fragment, and extracted data SHA-256 values. Sage code was not run.

Validation uses exact Python integers. It checks all 12 row and column permutations for each square, all 144 ordered pairs for each square pair, the 11-square universal upper bound, malformed values, and duplicate squares. The objective is the checked square count. All submitted objective and score fields are ignored, and a fixed detail states this. The source witness has ten square-pair checks. The MacNeish baseline independently constructs two MOLS using GF(3) and GF(4). The simple starter constructs one cyclic square. The search program records its seed, requested and actual iterations, and elapsed generation time.

Sol review should independently replay `human.py`, verify the Sage source pin and hashes, recompute at least one orthogonal-pair count, and run the required valid, damaged, duplicate, invalid-number, false-score, program-error, and timeout cases.

## Local checks

The initial test run before Sol's return had 12 passed and 1 skipped because the task was not in the shared registry. The return fixes remove that registration dependency by testing the runner's process-error and timeout controls directly. Reran `.venv/bin/python -m pytest tasks/t038/test_task.py -q`: 18 passed. Parsed `task.json`, `records.json`, and `sota.json` with `python -m json.tool`. Regression cases compare the full checker result after objective, score, and claimed-score tampering, including NaN values. Independently ran the starter, MacNeish baseline, evolution entry, human replay, and reference entry through the exact checker; their objectives were 1, 2, 2, 5, and 5.
