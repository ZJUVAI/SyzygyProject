# T035 implementation record

- Configuration: `T035-C01`, degree 4, girth 10, minimize vertex count.
- `run_code()` data contract: an object with positive integer `vertices` and an `edges` list of undirected endpoint pairs; endpoints are integer labels in `[0, vertices)`.
- The trusted checker rejects booleans, non-integers, out-of-range endpoints, loops, duplicate edges, non-4-regular graphs, disconnected graphs, and graphs without exact girth 10. It computes the objective from the vertex count and ignores a claimed value.
- Human witness source: the paper authors' public graph6 file `genLifts/data/graphs/cage/n320_k4_g10.g6`, converted to `data/human_graph.json`. The paper reports `243 <= n(4,10) <= 320`; the order 320 is not proved optimal.
- The seed builds `X^(5,37)` by projectively normalized matrix multiplication on `PGL_2(37)`. The LPS graph has 50,616 vertices and degree 6. The code removes two distinct generator matchings, leaving a 4-regular graph. This construction is independent of the task-local 320-vertex human witness. The baseline starts from the valid LPS graph and tries to delete a vertex. It pairs the four neighbours in each of three ways. Before adding an edge, it runs a depth-8 BFS with the deleted vertex blocked. It adds an edge only when the endpoints have distance at least 9. This protects the girth constraint. It returns the first connected result, or the LPS graph if the search budget expires. The trusted checker verifies exact girth. The default search limit is 2 seconds. For seed 0, the baseline returns a valid graph on 50,615 vertices.
- Source graph6 SHA-256: `2e0186417514270a2d9488c83baaeb0f6fe797d3829da05f98f4dada6fe8147d`. Converted JSON SHA-256: `dba7e70847bb9d417b38092ba17a4a71afbe62ed731bf2942b558c5277b7d7b7`.
- Acceptance status stays `pending_sol_review`.

## Validation performed

- `.venv/bin/python -m pytest -q tasks/t035/test_task.py`: 8 passed after final negative-case coverage.
- `python3 -m json.tool` on `task.json`, `records.json`, and `data/human_graph.json`: passed.
- `python3 -m py_compile tasks/t035/*.py`: passed.
- Shared evaluator on `reference.py` and `human.py`: validity 1.0, objective 320, exact verification, compatibility score 1.0. The initial `human.py` import-path error was fixed; the final evaluator run passed.
- Shared evaluator on `init_program.py`: validity 1.0, objective 50,616, exact verification, compatibility score 0.00632211158526948. Shared evaluator on `baseline.py`: validity 1.0, objective 50,615, exact verification, compatibility score 0.0063222364911587475. It deleted one vertex and added two edges. The resulting graph had 101,230 edges and passed connectedness, degree, simplicity, and exact girth checks.
- The mathematical witness is validated by the exact local checker, not by graph6 metadata alone.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T035-C01` / `init_program`：原始目标 `50616`，验证 `exact`。
- `T035-C01` / `baseline`：原始目标 `50615`，验证 `exact`。
- `T035-C01` / `human`：原始目标 `320`，验证 `exact`。
- `T035-C01` / `reference`：原始目标 `320`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T035 tasks/t035/human.py --strict
.venv/bin/python -m pytest tasks/t035 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
