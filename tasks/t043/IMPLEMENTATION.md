# T043 implementation record

Status: **accepted by Sol on 2026-11-06**. This task has not been admitted to the shared registry.

## Fixed model

Configuration `T043-C01` fixes `q=2`, ambient dimension 7, subspace dimension 3, and minimum subspace distance 4. The objective is to maximize the number of codewords. For two 3-spaces, distance at least 4 is equivalent to intersection dimension at most 1. The checker takes a list of three 7-bit row masks or a 3 by 7 binary basis matrix for each codeword. It checks rank, canonical span identity, and every pair by exact enumeration over `GF(2)`. It ignores claimed objective fields and returns a fixed `claimed_objective_ignored` detail.

An independent upper bound follows by counting 2-spaces. The Gaussian binomial coefficient is `[7 choose 2]_2 = (127*126)/(3*2) = 2667`, and `[3 choose 2]_2 = 7`. A valid code cannot repeat a 2-space, so its size is at most `floor(2667/7) = 381`. The 2025 Kurz survey gives a stronger conditional result: `A₂(7,4;3) ≤ 378` or `A₂(7,4;3) = 381`. The value 378 is not an unconditional upper bound.

## Human construction and public status

The primary witness is from Heinlein, Kiermaier, Kurz, and Wassermann, “A subspace code of size 333 in the setting of a binary q-analog of the Fano plane,” *Advances in Mathematics of Communications* 13(3) (2019), DOI [10.3934/amc.2019029](https://doi.org/10.3934/amc.2019029). The checked preprint is arXiv v5, dated 2019-03-22. Its first arXiv version is dated 2017-08-21. The paper reports an integer-linear-programming search and prints the orbit representatives and the two generators of `G_{4,6}`. The source does not report AI use, so the records do not claim an unaided hand construction.

The source TeX provided for the research pass has SHA-256 `26622afb1178db82948f215c7befe73172f8c30338f0632d1ae0786d487f2eb7`. Its Appendix B matrices and Appendix C representatives are extracted into [heinlein_2019_appendix_c.json](data/source/heinlein_2019_appendix_c.json), whose SHA-256 is `5bcf86a99365ad8eb9971dd6a8a825fd8fb59747d06238d73d779a5e7cd775a1`. The paper encodes a column as `a + 2b + 4c`; the implementation decodes these digits into a 3 by 7 binary matrix, closes each representative under `G_{4,6}`, and confirms the orbit sizes `1^9 2^26 4^68`. It reconstructs 333 distinct spaces. The exact checker then checks all 55,278 pairs. This verifies the lower bound and its score. It does not prove optimality.

For a current source check, the MIPLIB instance page [cdc7-4-3-2](https://miplib.zib.de/instance_details_cdc7-4-3-2.html) states `333 ≤ A₂(7,4;3) ≤ 381` and lists the 333 construction. The Kurz survey [Constructions and bounds for subspace codes](https://doi.org/10.15495/EPub_UBT_00008787) states the conditional 378-or-381 bound and describes this as an open case. No later exact value or 381-code proof was located in these checked sources as of 2026-11-06. This source check is not exhaustive. A direct request to the specialist tables site failed during this check, so the status statement does not treat that page as independently verified.

## Programs and saved search result

- `init_program.py` returns the coordinate 3-space and does not import task modules or comparison data.
- `baseline.py` enumerates all 11,811 3-spaces and runs a seeded randomized greedy packing against their 2-space supports. It records requested and actual pass counts and supports `MATHBENCH_SEARCH_SECONDS` through `mathbench.search.search_steps`.
- `evolution.py` runs independent seeded greedy restarts. It does not read the human witness.
- `human.py` replays the printed representatives and group action. `reference.py` exposes the fixed replay through `run_code()`.
- `best/randomized_greedy_seed0.json` stores a valid local-search result of size 230, its exact checker result, seed 0, 12 completed greedy passes, and the replay command. This direct local run used Python 3.13.12 on Linux. The process resource limits in the saved run record describe the benchmark defaults; the direct shell replay did not enforce them.

The saved search result is a task-generated result. The published 333 witness remains under `data/source/` and is not loaded by the initial program or search programs.

## Validation and pending review

Commands run:

```sh
.venv/bin/python -m pytest tasks/t043/test_task.py -q
.venv/bin/python -m json.tool tasks/t043/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t043/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t043/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t043/acceptance.json > /dev/null
.venv/bin/python -m json.tool tasks/t043/data/source/heinlein_2019_appendix_c.json > /dev/null
.venv/bin/python -m json.tool tasks/t043/best/randomized_greedy_seed0.json > /dev/null
```

The test command passed: **5 passed**. It covers the 333 witness and all 55,278 pairs, an invalid rank, a distance violation, equivalent bases for the same subspace, a Boolean matrix entry, empty code, objective/score/claimed-score invariance, source hash, orbit counts, every `run_code()` entry, and worker error and timeout controls through `mathbench.evaluate._run`.

The checker was also run directly on the initial seed (objective 1), the traditional search result (230), and the reconstructed published witness/reference (333). The local test executes the evolution entry with one requested restart and verifies its result. Full `evaluate_candidate("T043", ...)` is deferred until Sol admits the task to the shared registry; the expected missing-ID behavior is not a task failure. There are no known mathematical or reconstruction gaps. Sol review remains required for independent replay, source review, the upper-bound derivation, and acceptance status.
