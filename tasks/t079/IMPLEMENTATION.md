# T079 implementation notes

- Configuration `T079-C01`: 208 steps, support `[-1/4,1/4]`, nonnegative coefficients; minimize the normalized convolution maximum.
- `check.py` rejects wrong length, booleans, non-finite floats, negative values, malformed rationals, and zero mass. It uses `Fraction` and returns the exact objective and all maximizing convolution indices.
- `data/human_matolcsi_vinuesa.json` is a task-local copy of the research witness; runtime code does not read the research directory.
- The seeded init and local-edit baseline use no human witness data.
- Acceptance status: `pending_sol_review`.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T079-C01` / `init_program`：原始目标 `396117254/190026225`，验证 `exact`。
- `T079-C01` / `baseline`：原始目标 `1574683084/757735729`，验证 `exact`。
- `T079-C01` / `human`：原始目标 `6280435861361744576/4160000022692211721`，验证 `exact`。
- `T079-C01` / `reference`：原始目标 `6280435861361744576/4160000022692211721`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T079 tasks/t079/human.py --strict
.venv/bin/python -m pytest tasks/t079 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
