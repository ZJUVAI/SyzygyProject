# T081 implementation notes

- Selected only `T081-C02`: 208 equal bins on `[-1/4,1/4]`, signed values allowed, integral normalized to 1, minimize the maximum absolute autoconvolution.
- `check.py` treats every coefficient as an exact rational. Finite float inputs become their exact binary rational values. The checker rejects malformed values, booleans, nonfinite floats, the wrong configuration, wrong vector length, and zero coefficient sum.
- The full convolution has 415 coefficients. The score is `416 * max(abs(convolution)) / mass^2`; this equals the maximum absolute convolution after integral-one normalization and is invariant under nonzero scaling. Strict mode also uses the same exact full-domain calculation.
- The local human witness copies the 208 nonnegative coefficients in `research/baseline_examples/T079_matolcsi_vinuesa.json`. This admissible witness yields exact score `6280435861361744576/4160000022692211721` and decimal value `1.5097201507458786`.
- The primary paper record identifies Matolcsi and Vinuesa and describes explicit constructions, while the research audit identifies the copied witness as a published nonnegative 208-step construction. The transfer to the signed class is the benchmark's own admissibility inference. No optimality or latest-record claim is made. The source-supported signed 150-step value `1.458105685768` is a positive-only peak; its maximum-absolute score is about `2.426895802097`, so it is not used here.
- `init_program.py` is seeded and has EVOLVE markers. `baseline.py` performs bounded, mass-preserving signed coordinate search. Neither reads human data. Human and reference programs read the task-local witness.
- Validation: `.venv/bin/python -m pytest tasks/t081/test_task.py` (14 passed on 2026-11-04); `.venv/bin/python -m json.tool tasks/t081/task.json`; `.venv/bin/python -m json.tool tasks/t081/records.json`. Seeded init and zero-budget baseline smoke checks each returned 208 coefficients and passed the exact checker in the task-local worker import context.
- Source checked: https://arxiv.org/abs/0907.1379, primary paper record, accessed 2026-11-04. It supports authorship, 2009 version, subject, and explicit examples; see `research/confirmation_summary.json` for the audit's coefficient extraction and exact recomputation notes. The DREAM-RSI summary is not the human witness source and its one-sided `1.455642795...` objective is not used.
- Acceptance status: `pending_sol_review`.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T081-C02` / `init_program`：原始目标 `1756451731210942261445852549298250976/877498169092385841119192204846301409`，验证 `exact`。
- `T081-C02` / `baseline`：原始目标 `6981904708009195717660054042475770528/3509992676369543368223763709357458249`，验证 `exact`。
- `T081-C02` / `human`：原始目标 `6280435861361744576/4160000022692211721`，验证 `exact`。
- `T081-C02` / `reference`：原始目标 `6280435861361744576/4160000022692211721`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T081 tasks/t081/human.py --strict
.venv/bin/python -m pytest tasks/t081 -q
```

最佳公开见证的缺口及来源范围见本任务 `records.json` 和统一验收报告。完整模型对比实验尚未开展。
