# T067 implementation report

Task implementation status: `accepted_by_sol` (2026-11-04). SOTA supplement status: `pending_sol` (2026-11-05).

## Construction and validation

The historical task baselines remain unchanged. The BCH-based human witness has 128 words and minimum distance 6. The 258-word result remains the highest reported lower bound for this configuration. Milshtein's abstract reports a length-16, distance-5 code with 258 words; adding an overall parity bit gives a length-17, distance-6 code. The 258-word witness is not reproduced in this package.

The SOTA replay uses the standard Octacode construction. It enumerates the 256 messages over `Z4` using the published 4-by-8 generator matrix, applies the published Gray map, then appends one zero coordinate. The result has 256 distinct 17-bit words. The exact T067 checker verifies all 32,640 pairs and finds minimum distance 6. The full witness is saved in `data/sota_nordstrom_robinson_256.json`; `sota.py` regenerates it from the formula. This is a reproduced public construction at 256, not a reproduction of the 258-word result.

The original BCH data file, human replay, randomized baseline, and starter are preserved. They remain separate from the SOTA replay.

## Source checks

- Brouwer's table lists `A(17,6)=258-340` and attributes the 258 lower bound to Milshtein.
- Milshtein's Springer abstract reports a `(16,258,5)` construction. Appending a parity bit produces the `(17,258,6)` construction cited by Brouwer.
- Forney, Sloane, and Trott identify the Nordstrom–Robinson code as the Gray image of the Octacode. Magma's public Z4-code documentation gives the exact generator matrix, Gray map, and 256-word count.
- OpenAlex marks the Milshtein paper closed and reports no repository full text. Semantic Scholar and OpenAIRE also mark the paper closed. The Internet Archive has no captured 200-response for the publisher PDF. The ResearchGate preview shows only the abstract and first page. The codeword table remains unavailable through the public sources checked.
- The Springer full-text TDM API requires an applicable license or special agreement. It was not used.

## Commands and results

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t067 -q
.venv/bin/python -m json.tool tasks/t067/task.json >/dev/null
.venv/bin/python -m json.tool tasks/t067/records.json >/dev/null
.venv/bin/python -m json.tool tasks/t067/data/bch_extended_128.json >/dev/null
.venv/bin/python -m json.tool tasks/t067/sota.json >/dev/null
.venv/bin/python -m json.tool tasks/t067/data/sota_nordstrom_robinson_256.json >/dev/null
```

Results: all 9 tests passed, with 7 subtests also passing. The 128-word historical witness and 256-word SOTA witness both pass exact pairwise-distance checks.

## Limits

No optimality proof is provided. The best reproducible public construction in the SOTA record is 256, two words below the highest reported lower bound of 258. The paper's codeword table has not been obtained, so the SOTA JSON keeps 258 in `highest_reported` and does not mark it as reproduced. The search baseline is heuristic and makes no optimality claim.

## Sol acceptance / Sol验收

2026-11-04：主代理独立验收通过。最终状态以 `task.json` 与 `../../reports/acceptance.json` 为准。所有配置均完成合法见证、故意破坏的构造、声明分数修改以及关键量独立复算检查。

- `T067-C01` / `init_program`：原始目标 `96`，验证 `exact`。
- `T067-C01` / `baseline`：原始目标 `128`，验证 `exact`。
- `T067-C01` / `human`：原始目标 `128`，验证 `exact`。
- `T067-C01` / `reference`：原始目标 `128`，验证 `exact`。

复跑：

```sh
.venv/bin/python -m mathbench evaluate T067 tasks/t067/human.py --strict
.venv/bin/python -m pytest tasks/t067 -q
```

SOTA 来源检索结果和 258 字见证缺口见本任务 `sota.json`。256 字Octacode见证尚待 Sol 独立验收。完整模型对比实验尚未开展。
