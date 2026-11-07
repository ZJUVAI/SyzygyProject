# T067 implementation and verification record

## Configuration

- Configuration: `T067-C01`, binary constant-weight code (A(17,4,5)).
- Objective: maximize the number of codewords.
- Human and reproduced reference: 444 codewords.
- Status: `accepted_by_sol`.

## Sources and record status

Milshtein's paper was published online on 2022-10-08 and in *Cryptography and Communications* 15 (2023), pages 443–453. The abstract says the author found a 444-word code by computer search for a maximum independent set. It describes a stochastic local-search algorithm based on Generic Scuba Search. The paper does not report generative-AI use or give a separate AI-provenance statement.

The saved raw file `data/source/milshtein_a17_4_5_444.txt` has SHA-256 `bc5261c3f1b9229985dcd4a95388bf15b42f9d657aa1fa55fd017121d255216a`. The replay witness `data/reference/a17_4_5_444.json` has SHA-256 `e278101d7c5496d890e87330df664e874225020ded21750515954e8b8a42219d`.

The Brouwer table checked on 2026-11-06 lists 444 for (A(17,4,5)) without an optimum marker. Milshtein states an upper bound 474 and cites Östergård (2010). The correction is listed by Springer on 2023-03-01. No matching proof of optimality was found. The implementation records 444 as a reproduced construction and lower bound.

## Programs

- `check.py` checks all input words and all unordered word pairs using exact integer bit counts.
- `init_program.py` returns one valid weight-five word. It is standalone.
- `baseline.py` makes seeded random priority orders over all 6,188 weight-five words and greedily builds a feasible independent set. Defaults use eight restarts; `MATHBENCH_RESTARTS` can set a bounded count.
- `evolution.py` uses seeded block-shuffle mutation and elitist selection over candidate orderings. Defaults use 60 generations and population size six. It imports only generic search code from this task's baseline and does not read comparison files.
- `human.py` reads and replays the archived published construction.
- `reference.py` replays the same fixed witness.
- `evaluator.py` uses the shared evaluation interface.

The search programs do not load `data/source/` or `data/reference/`. The reference programs load only the task-local reference witness. No comparison witness is saved under `best/`.

## Checks performed

The test suite independently checks all 444*443/2 = 98,346 unordered pairs and verifies that the minimum distance is exactly 4. It tests a feasible pair at distance 4, an empty code, one-code initialization, malformed words, incorrect weight, duplicate words, a distance-2 pair, invalid configurations, malformed numeric values, forged score fields, and worker failure and timeout controls.

Run commands:

```sh
.venv/bin/python -m pytest tasks/t067 -q
.venv/bin/python -m json.tool tasks/t067/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t067/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t067/records.json > /dev/null
```

Results:

- `.venv/bin/python -m pytest tasks/t067 -q`: 8 passed in 2.40 seconds.
- JSON parsing for `task.json`, `sota.json`, `records.json`, and `data/source/source_notes.json`: passed.
- Python environment: CPython 3.13.12, Linux x86_64. The runner limits generation to 300 seconds, verification to 60 seconds, memory to 4 GiB, and one thread.
- Default traditional search replay with `MATHBENCH_CONFIG_ID=T067-C01`, seed 0, no time cutoff: 8/8 restarts, 0.476 seconds, exact checker score 308.
- Default evolutionary search replay with `MATHBENCH_CONFIG_ID=T067-C01`, seed 0, no time cutoff: 60/60 generations, population 6, 3.895 seconds, exact checker score 312.
- Replay commands: `.venv/bin/python -m tasks.t067.human` and `.venv/bin/python -m tasks.t067.reference`; each prints the 444-word witness.

Search uses fixed counts and the seed from `MATHBENCH_SEED` unless `MATHBENCH_SEARCH_SECONDS` is explicitly set. The lower 308/312 search results are task-local baseline results; they do not replace the frozen 444 human/reference construction.
