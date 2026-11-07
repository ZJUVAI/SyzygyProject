# T056 implementation record

## Configuration and problem definition

`T056-C01` is Taillard's job-shop instance `ta41`, with 30 jobs and 20 machines. This task uses the first 30-by-20 block in the official `tai30_20.txt` file. Each job has its own route through all 20 machines. The route order and processing times are fixed. Each machine has its own chosen job order. The objective is the exact integer makespan and is minimized.

This is general job-shop scheduling. It is not a permutation flow-shop: jobs do not share one common machine order, and each job may use a different machine route.

The candidate contains 20 machine rows. Each row is a permutation of jobs `0..29`. For each operation, the checker adds the preceding operation in the same job and the preceding job on the same machine as graph predecessors. If the resulting graph is acyclic, an exact topological longest-path calculation gives the earliest start and finish times. Its maximum completion time is the objective. If the graph has a cycle, the candidate is infeasible. All operations and edge weights are integers, so this check is exact.

## Current bounds and open status

The official Taillard source page groups job-shop files by size. It lists `ta41` through `ta50` as 30 jobs by 20 machines. The 50-by-20 instances are `ta61` through `ta70`; the official ta61 file has equal bound fields 2868 and is not selected here.

The current Taillard bounds page, last updated 2026-10-18, lists `ta41` with lower bound 1912 and upper bound 2006. The upper-bound schedule is attributed to Shylo and Pardalos (2008) and is downloadable from the same page. Its exact machine orders are saved locally and rechecked by this task. No later same-instance closure was found in the sources checked on 2026-11-06.

Coupvent des Graviers et al. (2025), arXiv:2504.16106, report a CP-SAT `OPT-50000s` numerical lower bound of 1915 for ta41. The paper defines `OPT` as the best lower bound found while minimizing makespan. It also states that it does not formally prove solver-derived lower bounds because implementation errors cannot be excluded. We therefore report 1915 separately as a solver-derived numerical result; the task's conservative current public bound entry remains 1912. Neither value closes the gap to the feasible schedule at 2006. The exact optimum remains open.

The `tai30_20.txt` first-block header has historical bounds 1850 and 2064. These are not used as current bounds. The input itself is retained byte-for-byte and normalized to `data/source/ta41_instance.json` for program use.

## Public witness and human baseline

The frozen weak human baseline is 3296. `human.py` implements the active-schedule generation procedure of Giffler and Thompson (1960), then selects the longest-processing-time operation from each conflict set. The resulting machine orders are deterministic for a fixed seed and are checked by the exact checker. This is a reproduced traditional dispatching construction, not a claim to reproduce the paper's best schedule or the 2006 benchmark record.

The public schedule is Shylo and Pardalos's 2008 makespan-2006 result. Its published machine orders were downloaded from `optimizizer.com`, normalized to `data/reference/ta41_2006_schedule.json`, and independently recomputed. The full HTML capture and official instance snapshot are under `data/source/`.

AI use is not stated by the cited GES source. No claim is made that the historic record is AI-free. The reconstructed GT baseline is our local traditional-method implementation.

## Programs and default seed results

| Entry | Method | Seed 0 makespan | Work |
| --- | --- | ---: | ---: |
| `init_program.py` | Every machine orders jobs by index | 25114 | direct construction |
| `baseline.py` | 32 seeded random choices inside GT conflict sets, retaining the best | 2795 | 32 schedules |
| `human.py` | GT active schedule generation with longest processing time in the conflict set | 3296 | one deterministic schedule |
| `reference.py` | Replay downloaded public machine orders | 2006 | direct replay |
| `evolution.py` | 375 randomized GT restarts and 125 adjacent-swap trials with exact cycle checks | 2795 | 500 iterations; 497 feasible candidates; 2 improvements over its initial schedule |

The saved own-search witness is `best/seed_0.json`. It stores the 20 machine orders, recomputed makespan, seed, environment, generation budget, and replay command. The evolution search reads the simple initial program and instance data. Neither it nor the baseline reads `human.py`, `reference.py`, or `data/reference/`.

Replay the saved search construction with:

```sh
MATHBENCH_CONFIG_ID=T056-C01 MATHBENCH_SEED=0 .venv/bin/python -c 'from tasks.t056.evolution import run_code; import json; print(json.dumps(run_code()))'
```

The runner limits candidate generation to 300 seconds, verification to 60 seconds, memory to 4 GiB, and numerical threads to one. The fixed search defaults are 32 candidates for `baseline.py` and 500 iterations for `evolution.py`. Both programs always use fixed iteration counts; the shared runner applies the generation timeout.

## Source snapshots

- Official Taillard `tai30_20.txt`, URL `https://mistic.iict-heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/jobshop.dir/tai30_20.txt`, SHA-256 `fa6631f4411187bb1b43e4c444293227852860fa56f3ea6e14f48a294adbd3b9`.
- Normalized ta41 instance, SHA-256 `1857bd6845eca1147b5593e2011ae4c5da24ff8749d26f603fbf909a68087ce6`.
- Downloaded public schedule HTML, URL `https://www.optimizizer.com/solution.php?UB=2006&name=ta41&problemclass=ta`, SHA-256 `f3e941ea8f70aae2110892f86f3bd034f757578270d97feca37041725db870f8`.
- Normalized public schedule, SHA-256 `d3760f7a46266d9da02920433f027645056704d76fb423846414ca9d275c58ed`.

## Validation

Run:

```sh
.venv/bin/python -m pytest tasks/t056/test_task.py -q
```

Result on 2026-11-06: `21 passed in 0.96s`.

The test suite checks the published schedule, an independently written earliest-time calculation, the simple initial schedule, source hashes and input shape, malformed job orders, an explicit cycle, invariance to claimed-score fields, all five `run_code()` entries, search isolation, and worker error and timeout handling through `mathbench.evaluate._run` without task registry admission.

Sol review remains pending.
