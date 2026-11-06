# T066 implementation report

Status: `pending_sol_review`.

## Construction and verification

The reference witness is generated from three block-diagonal copies of the evaluation matrix for affine Boolean functions on four variables. Each block is RM(1,4), with parameters `[16,5,8]`. The final 20 coordinates are zero. The checker verifies binary entries, dimensions, GF(2) rank 15, then enumerates all 32767 nonzero linear combinations using Gray-code updates. The tests also recompute the witness distance with a separate direct XOR enumeration. Both methods report minimum distance 8.

The public BKLC entry was checked on 2026-11-04. It reports lower bound 24 and upper bound 26. Its construction chain ends in a subcode of a `[68,18,24]` code, but no matrix or data download was found at that entry. Therefore the published value 24 remains unverified here. The published-derived human witness has distance 8. A separate seed-zero project search witness has distance 17 and is recorded as AI-generated.

## Commands and results

Run the exact commands below from the repository root:

```sh
.venv/bin/python -m pytest tasks/t066 -q
python3 -m json.tool tasks/t066/task.json >/dev/null
python3 -m json.tool tasks/t066/records.json >/dev/null
python3 -m json.tool tasks/t066/data/human_generator.json >/dev/null
python3 -m json.tool tasks/t066/data/search_generator.json >/dev/null
```

Results: all 9 tests passed. All four JSON files parsed successfully. The independent witness check returned objective 8, verification status `exact`, rank 15, and 32767 checked nonzero codewords.

## Limits

No proof of optimality is provided. The best reproduced project result is 17. The published-derived human witness has distance 8. The public table's distance-24 witness was not independently reconstructed. The search baseline mutates entries of the parity block P in systematic `[I|P]` matrices. Each candidate keeps rank 15, receives an exact distance score from all 32767 nonzero words, and enters a simulated-annealing acceptance step. A regression test confirms a parity mutation can change the code and reduce distance from 2 to 1. The search is bounded and stochastic; it provides no optimality certificate. With `MATHBENCH_SEARCH_SECONDS=0` and seed 0, the saved starting matrix has exact distance 17.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T066-C01` / `init_program`：原始目标 `17`，验证 `exact`。
- `T066-C01` / `baseline`：原始目标 `19`，验证 `exact`。
- `T066-C01` / `human`：原始目标 `8`，验证 `exact`。
- `T066-C01` / `reference`：原始目标 `19`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T066 tasks/t066/human.py --strict
.venv/bin/python -m pytest tasks/t066 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
