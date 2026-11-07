# T045 implementation record

Status: **accepted by Sol on 2026-11-06**. The task has not been admitted to the shared registry.

## Model and fixed graph

Configuration `T045-C01` fixes the unweighted undirected graph `gd96a`: 1,096 vertices and 1,676 edges. A solution lists each vertex ID from 1 through 1,096 once. The objective is to minimize the integer sum of `abs(position[u] - position[v])` over every edge.

The graph comes from Jordi Petit’s MinLA experiment archive at [the official experiments page](https://www.cs.upc.edu/~jpetit/MinLA/Experiments/). The downloaded archive URL is `https://www.cs.upc.edu/~jpetit/MinLA/Experiments/jpetit-extra.tar.gz`. Its path is `CodeJEA/Graphs/gd96a.rmf`. The archive SHA-256 was `69f2b258f866122ed1cd8517ad41c5866940db1a3642db0e1b4e1315715d7621`. The task stores the exact unweighted edge list as [gd96a.rmf](data/source/gd96a.rmf), SHA-256 `a3f6f97b8c084f41b6312a02544d71b293bfb8e809f627e4c5e7a04495061f4c`. The checker reads the pinned file and rejects a header, edge count, weight, endpoint, loop, or duplicate-edge mismatch.

The initial program returns the identity permutation. The traditional search baseline uses randomized reverse-Cuthill–McKee traversals and adjacent-swap descent. The evolution program starts from that graph-only search method and uses a seeded simulated-annealing run with vertex swaps. Neither search entry reads the human or reference ordering.

## Human-method baseline and open record

The public MinLA experiment tables and the primary 2011 paper were checked on 2026-11-06. Caprara, Letchford, and Salazar-González, “Decorous Lower Bounds for Minimum Linear Arrangement,” *INFORMS Journal on Computing* 23(1) (2011), [DOI 10.1287/ijoc.1100.0390](https://doi.org/10.1287/ijoc.1100.0390), report a best heuristic cost of 95,242 for `gd96a` in Table 1 and attribute it to Rodriguez-Tello et al. (2008). Table 1 lists the earlier 5,155 lower bound. Table 2 gives the stronger LP lower bound of 77,860 and an 18.3% gap. The original 95,242 ordering was not present in the checked archive or located in the checked sources. It remains a reported result with AI provenance not stated by its source.

The latest source check included the current [Petit upper-bound table](https://www.cs.upc.edu/~jpetit/MinLA/Experiments/upperbounds.html), the [lower-bound table](https://www.cs.upc.edu/~jpetit/MinLA/Experiments/lowerbounds.html), and the 2026 paper [Small boundary: a family of linear-time greedy heuristics for the minimum linear arrangement problem](https://doi.org/10.1007/s10732-026-09604-6). The current upper-bound table lists 96,342 as its best simulated-annealing value and 170,903 as its spectral value for this graph; neither improves on 95,242. The 2026 paper studies another set of 26 large real-world graphs and does not include `gd96a`. No exact optimum or newer same-parameter result was located in these sources. The check is bounded; it does not prove that no later result exists.

The fixed human-method reference is a task-local reproduction of spectral sequencing followed by adjacent-swap descent. The source archive’s `spectral` method uses a Fiedler-vector ordering. This implementation uses SciPy’s sparse Laplacian eigensolver with fixed seed 0, then accepts only adjacent swaps that lower the exact MinLA objective. It stops when a sweep finds no improvement, up to 200 sweeps. The resulting ordering has cost **147,653** after 124 sweeps. This is an AI-assisted implementation of a traditional method. The score is not attributed to the source paper, and it is weaker than the reported 95,242 result. The saved ordering is [spectral_adjacent_ordering.json](data/reference/spectral_adjacent_ordering.json); `reference.py` replays it.

## Saved search result and verification

`best/seeded_rcm_adjacent_seed0.json` stores a separate search result with cost **280,285**, seed 0, eight requested and completed starts, and at most 12 adjacent-swap sweeps per start. It includes the exact checker result, local Python/platform details, budget fields, and replay command. The direct local replay did not enforce MathBench process resource limits; official runner defaults remain 300 seconds for generation, 60 seconds for checking, 4 GiB, and one thread.

Commands run:

```sh
.venv/bin/python -m pytest tasks/t045/test_task.py -q
.venv/bin/python -m json.tool tasks/t045/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t045/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t045/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t045/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t045/data/reference/spectral_adjacent_ordering.json > /dev/null
.venv/bin/python -m json.tool tasks/t045/best/seeded_rcm_adjacent_seed0.json > /dev/null
```

The task test command passed: **4 passed**. Tests cover the exact graph hash and counts, the 1,096-element legal reference, an independently recomputed 1,676-edge score, short and empty orderings, duplicate vertices, Boolean, NaN, and out-of-range values, claimed-score invariance, all five `run_code()` entries, and process error/timeout controls through `mathbench.evaluate._run`.

The local entries produced these verified objectives: identity seed 579,874; randomized RCM search 280,285 for its saved seed; spectral plus adjacent-swap method and reference 147,653. `evolution.py` was also run with a one-step test budget and its permutation passed exact checking. Full `evaluate_candidate("T045", ...)` is deferred until Sol admits the task to the shared registry. The expected missing-ID behavior is not a task failure.

Sol review remains required for an independent graph-source replay, source-date and open-status audit, human reference replay, upper/lower-bound wording, and acceptance status. The 95,242 published ordering and an LP lower-bound certificate are not stored, so the records distinguish those reports from the reproduced reference.
