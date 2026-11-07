# T062 implementation record

Status: `accepted_by_sol`.

The fixed instance is `T062-C01`, maximizing the cardinality of a subset of `[42025]` with no positive square difference. The exact checker uses Python integers and checks all positive square translations within the interval. Its result is independent of candidate `objective`, `score`, and `claimed_score` fields.

The human construction was rebuilt from Mark Lewko's Theorem 3 residue set modulo 205. The frozen JSON witness is `data/reference/lewko205_n42025.json`, SHA-256 `c31651d54da1b1bdd2b8ce73d74096ad5bdc259e9dd99799f6d9f9509aab7730`. It has 2460 distinct elements, with minimum 8 and maximum 42020. A separate exact verification checked every positive-square shift `k^2` for `1<=k<=204`; none maps a selected element to another selected element.

The source theorem is asymptotic. The reproduced 2460 is a finite feasible construction, not an exact optimum claim. The checked literature audit and its limits are documented in `README.md` and `sota.json`. The cubic-difference residue set in the same paper is excluded.

The initial program returns `{1}`. The search uses ascending greedy followed by a fixed-seed randomized-order greedy, with a fixed trial count unless `MATHBENCH_SEARCH_SECONDS` is explicitly set. Neither reads comparison assets. The human program reconstructs the residue formula; the reference program reads only the frozen file under `data/reference/`.

Validation command and result:

```sh
.venv/bin/python -m pytest tasks/t062/test_task.py -q
```

The stored witness SHA-256 and exact objective are also checked by the task tests. Generation uses the shared 300-second limit; verification uses the shared 60-second limit. No external Python package is required.
