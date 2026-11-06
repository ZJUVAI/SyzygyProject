# T097 implementation report

Status: `pending_sol_review`.

The task implements the fixed ordinary addition-chain target `2^192 - 2^64 - 3`. The checker uses exact Python integers. It rejects non-integer entries (including booleans), non-increasing chains, invalid addition steps, wrong endpoints, and unsupported configurations. Strict mode uses the same full exact check.

The human witness is the linked `P-192_field_inverse_202.txt` file from Neill Clift's page. The page credits McLoughlin for the previous 203-step value and describes Clift's new 202-step result. It has 203 entries and 202 additions. Independent replay confirms each addition and the endpoint. The source reports a prior length of 203, the 202-step result, and says the listed lengths are not proved optimal. The reference and human programs load only this task-local witness. The initial program uses binary expansion. The search baseline compares the binary chain with fixed-width sliding-window chains for widths 2 through 6. Its default work count is deterministic; `MATHBENCH_SEARCH_SECONDS` may stop it early. It does not read witness data.

Validation run:

```sh
.venv/bin/python -m unittest tasks.t097.test_task
.venv/bin/python -m json.tool tasks/t097/task.json >/dev/null
.venv/bin/python -m json.tool tasks/t097/records.json >/dev/null
```

Results: all 7 unit tests passed. Both JSON files parsed successfully.

Source check: https://additionchains.com/LargeChains.html. The page lists the exact exponent, 203 previous steps, 202 new steps, a downloadable chain, and states that none of the lengths is proved optimal.

Limitation: no global shortest-chain proof is provided.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T097-C01` / `init_program`：原始目标 `380`，验证 `exact`。
- `T097-C01` / `baseline`：原始目标 `241`，验证 `exact`。
- `T097-C01` / `human`：原始目标 `202`，验证 `exact`。
- `T097-C01` / `reference`：原始目标 `202`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T097 tasks/t097/human.py --strict
.venv/bin/python -m pytest tasks/t097 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。

## Staged configuration expansion

`T097-C02` targets `2^221-5`; `T097-C03` targets `2^521-3`. Both remain `pending_sol_review`. Their records are in `configuration_expansion.json`; the live `task.json` still contains only the accepted C01 configuration.

The primary source is Clift's [large addition-chain table](https://additionchains.com/LargeChains.html), updated 2 November 2026. It reports a 230-step M-221 chain (previously 231) and a 532-step P-521 chain (previously 533). I fetched and preserved the linked one-integer-per-line files at `data/human_t097_c02.json` and `data/human_t097_c03.json`. The source says its listed lengths are not proved optimal. No subtraction or modular reduction is used by the witnesses or checker.

The checker now selects the exact endpoint from the configuration ID. The seed and sliding-window search use `MATHBENCH_CONFIG_ID`; the human and fixed-reference programs load that configuration's local witness. Neither seed nor search reads witness files. For C02, exact replay returned 230 steps for human/reference, 439 for the binary seed, and 276 for search. For C03, it returned 532, 1039, and 633 steps, respectively. Damaged endpoints were rejected, and a forged `claimed_score` did not change either recomputed objective.

Validation run:

```sh
.venv/bin/python -m pytest tasks/t097 -q
```

Result: 9 tests passed, including 8 subtests, in 12.93 seconds. The suite covers both staged witnesses, all four program roles, invalid endpoints, and ignored claimed scores.

Limitations: the source calls the rows new records and reports previous lengths, but these are constructions and not optimality proofs. Sol must independently review the parameter provenance, attribution, witnesses, and per-configuration checks before either configuration is added to the live registry.
