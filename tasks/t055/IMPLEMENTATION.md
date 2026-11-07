# T055 implementation evidence

Status: accepted by Sol on 2026-11-06.

## Definition and fixed instance

- `T055-C01` is partial MaxSAT: assign 1630 Boolean variables, satisfy all 6150 hard clauses, and maximize the weight of satisfied soft clauses. The 649 soft clauses all have unit weight, so the objective ranges from 0 to 649.
- The selected normalized WCNF has SHA-256 `cd81f483b6cc3d05e9760274eee7697d9cc0f0a5a7146d3c6887af687d149195`. `maxsat.py` checks the hash before parsing. The parser verifies exactly 6150 `h` clauses and 649 weighted soft clauses, then checks every literal is in `[-1630,1630] \ {0}`.
- The benchmark is `b4794d123e18a908924d3d33cdeeae3b`, family `inconsistency-measurement`, submitted in 2023, submitter unknown. The complete MSE 2026 benchmark collection is Zenodo record 21283148 (version 2026, published 2026-07-09). The official evaluation dataset is Zenodo record 21358014, v1, published 2026-07-14.

## Public result and human baseline

- The MSE 2026 metadata gives best-known unsatisfied soft cost 62 and optimum cost unknown. This maps to task score `649 - 62 = 587`; no optimality proof is given.
- The official `ANYTIME-UW` 60-second BouMS log for this instance is indexed at `outputs/ANYTIME-UW/60/BouMS/b4794d123e18a908924d3d33cdeeae3b.wcnf.o`, offset `813824899`, CRC32 `10873941`. Its paired completion member has CRC32 `2569026316` and says `62 VERIFIED`. The archive index was available without downloading the full 1.8 GB `logs.zip`.
- The extracted official assignment is saved as `data/reference/mse2026_boums_60_assignment.json`, SHA-256 `c129d0fded17b46dca93fe9a4c3c2273926c346c78578bfec2e922023a746543`. Exact validation confirms 1630 values, all 6150 hard clauses satisfied, soft score 587, and unsatisfied soft weight 62.
- The public MSE record does not state whether AI contributed to BouMS or this run. The AI provenance is unknown; the solver result is not labelled human-only.
- The frozen human-method baseline is 360. `human.py` runs the traditional DPLL procedure on the hard clauses and then exact feasible single-variable soft hill climbing. The method follows Davis, Logemann, and Loveland (1962), *A Machine Program for Theorem-Proving*, DOI `10.1145/368273.368557`, using SymPy 1.14.0's DPLL2 implementation. The score 360 is recomputed from this instance and is not a public competition score. A separate research seed file was not used; `human.py` and `init_program.py` regenerate the hard-SAT assignment from the fixed formula.
- The replayed DPLL baseline is saved at `data/reference/human_dpll_assignment.json`, SHA-256 `da78d29bc9625dd3f6fcae85ea8e990c66c02fb95243a9f4aa61d8e9f11e216f`. It satisfies all hard clauses and has soft unsatisfied cost 289.

## Programs and search result

- `init_program.py` is standalone and reads only the public WCNF. It runs DPLL on the hard clauses and returns a feasible assignment. It imports no task module.
- `baseline.py` uses a fixed-seed random block-flip search. It keeps candidates only when every hard clause remains satisfied.
- `evolution.py` uses a bounded population and block mutations. It checks hard feasibility exactly before accepting candidates.
- `human.py` rebuilds the DPLL hard-SAT solution and applies feasible single-variable soft improvements.
- `reference.py` replays the saved official BouMS assignment. No search entry reads the reference assignment.
- A saved task-local search used Python 3.13.12, SymPy 1.14.0, Linux x86_64, seed 2026, and 32 generations. It ran 32 mutations, found no hard-feasible mutant, and kept the valid DPLL seed at score 360 / cost 289. Generation took 0.2039 seconds. The exact output, validation result, environment, and replay command are saved in `best/T055-C01/evolution_seed2026.json`.
- Replay command:

  ```sh
  MATHBENCH_CONFIG_ID=T055-C01 MATHBENCH_SEED=2026 MATHBENCH_SEARCH_ITERATIONS=32 .venv/bin/python -m tasks.t055.evolution
  ```

- Default limits are generation 300 seconds, verification 60 seconds, memory 4 GiB, and one compute thread. Search uses fixed iterations unless `MATHBENCH_SEARCH_SECONDS` is set.

## Validation performed

From the repository root:

```sh
.venv/bin/python -m pytest tasks/t055/test_task.py -q
.venv/bin/python -m json.tool tasks/t055/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t055/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t055/records.json > /dev/null
```

The task-local suite passed: `5 passed in 3.30s` on the final run. It checks the WCNF hash and clause counts, independently re-counts the 587 public score, checks the 360 DPLL baseline, rejects malformed assignments and an all-false hard-violating assignment, confirms claimed-score fields do not change the result, runs all five program entries, and tests worker errors and timeouts through `mathbench.evaluate._run`. All four task JSON files passed `python -m json.tool`.

## Review limits

- The instance metadata says `optimal_cost=unknown`; score 587 is a verified lower bound, not an optimality proof.
- The official competition release does not disclose the AI provenance of the BouMS solver or this run.
- The DPLL baseline is deliberately weaker than the public competition assignment. It is a reproducible traditional method baseline, not a claim about best human performance.
