# T082 implementation record

- Status: `pending_sol_review`.
- Configuration: T082-C01, 51 equal steps on `[0,2]`, range `[0,1]`, integral 1, minimize the two-sided overlap supremum.
- Human/source check: Haugland's 2016 arXiv paper reports its 51-step construction and rounded-up value `0.3809268534330870` ([arXiv:1609.08000](https://arxiv.org/abs/1609.08000); [HTML text](https://arxiv.org/html/1609.08000)). The paper prints one half of the symmetric 51 entries. We use the repository's previously audited symmetric transcription. Its decimal rationals sum to `51/2`; thus the integral is exactly 1 without mass correction. Exact rational computation gives `64757565083624785688821235069923/170000000000000000000000000000000 = 0.38092685343308696`.
- Verification method: at shifts that are integer multiples of bin width `2/51`, compute the finite exact overlap sum. For two equal-bin step functions, the cross-correlation is linear between differences of bin endpoints, including the exterior zero regions. Therefore the maximum over all real shifts occurs at one of the 101 integer grid lags from -50 through 50. The checker evaluates all of them with `Fraction`.
- Limitation: this establishes a feasible score for the transcribed 51-step witness. It does not establish optimality of the fixed-step problem or of the limiting constant. Haugland's later 19-step example is a different configuration and is not substituted for this task's public record.
- Tests: `.venv/bin/python -m pytest -q tasks/t082/test_task.py` — 7 passed.
- JSON validation: `.venv/bin/python -m json.tool tasks/t082/task.json >/dev/null` and `.venv/bin/python -m json.tool tasks/t082/records.json >/dev/null` — passed.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T082-C01` / `init_program`：原始目标 `1/2`，验证 `exact`。
- `T082-C01` / `baseline`：原始目标 `2051699/4250000`，验证 `exact`。
- `T082-C01` / `human`：原始目标 `64757565083624785688821235069923/170000000000000000000000000000000`，验证 `exact`。
- `T082-C01` / `reference`：原始目标 `64757565083624785688821235069923/170000000000000000000000000000000`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T082 tasks/t082/human.py --strict
.venv/bin/python -m pytest tasks/t082 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
