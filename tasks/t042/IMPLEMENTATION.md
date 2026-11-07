# T042 implementation evidence

Status: accepted by Sol on 2026-11-06.

## Definition and source status

- T042-C01 fixes `[1,212]`, maximizes the number of selected integers, and forbids distinct `a < b < c` with `a + c = 2b`.
- The reproduced human-method baseline has 32 elements and uses the ternary-digit formula for Odlyzko and Stanley's 1978 greedy sequence S(1). This is a feasible construction, not an optimum claim.
- The public 43-element set is kept under `data/reference/`, separate from `best/`. Its source says it was found for `[1,211]`; the saved set lies in `[1,211]` and is therefore also a valid witness at `[1,212]`. The raw source witness file hash is recorded and tested.
- The paper v1 leaves the 44-set upper-bound question open. The current linked repository reports DRAT closure of its two historical T1c chunks and partial solver closure of T2. It also says the full T3 cube space remains uncertified. The verified range is still `43 <= r_3(212) <= 44`.
- The current maintained paper discloses Claude Sonnet 4.5, Claude Opus 4.6, and Codex GPT-5 use for writing, code generation/review, experiment planning, repository scaffolding, and computational orchestration. It does not state whether AI proposed or searched for the 43-set. The witness-specific discovery path is recorded as undisclosed. It is not called a human construction.

## Programs and data

- `check.py` validates the fixed configuration, integer types, range, duplicates, and every selected pair that could define an AP midpoint. It recomputes `|A|` and ignores declared scores.
- `init_program.py` is self-contained and returns `{1}`.
- `baseline.py` runs seeded randomized greedy insertion with exact precomputed AP incidence. It uses 48 fixed restarts by default and reads no comparison witness. `MATHBENCH_SEARCH_SECONDS` enables a machine-dependent exploration cutoff.
- `human.py` reconstructs the 32-element Odlyzko-Stanley digit construction.
- `reference.py` reads the pinned public 43-element witness from `data/reference/`.
- `evolution.py` exposes `run_code()` through the task's traditional search baseline. `evaluator.py` provides the shared evaluation adapter.
- `best/T042-C01/` stores the seed-0 baseline output, exact checker result, replay command, environment, budget, and output hash. The run returned 35 elements. No public or human comparison witness is stored there.

## Verification commands and results

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t042/test_task.py -q
.venv/bin/python -m json.tool tasks/t042/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t042/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t042/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t042/best/T042-C01/solution.json > /dev/null
.venv/bin/python -m json.tool tasks/t042/best/T042-C01/result.json > /dev/null
.venv/bin/python -m json.tool tasks/t042/best/T042-C01/provenance.json > /dev/null
```

The task tests passed: 7 tests. They cover the public 43-set and source-file hash, an independent AP scan, the 32-element Odlyzko-Stanley formula and its archived hash, the simple seed, an empty set and endpoint case, forbidden progressions, duplicate input, bool/float/NaN/infinity, range errors, fixed parameters, forged scores, all five `run_code()` entries, seeded search metadata, and shared-runner candidate errors and timeout reporting.

The saved seed-0 result was also replayed through `evaluate_candidate` with strict checking. It returned objective 35, exact status, 2.13 seconds generation, 0.80 seconds verification, Python 3.13.12 on Linux, and the default 300-second/60-second/4-GiB/one-thread policy. The task ID was added only to the local in-process registry tuple for this check; no shared registry file was changed.

The 43-set checker uses integer arithmetic only. For each selected pair `a < b`, it checks whether `2b-a` is selected. This covers every possible nontrivial three-term progression exactly. A separate test scans candidate triples by an independent loop order.

## Limits and review points

- This implementation independently verifies a lower-bound witness. It does not verify the large solver certificate collection or prove the upper bound at N=212.
- The current maintained paper discloses broad AI collaboration, but not whether AI proposed or searched for the 43-set.
- Sol must independently replay all five program entries, check at least one valid and one deliberately broken witness, recompute a key quantity, and confirm a forged score does not change the result before acceptance.
