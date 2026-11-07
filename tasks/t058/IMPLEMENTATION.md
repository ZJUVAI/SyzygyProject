# T058 implementation record

Status: accepted by Sol on 2026-11-06.

## Sources and current status

The 2026 Miller–Valkov–Abel supplementary Table 4 lists 35 players, group size 5, a bound of 8, and a 7-round `RTD(5,7)` construction. The paper defines “optimal” as best currently known and “maximal” as attaining the upper bound. Checked on 2026-11-06, the OEIS A107431 entry currently says `T(7,5)` is either 7 or 8. The entry revision history was not checked. The checked sources therefore leave the maximum unresolved. The fixed reference is a 7-round lower-bound construction.

Reference witness: `data/reference/rtd_5_7.json`, SHA-256 `f950b70f2ed05281c6fbde7c6cf0a58214b19a8517671108e278e8ab20e6e773`. It is rebuilt by the finite-field formula in `human.py`. Exact validation checks 35 distinct players in every group partition and all 490 distinct pairs across the seven rounds.

## Reproduction

Commands run with repository `.venv` Python 3.13.12:

```sh
.venv/bin/python -m pytest tasks/t058/test_task.py -q
.venv/bin/python -m json.tool tasks/t058/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t058/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t058/records.json > /dev/null
```

The default randomized greedy baseline used seed 0, eight restarts, and 5000 random partitions per attempted added round. It checked 40008 partitions in 0.84 seconds and retained its valid one-round starting schedule. The run result, construction, and exact validation are saved under `best/T058-C01/`. This search baseline is weaker than the published 7-round construction. It reads no reference data.

Tests cover the five program entries, the one-round simple construction, the human and fixed reference constructions, exact pair counting, invalid group counts, duplicate/missing/out-of-range/bool/float/NaN IDs, repeated pairs, the eight-round counting bound, forged score fields, deterministic search, and runner error and timeout behavior through `mathbench.evaluate._run` without task registration.

## Limits and uncertainty

The upper bound 8 follows because each player has 34 possible partners and meets four new players in each round. No proof of an 8-round construction or of impossibility was found in the cited current sources. The task remains open on the checked evidence. The sources reviewed were the 2026 paper and supplement, the current OEIS A107431 entry checked on 2026-11-06 (without checking its revision history), and the 2021 paper for the excluded four-person-group parameters. The literature check is not exhaustive.

The shared runner uses its default generation limit of 300 seconds, verification limit of 60 seconds, 4 GiB memory, and one thread. The task adds no shared registry entry. Its comparison witness is kept under `data/reference/`.
