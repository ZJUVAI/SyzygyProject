# T099 implementation notes

- Selected configuration: `T099-C01`, `k=343`, minimize diameter, human reference 2340. Status remains `pending_sol_review`.
- Checker uses strict Python integer type checks, rejects booleans and duplicates, accepts negative values and translations, ignores claimed scores, and checks every prime through 343. For larger primes, 343 entries cannot cover all residue classes.
- Human data is copied from the repository's audited `research/baseline_examples/admissible_343_2340.json`. The witness is credited to Thomas Engelsma (2013). The available source's unmarked row does not establish optimality.
- The seed uses 343 consecutive multiples of the primorial. Its construction proves feasibility and its diameter follows directly from the endpoints.
- The search baseline builds its own admissible tuple by greedy residue checks and uses randomized interval replacement; it does not load human or reference data.
- Validation: `.venv/bin/python -m unittest tasks.t099.test_task` passed (5 tests); `.venv/bin/python -m json.tool tasks/t099/task.json` and the same command for `records.json` passed. A zero-second search-baseline run generated a 343-entry admissible tuple of diameter 2468, confirmed by the checker. A one-second run also returned a checked tuple (diameter 2468).
- Limitations: witness feasibility is established. Global minimality and the best available construction after the cited source snapshot remain unverified.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T099-C01` / `init_program`：原始目标 `738618971698707114724185491282414717945192998076415916248707090255107158808576221136520697066313981897227269221105572775579355751767196180`，验证 `exact`。
- `T099-C01` / `baseline`：原始目标 `2468`，验证 `exact`。
- `T099-C01` / `human`：原始目标 `2340`，验证 `exact`。
- `T099-C01` / `reference`：原始目标 `2340`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T099 tasks/t099/human.py --strict
.venv/bin/python -m pytest tasks/t099 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
