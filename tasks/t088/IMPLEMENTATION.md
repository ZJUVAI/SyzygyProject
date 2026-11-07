# T088 implementation record

Status: `accepted_by_sol`.

## Fixed instance

- Configuration: `T088-C01`, graph `arc130.mtx.rnd`, 130 vertices and 715 edges.
- Input: `data/source/arc130.mtx.rnd`, copied from the Optsicom instance archive. SHA-256: `be272e3c2b11280c2c8335ae966c3d14ecef94fb4cb8fc2b049ecd7d676734a8`.
- The input parser independently checks the header, edge count, endpoint range, loops, and duplicate undirected edges. Observed maximum degree is 124.
- Current source review checked the Optsicom page and Martí et al. (2013), Appendix Table 9, on 2026-11-06. The report gives lower bound 62 and upper bound 202. The reported 202 ordering was not recovered. No proof closing the instance was found in the checked sources; this is not an exhaustive literature survey.

## Programs and results

- `init_program.py` returns natural vertex order.
- `baseline.py` and `evolution.py` run bounded seeded GRASP-style construction with insertion moves. They only read the public graph. The default is six trials and twelve shuffled vertices per local pass. The optional time cutoff is explicit.
- `human.py` reconstructs the cited GRASP method family with three trials and eight shuffled vertices per local pass. It produces a fixed exact score of 229; it does not claim to reproduce the reported 202 ordering.
- `reference.py` loads the frozen local reconstruction from `data/reference/`; it does not load a file from `best/`.
- The run saved at `best/seed-0.json` scored 221 after six trials. Its metadata records seed, runtime, settings, and exact checker output.
- `check.py` validates the full permutation and computes all 129 prefix cut sizes with exact integer difference-array arithmetic. It ignores optional candidate score fields.

## Validation

- Command: `.venv/bin/python -m pytest tasks/t088/test_task.py -q`
- Result: `11 passed in 8.16s`.
- Tests cover all five entries, exact independent cut counts, graph file hash and edge count, invalid permutations and labels, complete configuration matching, score-claim invariance, repeatable seeded search, and runner error/timeout behavior through `mathbench.evaluate._run`.
- JSON files were checked with `python -m json.tool`; whitespace was checked with `git diff --check`.
- Resource defaults remain 300 seconds for generation, 60 seconds for verification, 4 GiB, and one thread. The saved six-trial baseline took 7.327 seconds in the local Python 3.13 environment.

## Limits

The source's 62–202 gap is retained as reported evidence. The current local search scores are feasible upper bounds only. Neither the literature result nor the local runs prove optimality.
