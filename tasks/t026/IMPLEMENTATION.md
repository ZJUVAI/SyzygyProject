# T026 implementation record

Status: **accepted by Sol on 2026-11-06**.

## Reproduced constructions

- `human.py` rebuilds Fredricksen and Sweet's same-parameter 536 coloring from the six representative lists in `data/fredricksen_sweet_536_halfsets.json`. The task checker confirms every number from 1 to 536 appears once and checks the ordinary Schur condition, including equal addends. Recomputed objective: 536.
- `reference.py` decodes the 537-color certificate at the pinned GitHub commit in `source_hashes.json`. The downloaded certificate digest matches the upstream `SHA256SUMS`; the task checker recomputes objective 537.
- The 537 paper says the partitions were found by search. It does not report whether AI or LLM tools were used. The record leaves this provenance undisclosed.
- The source does not prove `S(6)=537` or that 538 cannot be colored. The task objective is a feasible lower bound only.

## Programs and search record

- `init_program.py` returns the simple valid coloring `[0,1,1,0]` of `[1,4]`. It does not read task data.
- `baseline.py` uses sequential greedy placement, randomized choices, six labels, and random restarts. It reads no human or public witness. Seed 0 used 50,000 attempted placements across 820 restarts and returned a valid coloring of length 104. The replay metadata is in `data/baseline_replay.json`.
- `human.py` and `reference.py` are fixed external comparisons. They are not used by either starting or search program.

## Verification run

Command:

```sh
.venv/bin/python -m pytest tasks/t026/test_task.py -q
```

Result: 20 passed in 2.76 seconds. The test suite checks the initial coloring, human and public witnesses, exact score recomputation, ignored score claims, equal and unequal addends, malformed partitions, duplicate members, a missing prefix element, boolean and non-integer values, NaN, infinity, reproducible search metadata, zero-second search budget, the `evolution.py` entry point, pinned upstream and transcription hashes, candidate program errors, and generation timeout handling.

Independent recorded calculations used a separate nested loop over all pairs `x<=y` and checked `x+y<=N` before comparing colors. It found no violations for the human partition (N=536; 143,916 pairs), the pinned public certificate (N=537; 144,453 pairs), or the seeded traditional baseline (N=104; 5,460 pairs). The respective recomputed objectives are 536, 537, and 104. The task checker separately recomputes each value from its color array.

## Remaining review work

Sol must independently compare the 536 transcription with the source paper, replay both external constructions, inspect the cold-start program and traditional search, and verify that claimed scores do not affect recomputation. No mathematical optimality claim is made.
