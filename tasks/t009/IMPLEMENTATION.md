# T009 implementation notes

- Active configuration: T009-C02, 16 directions in S², maximize minimum angular separation in radians. Acceptance remains `pending_sol_review`.
- Configuration validation checks both the ID and the exact parameter object (`n=16`, `space=S2`, and the named radian objective).
- The prior N=15 configuration was replaced after the research audit confirmed a 2026 optimality proof for that case. Its public coordinate file remains in `data/spherical_code_3_15.txt` only for historical provenance; it is not a valid witness for the active task.
- Source checked: spherical-codes.org and its linked `/data/3/16` coordinate file. The public row reports cosine 0.612294616483. The 16 coordinates yield recomputed maximum normalized pair cosine approximately 0.6122946164826968 and minimum angle approximately 0.9118367215999165 radians. The table cites K. Schütte and B. L. van der Waerden (1951); Henry Cohn is credited as maintainer, not original author.
- Checker behavior: exact rational arithmetic parses each input coordinate, rejects zero vectors and duplicate directions, and checks all 120 pairs. Antipodal points are valid distinct points. Strict mode encloses normalized pair cosines and then bounds `atan2(sqrt(1-c²),c)` for the maximum cosine. It returns the outward-rounded interval lower endpoint as the objective, so the scored value is conservative. It does not certify global optimality. Non-strict mode reports the interval midpoint as numeric.
- Input rules: exactly 16 three-coordinate lists; integer, finite float, or rational-string coordinates; bool, NaN, infinity, malformed strings, zero vectors, repeated vectors, and distinct positive scalar multiples of one direction are rejected. Nonunit vectors are accepted and normalized by direction for scoring. Unknown or parameter-mismatched configurations are rejected.
- Baseline: bounded multistart SciPy optimization from independently generated nonzero random directions. It does not read human/reference data. The simple seed is a Fibonacci-sphere construction.
- Validation command: `.venv/bin/python -m pytest tasks/t009/test_task.py`.
- Known limits: the construction is a feasible reference, not a proof of the best possible 16-point code. Interval certification relies on mpmath's interval arithmetic implementation.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T009-C02` / `init_program`：原始目标 `0.7915824124681972`，验证 `certified`。
- `T009-C02` / `baseline`：原始目标 `0.7920330343039196`，验证 `certified`。
- `T009-C02` / `human`：原始目标 `0.9118367215999161`，验证 `certified`。
- `T009-C02` / `reference`：原始目标 `0.9118367215999161`，验证 `certified`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T009 tasks/t009/human.py --strict
.venv/bin/python -m pytest tasks/t009 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
