# T072 implementation and verification record

## Configuration and status

- Configuration: `T072-C01`; exactly 32 distinct positive integers, with no upper bound.
- Objective: minimize `max(|A+A|, |AA|)`.
- Reproduced human and public construction: 154 sums and 154 products, so objective 154.
- Optimality remains open in the checked sources. Status: `accepted_by_sol`.

## Sources and provenance

O'Bryant, [Visualizing the Sum-Product Conjecture, arXiv:2411.08139v2](https://arxiv.org/html/2411.08139v2), Table 2 reports `Psi_35^5` minus `{75,81,100}` at cardinality 32, with sumset and product set sizes 154 and 154. The table caption says its minima are not known to be optimal. Section 2 describes traditional computational exploration, mainly using Mathematica 14 and some Julia 1.10. The checked paper does not discuss generative-AI use; this record makes no claim about unreported workflow details.

The [author dataset page](https://www.math.csi.cuny.edu/~obryant/SumProduct/) supplies `SPPsets.txt`. Its retrieved snapshot is 102,089,754 bytes, SHA-256 `20d33250e047272c170fb575a9dad51dec81c882a5694d2a674d2357dae597b8`, and 1,163,592 lines. The paper's v2 abstract reports an older count of 1,162,868. The task retains only source line 1,005,722, 91 bytes, SHA-256 `0cd52d3292fdef5a69e851e8c6d8c37c285666c6064377dc09e3c6cd7e0a58e4`; it does not copy the complete file. The matching witness JSON has SHA-256 `21862735ba6d83cb1017b2c3cfad783d0fc039ba18d0ac85d45a7398240d7e25`.

The checked 2026 paper [arXiv:2601.21828](https://arxiv.org/abs/2601.21828) proves exact values at cardinalities 10 and 11. It does not settle cardinality 32. The 154 construction is a feasible upper bound, not a minimum proof.

## Programs

- `check.py` rejects wrong cardinality, non-integers, booleans, nonpositive values, and duplicates. It recomputes both sets using exact arbitrary-precision integer operations. There is no element-size cap.
- `init_program.py` is standalone and returns `{1,...,32}`.
- `baseline.py` runs seeded hill climbing from that same simple set. Each step replaces one or two elements. It allows occasional equal-score moves to explore plateaus.
- `evolution.py` maintains a small elitist population and applies one- or two-element replacements. It also starts from `{1,...,32}`.
- The two search programs cap proposed values at 4096 by default. This cap only limits their heuristic proposals; it is not a task or checker constraint. `MATHBENCH_SEARCH_INTEGER_LIMIT` changes it.
- `human.py` and `reference.py` replay the fixed source-derived construction. Initial and search programs do not import or read this witness.
- `evaluator.py` uses the shared candidate evaluator. No task registry entry is added by this task agent.

## Checks performed

Tests independently parse the saved source row and calculate all pairwise sums and products. They cover all five program entries, exact witness replay, wrong cardinality, duplicate elements, booleans, floats, NaN, infinity, nonpositive values, huge integers, forged score fields, configuration mismatch, worker errors, and timeouts.

Commands:

```sh
.venv/bin/python -m pytest tasks/t072 -q
.venv/bin/python -m json.tool tasks/t072/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t072/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t072/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t072/data/source/source_notes.json > /dev/null
```

Results on CPython 3.13.12, Linux x86_64:

- `.venv/bin/python -m pytest tasks/t072 -q`: 8 passed in 0.37 seconds.
- JSON parsing passed for all four JSON records listed above.
- Seed 0, default fixed budgets, no wall-clock cutoff: initial output objective 354 (`|A+A|=63`, `|AA|=354`); baseline after 500 iterations returned 331 (`195`, `331`) in 0.193 seconds; evolution after 60 generations returned 352 (`124`, `352`) in 0.014 seconds.
- `human.py` and `reference.py` each returned objective 154 with exact counts `(154,154)`.
- The public witness was independently recomputed from the 32 integers; 1,024 ordered pairs were checked for each operation.
- Runner defaults remain 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one thread. The test exercises `_run` error and short-timeout paths. The full task suite was not run.

This implementation has not been accepted by Sol. It remains `accepted_by_sol`.
