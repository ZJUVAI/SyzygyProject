# T057 implementation notes

- Configuration: `T057-C01`; 2 to 512 distinct integers in `[-1000000,1000000]`; maximize the normalized logarithmic ratio.
- `check.py` rejects duplicate elements and bool values. It forms `A+A` and `A-A` with exact integer arithmetic. It accepts only cases with `|A+A| > |A-A| > |A|`, so the score is defined and greater than one.
- The checker evaluates logarithms with mpmath interval arithmetic and returns the interval lower endpoint as the conservative maximize objective. A regular floating-point score is not treated as exact.
- The simple seed is `{0,2,3,4,7,11,12,14}`. Exact checking gives `|A+A|=26`, `|A-A|=25`, and a certified ratio above 1.0344. `baseline.py` starts from this valid lower bound and applies bounded local add/delete moves. Neither reads the human or reference witness.
- Public witness provenance: Martin and O'Bryant, [arXiv:math/0608131](https://arxiv.org/abs/math/0608131). Its 17 elements and exact counts (59,55) are reproduced in `human.py` and `records.json`.
- The public snapshot date is 2026-11-04. It is a finite record snapshot, not a world-best claim.
- Validation: `.venv/bin/python -m pytest tasks/t057/test_task.py -q` passed (10 tests). `task.json` and `records.json` both passed `.venv/bin/python -m json.tool`. The baseline ran with `PYTHONPATH=tasks/t057`; its returned set passed the trusted checker with exact counts 26 and 25.
- Status: `pending_sol_review`.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T057-C01` / `init_program`：原始目标 `1.034421215625998107826754355611914904363368310747775356577516581961163849508028730503`，验证 `certified`。
- `T057-C01` / `baseline`：原始目标 `1.034421215625998107826754355611914904363368310747775356577516581961163849508028730503`，验证 `certified`。
- `T057-C01` / `human`：原始目标 `1.059793094547245377600002106026027810995517075670792756303442005379263930059059337409`，验证 `certified`。
- `T057-C01` / `reference`：原始目标 `1.059793094547245377600002106026027810995517075670792756303442005379263930059059337409`，验证 `certified`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T057 tasks/t057/human.py --strict
.venv/bin/python -m pytest tasks/t057 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
