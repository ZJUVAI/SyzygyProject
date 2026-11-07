# T090 implementation record

Status: `accepted_by_sol`.

## Definition and source review

- Configuration: `T090-C01`, length 64, entries in `{−1,+1}`, periodic boundary, minimize the sum of squared correlations for shifts 1 through 63.
- Tyler and Loftsson's NASA Table 2 supplies the sequence `B24FEAE7E4529CF0`; footnote ZZ cites J. Watkins, personal communication, June 1985. The source report copy has SHA-256 `edc332b8a9410cb0d8f14d6db65225469f592c5096c88fa3e8051315282d63cf`. Exact decoding gives energy 240 and PSL 4. The earlier metadata had the wrong title, authors, year, and NTRS record; these fields and asset filenames are corrected.
- Mertens and Bessenrodt §4.2 Table 4 gives `ΔE=14` at N=64, which is E=224 under their `ΔE=E/16` definition. The row comes from numerical search and marks ground-state status `?`; it does not claim a proof. The sequence was not recovered.
- Their table states exhaustive search for the N=4t periodic case only through N≤40. Source checks on 2026-11-06 found no later proof closing periodic N=64. Aperiodic results at N=64 are distinct and do not change this task's objective.

## Programs and stored results

- `init_program.py` returns the all-`+1` sequence, with energy 258048.
- `baseline.py` uses four seeded random restarts, each with 5000 single-spin annealing proposals and exact integer correlation deltas. It reads no comparison sequence.
- `evolution.py` is the task-qualified search entry.
- `human.py` reconstructs the NASA report's hex sequence. `reference.py` loads its separately frozen witness in `data/reference/`.
- The saved seed-0 baseline in `best/seed-0.json` has exact energy 608 and PSL 8. The default run took 4.312 seconds locally.

## Checker and validation

- The checker validates all 64 entries as exact integers in `{−1,+1}` and directly recomputes all 63 periodic correlation sums, energy, and PSL using integer arithmetic.
- Candidate score claims do not affect validation.
- Command: `.venv/bin/python -m pytest tasks/t090/test_task.py -q`
- Result: `12 passed in 4.92s`.
- Tests cover all five program entries, exact human reconstruction, exact flip-delta updates versus full recomputation, invalid length and values, NaN/infinity, fixed configuration, claim invariance, deterministic search, and `_run` errors and timeouts.
- All JSON files were parsed with `python -m json.tool`; `git diff --check -- tasks/t090` passed.
- Shared limits remain 300 seconds for generation, 60 seconds for verification, 4 GiB, and one thread.

## Limits

Energy 224 is a reported numerical low-energy result, not a proved minimum. The exact minimum periodic energy at length 64 remains unresolved in the sources checked. The reproducible human baseline is 240.
