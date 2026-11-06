# T005 implementation notes

Status: `pending_sol_review`.

## Configurations and objective

T005-C01 uses 26 circles. T005-C02 uses 32 circles. Both configurations maximize the exact sum of radii in the unit square. The checker derives the score from the submitted radii and does not accept a claimed score.

## Witnesses and provenance

The saved human witnesses start with the public equal-circle coordinate files `data/csq26.txt` and `data/csq32.txt` from `https://packomania.com/csq/txt/csq26.txt` and `https://packomania.com/csq/txt/csq32.txt`. The original coordinates use a square centered at the origin. The witness files translate centers by `(1/2, 1/2)` and subtract `1/10^9` from each radius. Exact `Fraction` checks establish square containment and non-overlap for all 325 pairs at n=26 and all 496 pairs at n=32. The resulting radius sums are 2.50542078826 and 2.811460994816.

These are transferred equal-radius constructions. Their feasibility applies to this variable-radius task, but equal-radius optimality does not establish variable-radius optimality. `records.json` keeps these reproduced historical constructions separate from the public variable-radius frontier. The n=26 frontier value 2.635983084919 comes from the repository research summary; this implementation did not obtain or reproduce its witness. The current n=32 public value and exact provenance remain unresolved.

## Programs

`init_program.py` returns a 6 by 6 grid subset with radius 1/12 as a simple feasible seed. `baseline.py` starts from the same grid and makes a bounded SLSQP attempt. It emits the grid if the numerical attempt does not return an improved feasible proposal. The human/reference coordinate files are never read by either program. `reference.py` loads the task-local witness for trusted checking.

## Validation

Command run:

```sh
.venv/bin/python -m pytest tasks/t005/test_task.py -q
```

Result: 9 passed. Tests cover both saved witnesses, exact score sums, tangent grid boundaries, wrong sizes, wall violations, overlapping circles, boolean rejection, and ignored claimed scores. Source coordinate records were also independently parsed as decimal `Fraction` values; the radius reduction was checked against all exact wall and pairwise distance constraints.

## Open evidence

The public best-known variable-radius witness has not been reproduced here. In particular, the n=32 current public value and provenance need review. The historical source attributions refer to equal-radius constructions, not records for the variable-radius objective.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T005-C01` / `init_program`：原始目标 `13/6`，验证 `certified`。
- `T005-C01` / `baseline`：原始目标 `13/6`，验证 `certified`。
- `T005-C01` / `human`：原始目标 `125271039413/50000000000`，验证 `certified`。
- `T005-C01` / `reference`：原始目标 `125271039413/50000000000`，验证 `certified`。
- `T005-C02` / `init_program`：原始目标 `8/3`，验证 `certified`。
- `T005-C02` / `baseline`：原始目标 `8/3`，验证 `certified`。
- `T005-C02` / `human`：原始目标 `10982269511/3906250000`，验证 `certified`。
- `T005-C02` / `reference`：原始目标 `10982269511/3906250000`，验证 `certified`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T005 tasks/t005/human.py --strict
.venv/bin/python -m pytest tasks/t005 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
