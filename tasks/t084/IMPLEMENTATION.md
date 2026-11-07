# T084 implementation and validation

Status: **accepted by Sol on 2026-11-06**.

## Mathematical model

`T084-C01` uses 31 distinct integers. It checks the 5,456 multisets of three elements with repetition and minimizes the diameter. All checks and the objective use exact integer arithmetic. There is no integer magnitude cap. Canonical decimal strings support integers beyond Python's default JSON parser digit limit.

The public comparison is the Table 3 `SG, q=31, m=31` witness in Martos Ojeda, Delgado Ordoñez, and Trujillo Solarte (2021), DOI `10.1109/ACCESS.2021.3106617`. Its listed diameter is 19,407. The list was transcribed from the ResearchGate web rendering because the automated IEEE publisher endpoint rejected retrieval; the transcription is not a byte-for-byte PDF copy. Its SHA-256 is `3c24b9ecb40dfa3a75729b6ae5be6a2450f02b36b33276083be570583c4bed39`.

The 2021 paper describes the table as near-optimal and states that exact optimal B3 sets were known through size 7. A literature search on 2026-11-06 for this exact cardinality and record found no later closure. The paper cites Atkinson, Santoro, and Urrutia (1986), DOI `10.1109/TCOM.1986.1096587`, for `G3(m+1) > 10m^3/57`. At `m=30`, this yields diameter at least 4,737. This bound does not establish optimality of the public witness.

## Program separation

- The initial program uses the base-4 no-carry construction.
- The traditional greedy program tests increasing candidates and stops after at most 100,000 candidate checks. It returns the valid base-4 seed if it reaches the cap.
- The evolution program starts only from the greedy construction and makes 1,500 exact-checked mutations. It does not read human or reference data.
- The human and reference programs load the public witness from `data/reference/`.
- The checker ignores all submitted score fields and recomputes all sums and the diameter.

## Reproduction record

The frozen seed-0 evolution output is in `best/seed-0.json`. On Python 3.13.12/Linux, it used the deterministic greedy construction plus 1,500 mutations, accepted 28 valid proposals, and retained diameter 68,302. The record includes seed and shared runner limits. This local search result is weaker than the public comparison.

Run the tests and JSON checks with:

```sh
.venv/bin/python -m pytest tasks/t084/test_task.py -q
.venv/bin/python -m json.tool tasks/t084/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t084/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t084/records.json > /dev/null
git diff --check
```

Validation run on Python 3.13.12/Linux: `.venv/bin/python -m pytest tasks/t084/test_task.py -q` passed all 20 tests in 17.17 seconds. The three JSON files parsed with `python -m json.tool`, and `git diff --check -- tasks/t084` passed. The tests verify the human and reference witnesses, the initial program, greedy and evolution entries, all 5,456 sums, duplicate and collision rejection, exact handling of 5,000-digit translated integers, canonical integer strings, score-claim invariance, and runner error and timeout handling through `mathbench.evaluate._run`.

Known limitation: the local transcription is based on the author's rendered table, not the original PDF bytes. The public value is a feasible upper bound; its optimality is open in the checked sources.
