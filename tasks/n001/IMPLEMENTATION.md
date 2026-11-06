# N001 implementation

- Configuration: N001-C01, q=7, power=5, maximize cardinality, human reference 367.
- The checker validates integer symbols, word length, uniqueness, and all unordered pairs. It ignores the candidate score and derives the objective from the word count. Strict mode uses the same exhaustive exact finite check.
- The seed is the product set {0,2,4}^5 (243 words). The baseline uses seeded random greedy construction over all 7^5 vertices and bitset conflict tracking, then bounded one-for-many local search. It does not read the human or reference witness.
- The task-local reference witness is based on Polak and Schrijver, [arXiv:1808.07438](https://arxiv.org/abs/1808.07438). The research witness was independently checked across all 67,161 pairs.
- Validation: `.venv/bin/pytest -q tasks/n001/test_task.py` — 9 passed; `.venv/bin/python -m json.tool tasks/n001/task.json`; `.venv/bin/python -m json.tool tasks/n001/records.json`.
- Limitation: 367 is a feasible published construction. The independence number for this fixed graph power has not been established by this task.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `N001-C01` / `init_program`：原始目标 `243`，验证 `exact`。
- `N001-C01` / `baseline`：原始目标 `244`，验证 `exact`。
- `N001-C01` / `human`：原始目标 `367`，验证 `exact`。
- `N001-C01` / `reference`：原始目标 `367`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate N001 tasks/n001/human.py --strict
.venv/bin/python -m pytest tasks/n001 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
