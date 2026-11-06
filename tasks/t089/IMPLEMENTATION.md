# T089 implementation notes

- Configuration: `T089-C01`, n=29, sign entries, maximize absolute determinant.
- The verifier rejects wrong dimensions, non-integer values (including bool), and values outside {-1,+1}. It ignores any claimed score and returns the exact Bareiss result.
- The public matrix is transcribed from Orrick et al. (2003), arXiv:math/0304410, order-29 display. A separate exact recomputation gives signed determinant `-1188957517256767569920`, equal in magnitude to `320*7^12*2^28`.
- The seed is `2I-J`; direct exact computation gives `-27*2^28`. The local search starts from this seed and reads no reference data.
- Commands run: `python3 -m unittest discover -s tasks/t089 -p 'test_task.py'`; `python3 -m json.tool tasks/t089/task.json >/dev/null`; `python3 -m json.tool tasks/t089/records.json >/dev/null`.
- Limitations: the literature witness is a feasible construction. Neither the paper nor the task claims a proof of global optimality. The baseline's elapsed-time budget is a practical bound; exact determinant computation is used for every accepted move.
- Status: `pending_sol_review`.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T089-C01` / `init_program`：原始目标 `7247757312`，验证 `exact`。
- `T089-C01` / `baseline`：原始目标 `61816709450825728`，验证 `exact`。
- `T089-C01` / `human`：原始目标 `1188957517256767569920`，验证 `exact`。
- `T089-C01` / `reference`：原始目标 `1188957517256767569920`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T089 tasks/t089/human.py --strict
.venv/bin/python -m pytest tasks/t089 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
