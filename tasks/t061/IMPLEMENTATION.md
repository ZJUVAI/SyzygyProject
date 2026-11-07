# T061 implementation record

Status: accepted by Sol on 2026-11-06.

## Source check and construction

The fixed parameter is `sat(100,C6)`. Theorem 1.5 of Lan, Shi, Wang, and Zhang gives a lower bound of `4n/3-2` and the construction upper bound `4n/3+epsilon^2/2-5epsilon/6`, where `epsilon=n mod 3`. At `n=100`, these imply the integer interval 132–133. No exact n=100 closure was found in the sources checked on 2026-11-06.

The 133-edge construction uses `t=33`, `epsilon=1`: the nine-vertex core `H` from Figure 1(a), 30 attached 3-vertex paths, and one leaf adjacent to `y4`. The core edge list in `human.py` was decoded from the vector graph in the paper PDF and checked against the path descriptions in the proof. The downloaded source PDF SHA-256 is `ecd1d073b69ab5f120b32c408f6ed5b11874368d571698541c417d4f91ba470e`.

The frozen witness `data/reference/c6_sat_100_133.json` has SHA-256 `39d7689fd56d2f47b4faef733ce8c3a170433ed111fcf0c991feb9e564d28061`. Exact validation found no simple C6 and found simple 5-edge paths for all 4817 nonedges. A simple path has six distinct vertices; the checker rejects a C6 as soon as a five-edge simple path closes on an existing edge.

The public upper-bound construction and its local proof are from [The saturation number of C6](https://doi.org/10.1016/j.disc.2025.114504), Theorem 1.5 and Figure 1, also available as [arXiv:2108.03910v3](https://arxiv.org/html/2108.03910v3). A 2026 paper on graphs saturated for the family `{C4,C5,C6}` has a different forbidden family and does not settle ordinary C6 saturation. The literature check is not exhaustive.

## Reproduction and performance

Tests and JSON checks were run with `.venv` Python 3.13.12:

```sh
.venv/bin/python -m pytest tasks/t061/test_task.py -q
.venv/bin/python -m json.tool tasks/t061/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t061/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t061/records.json > /dev/null
```

The fixed-order initial program returned a valid 198-edge saturated graph in 4.82 seconds; its exact check took 1.72 seconds. The four-trial randomized greedy search completed in 8.94 seconds and returned a valid 221-edge graph. The 133-edge human witness check completed in 0.06 seconds. All are below the shared generation limit of 300 seconds and verification limit of 60 seconds.

The tests cover all five program entries, the C6-free and saturation checks, a six-vertex simple C6, a non-saturated graph, malformed and duplicate undirected edges, loops, out-of-range and bool/float/NaN endpoints, a repeated-vertex walk that must not count as a simple path, score-field invariance, deterministic search, and runner error and timeout handling through `mathbench.evaluate._run` without task registration.

## Limits

The checker certifies feasibility and the edge count. It does not prove a 132-edge example impossible. The instance remains unresolved between 132 and 133 in the checked literature. The randomized greedy search is a weak baseline and does not read reference data. The shared runner uses 4 GiB memory and one thread by default.
