# T014 implementation

The checker parses coordinates as rational numbers, enforces the `n=11` configuration and unit-square bounds, rejects duplicate points, and computes all 165 triangle areas exactly. It returns the objective as a fraction string and marks the verification status `exact`. A zero minimum area is a valid score.

The initializer uses the rational parabola points `(i/10, i²/100)`, for `i=0,…,10`. The separate human witness stores Goldberg's 1972 public 11-point construction. Its published score is `1/27`; this is a construction record, not a proof that no better 11-point arrangement exists.

The baseline uses fixed-seed random restarts and bounded coordinate perturbations. The final coordinates are scored by the exact checker. Its score must be recorded only after running the baseline.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T014-C01` / `init_program`：原始目标 `1/1000`，验证 `exact`。
- `T014-C01` / `baseline`：原始目标 `462496714710343552389619850215399/20000000000000000000000000000000000`，验证 `exact`。
- `T014-C01` / `human`：原始目标 `1/27`，验证 `exact`。
- `T014-C01` / `reference`：原始目标 `1/27`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T014 tasks/t014/human.py --strict
.venv/bin/python -m pytest tasks/t014 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
