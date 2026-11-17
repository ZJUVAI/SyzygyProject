# T053 implementation notes

## Configuration

T053 has one official configuration: T053-C01, C(24,14,4). Its frozen human reference is the reproduced 62-block construction described below. The best reproduced public witness has 23 blocks. Its optimality is unknown.

## Programs

`check.py` reads v, k, and t from the selected configuration, rejects malformed or duplicate blocks, and recomputes the exact block count and coverage. It does not use the candidate's declared objective. `init_program.py` provides a deterministic complete-cover start.

`baseline.py` uses greedy set cover over 500 seeded random k-subsets plus the valid initial cover. `human.py`, `sota.py`, and `reference.py` provide the human construction, public witness, and fixed local-search result. `evolution.py` uses its specialized C01 search kernel.

## Limits and replay

Generation budget: 300 seconds. Verification budget: 60 seconds. Memory: 4 GiB. Threads: one.
