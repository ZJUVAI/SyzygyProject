# T044 implementation notes

For C01, the checker requires exactly 29 integer marks and rejects booleans, floats, and duplicate marks. It enumerates all 406 pairwise differences and rejects repeated values. It returns the span `max(marks) - min(marks)` as the exact integer objective. It ignores claimed scores and accepts translations. The checker now takes its mark count from the config, so C02/C03 check 435/496 differences.

The public witness was reconstructed from cube20's `modrules-pp-00` record. The gap sequence has 30 entries and sums to modulus 871. After prefix sums, multiplying each residue by 188 modulo 871 and sorting gives the cyclic modular ruler. The 29 consecutive marks beginning at residue 669 have span 623; the checker validates all 406 differences.

The source table identifies this as the Atkinson–Hassenklover (1984) projective-plane construction for 29 marks, with finite-field parameter 29. The value is a construction upper bound. Optimality for 29 marks is not established by the sources checked.

The initializer is a deterministic greedy extension and does not read the human witness. The baseline uses a fixed random seed and constructs rulers from fresh differences; it uses a bounded time budget. No human/reference witness is loaded by either program.

Validation command: `.venv/bin/python -m pytest tasks/t044/test_task.py` — 8 passed. The bounded baseline was also executed and returned a valid 29-mark ruler of length 1158. The baseline never reads the public witness.

## Staged C02/C03 expansion

See [EXPANSION.md](EXPANSION.md). Both public witnesses have been reconstructed
from cube20's `rulers-all-00.zip` rows and checked exactly. Their parameters
were cross-checked against `golomb-all-00.zip`. C02 has 30 marks and span 680;
C03 has 32 marks and span 784. Their source records and exact data are kept in
`configuration_expansion.json`, `records.json`, and `data/public_30_32.json`.
The staged configurations remain `pending_sol_review` and are not in
`task.json`.

Expansion validation: `.venv/bin/python -m pytest tasks/t044/test_task.py -q`
— 12 passed. Both staged JSON files parsed. The default-seed search returned
valid lengths 1311 and 1522 for C02 and C03. These results are search feedback,
not records or claims of optimality.

Sources checked: [cube20 Golomb ruler construction data](https://cube20.org/golomb/) and [Shearer's archived ruler table](https://web.archive.org/web/20060110160821/http://www.research.ibm.com/people/s/shearer/grtab.html). The task's human reference remains 623, matching the reconstructed witness. A search for a 2026 length-622 witness did not find an attributable construction; a page that uses 622 as a challenge ceiling is not evidence that such a ruler exists.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T044-C01` / `init_program`：原始目标 `1158`，验证 `exact`。
- `T044-C01` / `baseline`：原始目标 `1158`，验证 `exact`。
- `T044-C01` / `human`：原始目标 `623`，验证 `exact`。
- `T044-C01` / `reference`：原始目标 `623`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T044 tasks/t044/human.py --strict
.venv/bin/python -m pytest tasks/t044 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
