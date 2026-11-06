# T060 implementation notes

Implemented the exact checker, no-argument candidate interface, evaluator adapter, guaranteed finite seed, redundant-block deletion baseline, metadata, and tests. The seed adds a 14-set for each still-uncovered four-set, so it creates at most 10,626 blocks and always covers the complete domain. The checker rejects malformed blocks, booleans, out-of-range points, repeated points, and duplicate blocks. It then independently enumerates all 10,626 four-subsets.

The La Jolla source and 23-block public record were checked on 2026-11-05. The witness was retrieved from the Zenodo archive, converted from 1-based to 0-based point labels, and stored as `data/sota_witness.json`. `sota.py` loads this witness. The exact task evaluator independently checks all 10,626 four-subsets. The 62-block published-method reconstruction remains the frozen human reference; the 40-block local greedy search remains in `reference.py`.

Validation command: `.venv/bin/python -m pytest tasks/t060/test_task.py` (not run by this implementation agent).

Main reviewer amendment: reproduced the published finite-geometry and induced-covering method as 62 blocks. All 10626 four-subsets verified. The public 23-block witness has now been archived locally and is pending Sol review.

## Sol acceptance / Sol验收

2026-11-04：原实现由主代理独立验收通过。2026-11-05新增的23块公开见证标记为待Sol验收。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。

- `T060-C01` / `init_program`：原始目标 `1001`，验证 `exact`。
- `T060-C01` / `baseline`：原始目标 `40`，验证 `exact`。
- `T060-C01` / `human`：原始目标 `62`，验证 `exact`。
- `T060-C01` / `reference`：原始目标 `40`，验证 `exact`。
- `T060-C01` / `sota`：原始目标 `23`，来源为 Zenodo 封存的 La Jolla witness；待 Sol 独立复核。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T060 tasks/t060/human.py --strict
.venv/bin/python -m pytest tasks/t060 -q
```

最佳公开见证及来源范围见本任务 `records.json` 和 `sota.json`。完整模型对比实验尚未开展。
