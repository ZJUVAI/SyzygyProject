# T002 implementation report

Status: `pending_sol_review`.

The task uses 26 unit squares. The input gives each center `(x,y)` and rational half-angle tangent `t`. The checker derives `cos=(1-t²)/(1+t²)` and `sin=2t/(1+t²)`, builds exact rational corners, applies separating-axis tests to all 325 pairs, and reports the side of the smallest axis-aligned square containing the full layout. Floats are interpreted as exact binary rationals. The seed is a 5 by 6 axis-aligned grid with side 6. The basic baseline makes bounded local perturbations and keeps only exact-feasible improvements; it returns the valid seed otherwise.

The public Friedman paper checked on 2026-11-03 states in Section 3 that its off-center family packs `2a²+4a+b²+1` unit squares in a square of side `a+3/2+b/√2`; for `(a,b)=(2,3)` this is 26 squares and side `(7+3√2)/2`. The saved witness follows this formula: it places the central 3 by 3 rotated block, constructs the frame from the stated grid family, excludes cells that intersect the block, and adds the five-square column. The exact Q(√2) checker certifies all 325 pairs and both bounding extents, each equal to `(7+3√2)/2`. The Squares Project page reports the interval `5.545 ≤ s(26) ≤ 5.62132034355964`; the optimum remains open. The simpler side-6 grid remains the deterministic search seed and is not used as the human baseline.

## Commands

```sh
.venv/bin/python -m pytest tasks/t002 -q
.venv/bin/python -m json.tool tasks/t002/task.json >/dev/null
.venv/bin/python -m json.tool tasks/t002/records.json >/dev/null
.venv/bin/python -m json.tool tasks/t002/data/seed.json >/dev/null
```

## Limits

The Friedman witness is reconstructed from the published formula rather than copied coordinate-by-coordinate from Figure 9. Exact algebraic arithmetic certifies the reconstructed geometry. The search baseline remains a bounded local search and gives no optimality proof.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T002-C01` / `init_program`：原始目标 `6`，验证 `certified`。
- `T002-C01` / `baseline`：原始目标 `6`，验证 `certified`。
- `T002-C01` / `human`：原始目标 `7/2+3/2*sqrt2`，验证 `certified`。
- `T002-C01` / `reference`：原始目标 `7/2+3/2*sqrt2`，验证 `certified`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T002 tasks/t002/human.py --strict
.venv/bin/python -m pytest tasks/t002 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。

## Staged expansion implementation (2026-11-04)

C03 (`n=29`) and C04 (`n=38`) are staged in `configuration_expansion.json` with `pending_sol_review`; `task.json` is unchanged. C02 (`n=17`) was removed from this expansion because source review found a formalized reported proof of optimality. It must stay out until that claim receives its own review.

The strict checker now accepts n=26, 29 and 38, computes all pair checks from the configured n, and uses exact Q(√2) arithmetic for its algebraic formulas and exact rational arithmetic for rational inputs. `data/human_schadt_2025.json` converts all 29 squares from the later exact rationalization of Schadt’s 2025 numerical pose. The source rational YAML is archived as `data/source_schadt_n029_rational.yaml`; `rebuild_witnesses.py` reproduces both staged JSON witnesses without PyYAML. The source’s human search found the layout; a later repository contribution created the rational certificate. The converter averages each square’s four corners for its center and computes its rational half-angle tangent from the first edge. The checker independently verifies all 406 pairs. Its exact side is the fraction in `records_expansion.json` (approximately 5.933885799813026).

`data/human_gobel_figure1.json` reconstructs the a=5 member of Göbel’s Figure 1 diagonal-strip family. It has 15 squares in each staircase, two corner squares, and six 45-degree squares. The exact side is `6+sqrt(2)/2`. The checker verifies all 703 pairs and both bounding extents.

Both staged initial programs use axis-aligned grids and do not read human data. The baseline makes 40 bounded exact-feasible local proposals from the initial program. Human/reference programs read their task-local witness. Records distinguish the n=29 reproduced human construction from the newer public result and mark Gensane–Ryckelynck’s 2004 witness as unreproduced.

Commands run:

```sh
.venv/bin/python -m pytest tasks/t002 -q
.venv/bin/python -m json.tool tasks/t002/configuration_expansion.json >/dev/null
.venv/bin/python -m json.tool tasks/t002/records_expansion.json >/dev/null
```

Result: `11 passed`. Sol review remains required. Neither configuration claims optimality.
