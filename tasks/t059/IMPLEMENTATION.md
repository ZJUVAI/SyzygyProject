# T059 implementation record

## Configuration and objective

`T059-C01` fixes the simple undirected DIMACS graph C2000.9 with 2,000 vertices indexed from 0 and 1,799,532 edges. The task maximizes the cardinality of a set of distinct vertices that are pairwise adjacent.

The candidate is a list of vertex indices. The exact checker rejects a non-list, non-integer indices (including Boolean and floating-point values), out-of-range vertices, and duplicates. It loads the pinned source graph, builds one integer bitset per vertex, and checks every pair in the candidate. The score is the candidate list length. Optional claimed score fields do not affect validation.

The empty clique is accepted with objective zero. A one-vertex clique is accepted with objective one. The initial program returns vertex zero and does not import task modules.

## Instance and source pins

The input source was provided from the CMU COLOR04/DIMACS C2000.9 benchmark snapshot. It contains the DIMACS header `p col 2000 1799532`. The original file is 19,602,828 bytes. The local input is compressed at `data/source/C2000.9.clq.gz` (4.1 MiB). On load, the checker streams its uncompressed bytes, verifies SHA-256 `aa4b1d7df7f9c1afbf8c9f35fcf5bdfc6370fd27db5c9f3fd5409dfd0d164f16`, checks the header and edge count, rejects self-loops or duplicate edges, and builds adjacency bitsets. The compressed file SHA-256 is `936ec5806f6e58fbe1f28a87f018cd064dece5eae8ab29013040d47857fd1639`.

The human witness is `data/reference/human_2005_clique80.json`, SHA-256 `02eecb1280588703bd1a57b55e10c4ce46e0f5672e87c8962182dca7f472ce1c`. The source paper PDF is saved under `data/source/grosso_locatelli_pullan_2005.pdf`, SHA-256 `cc3897591e2aeadd21303d8fc1ac135923376c17e611a7257b8c6bf0ef92cc72`.

## Public lower and upper results

Grosso, Locatelli, and Pullan's 2005 short communication reports a 79-vertex clique and then says a longer run found an 80-vertex clique. The paper supplies the complete 80-vertex list, with zero-based labels. The list is saved locally. The checker verified all 3,160 pairs. This gives a public feasible lower bound of 80.

Krpan and Povh's 2026 paper, arXiv:2607.11726v1 (submitted 2026-07-13), reports an integer upper bound of 168 for C2000.9. It improves an earlier 177. The method tests `k=169` with core reduction and the Lovász theta upper-bound function. The authors state that the reduction certifies `omega(G)<169`. The run took 17 days, 18 hours, and 8 minutes on a node with 192 logical threads and 751 GiB of RAM. The paper and code state that C2000.9's exact value is unknown.

This task records 168 as an author-reported upper-bound result. It has not independently run MOSEK or replayed the authors' long computation. The saved local checker certifies feasible cliques only; it does not claim to validate the 168 upper bound. The paper's code repository was checked on 2026-11-06 and pinned to commit `79d3fe7dcfb09237042ad5059a4f1352838e3ba2`. No newer same-instance exact closure was found in the sources checked by that date.

The public human source does not state whether AI tools were used. No AI-free claim is made. The 2026 upper-bound source also does not state whether AI tools were used.

## Programs and fixed seed results

| Entry | Method | Seed 0 clique size | Work |
| --- | --- | ---: | ---: |
| `init_program.py` | Single vertex `[0]` | 1 | direct construction |
| `baseline.py` | Static-degree greedy starts and one-for-two improvement | 62 | 16 candidates |
| `human.py` | Replay the paper's 80-vertex human witness | 80 | direct replay |
| `reference.py` | Replay the saved public witness | 80 | direct replay |
| `evolution.py` | Dynamic-degree greedy restarts and repeated one-for-two improvement | 71 | 256 candidates; 4 best improvements |

The baseline and evolution programs use the public graph only. They do not read `human.py`, `reference.py`, or `data/reference/`. The saved own-search construction is `best/seed_0.json`; it includes its seed, candidate count, exact verification result, environment, budget and replay command.

Replay the saved search witness with:

```sh
MATHBENCH_CONFIG_ID=T059-C01 MATHBENCH_SEED=0 .venv/bin/python -c 'from tasks.t059.evolution import run_code; import json; print(json.dumps(run_code()))'
```

Search defaults are fixed at 16 candidate cliques for `baseline.py` and 256 for `evolution.py`. The runner limits generation to 300 seconds, verification to 60 seconds, memory to 4 GiB, and numerical threads to one.

## Validation

Command:

```sh
.venv/bin/python -m pytest tasks/t059/test_task.py -q
```

Result on 2026-11-06: `22 passed in 22.63s`.

The tests check the complete human witness with an independent edge-set parser, the compressed source hash and graph dimensions, empty and singleton boundaries, invalid indices/types/duplicates, a deliberately selected nonedge, claimed-score invariance, all five `run_code()` entries, search isolation, and worker error and timeout behavior through `mathbench.evaluate._run` without task registry admission.

Sol review remains pending.
