# T080 implementation notes

- Configuration: `T080-C01`, 20 nonnegative coefficients, support `[-1/4, 1/4]`, maximize AC2.
- The checker uses `Fraction` for each convolution term and the objective. It rejects wrong lengths, negative values, bools, NaN/infinity, malformed rationals, and zero mass. Claimed scores are ignored.
- `data/human_t080.json` stores the decimal coefficients from the cited 2009 appendix. Exact recomputation matches `108065664771600646574507764702/121527759800529249872686490775` and the rounded value `0.8892261730897966`.
- The deterministic seed and bounded local-edit baseline use generated positive integer coefficients and do not read human/reference witness data.
- A later result `0.962694` is listed separately in `records.json`; its representation and witness have not been matched to 20 steps.
- Tests: `.venv/bin/python -m pytest tasks/t080/test_task.py` (to run after files are installed).
- Acceptance status: `pending_sol_review`.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T080-C01` / `init_program`：原始目标 `1153011461750113/1801446296727186`，验证 `exact`。
- `T080-C01` / `baseline`：原始目标 `884125647619295/1145841092579883`，验证 `exact`。
- `T080-C01` / `human`：原始目标 `108065664771600646574507764702/121527759800529249872686490775`，验证 `exact`。
- `T080-C01` / `reference`：原始目标 `108065664771600646574507764702/121527759800529249872686490775`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T080 tasks/t080/human.py --strict
.venv/bin/python -m pytest tasks/t080 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
