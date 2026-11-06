# Repository Guidelines

## Project Structure & Module Organization

This repository contains a mathematical construction benchmark and its research records. `tasks/` holds task packages. `mathbench/` holds the runner, adapters, and replay tools. `tests/` holds shared tests. `reports/` holds acceptance results and saved witnesses. `research/` holds paired Markdown and JSON inventories grouped by subject (`discrete`, `geometry`, and `algebra_analysis`). Files ending in `_round2` contain a second research round. `research/sources/` contains source material. `research/baseline_examples/` contains recomputed examples.

## Development & Validation

Use Python 3.11 or newer. The local validated environment is `.venv`. Dependencies are in `pyproject.toml` and `requirements-lock.txt`. Run checks that match the change:

```sh
.venv/bin/python -m pytest tests tasks -q
.venv/bin/python scripts/independent_audit.py
python3 -m json.tool research/configuration_selection.json > /dev/null
```

Replace the path with each modified JSON file. Review Markdown rendering and check that links, counts, and corresponding Markdown and JSON records remain consistent. For mathematical changes, independently recompute examples where possible and document the verification method and limitations.

## Benchmark 要求

### 范围与配置

- 首批范围为 20 个任务。每个任务选 1–5 个配置，不要求数量相同。
- 对照 SimpleTES、DREAM-RSI 和 Google DeepMind AlphaEvolve 的数学任务。记录任务与原论文、公开仓库和固定版本的对应关系。仅因更名或参数变化不新增任务数。
- 当前配置选型以 `research/configuration_selection.json` 为准。配套说明见 `research/configuration_selection.md`。
- 已接入的配置以各任务的 `task.json` 为准。已验收的证据见 `reports/acceptance.json`。选型清单不能自动加入运行目录。
- 类别表示研究方向。任务固定数学目标与可行性规则。配置固定参数，例如正方形数量、码长或矩阵阶数。
- 随机种子、重复运行、搜索时间和数学目标的单调变换不另算配置或任务。
- 参数可以有无限多种取值。benchmark 只选有限个有代表性的实例。优先考虑不同规模、不同构造结构和可承担的验证成本。
- 已证明最优或完全解决的配置排除。不得为凑数量加入已解小实例。后续发现最优性证明时，标记退役并保留历史记录。
- 配置须有公开、可验证的人类构造或人类方法基线。有名的问题或数据库入口不能替代相同参数的证据。
- 人类基线可以弱于公开纪录。历史构造、可重建公式及传统计算搜索均可使用。必须说明来源和复现程度。
- 一个任务只有一个可靠开放配置时，可以保留一个。不得仅改参数就声称基线和验收已完成。

### 数学目标与评分

- 每个配置须有一个明确的标量目标。记录原始指标、单位、最大化或最小化方向及全部约束。
- 评测器独立读取构造并重算成绩。不得信任候选程序声明的分数。
- 正式排名只使用有效构造。无效结果标记无效，原始目标为空。启发式罚分只用于搜索反馈。
- 保留原始数学成绩。兼容分数使用冻结对照：最大化为 `J/H`，最小化为 `H/J`，无效为零。采用比值前须确认分母与符号适用；其他情况先制定并冻结评分规则。
- 兼容分数超过 1 只表示超过冻结对照。不能据此声称突破公开纪录。
- 跨配置汇总先在任务内汇总，再对任务等权汇总。不得让配置多的任务自动获得更大权重。汇总公式须在实验前冻结；尚未冻结时只报告逐配置成绩。
- 逐配置独立搜索与统一程序跨配置评测分开报告。前者不能直接支持泛化结论。当前所选参数是公开的，不能称为隐藏测试集。

### 每个任务的交付内容

- 数学定义、模型指令、固定配置和主来源。
- 独立评测器、简单初始程序、传统搜索基线、人类构造复现程序、固定的最佳可复现参考程序。
- 最佳公开结果档案。区分最佳人类结果、AI 辅助结果和来源未披露的结果。区分相同参数与其他参数。
- 每个配置均须有有效初始构造和已复现的人类对照。配置改变后须重新验证构造和成绩。
- 测试覆盖合法构造、破坏构造、重复数据、异常数值、边界情况、程序错误和超时。
- 保存构造、验证结果、实际运行环境、随机种子、预算及可重放命令。正式成绩必须能从保存的构造重新计算。

### 接口、预算与实验隔离

- 程序入口为 `run_code()`。任务评测入口为 `evaluate(program_path)`。公共接口见 `tasks/CONTRACT.md`。
- 默认使用 CPU。每次生成限时 300 秒，验证另限时 60 秒，内存 4 GiB，一个计算线程。记录实际环境；预算变更须显式配置。
- 传统搜索记录算法、迭代数、随机种子及预算。按时间截断的结果须说明机器差异。
- 被测模型统一从简单程序开始。人类构造、固定参考和纪录见证只作外部对照，不进入初始上下文。
- 初始程序与传统搜索程序不得读取参考见证。实验操作者须阻止模型访问对照资产。资源限制运行器不等于安全隔离环境。
- 搜索可以使用快速数值检查。正式成绩须有精确计算或保守区间依据。采样与浮点容差不能当作数学证书。
- SimpleTES 与 DREAM-RSI 的接口示例须能运行。接口验证、完整上游搜索和完整模型对比实验分别报告。

### Sol 与 Luna 的分工及验收

- 主代理与最终验收者使用 GPT-6.1 Sol。任务子代理使用 GPT-6 Luna。
- 实现阶段每个任务由独立 Luna 代理负责。返修交回原代理。T005 的全部配置由同一个任务代理负责。
- 最多同时运行 Sol 与 3 个任务代理。Luna 只修改自己任务的目录；公共接口、依赖、目录和汇总由 Sol 修改。
- Luna 交付一律标记“待 Sol 验收”。Sol 才能标记通过、退回修改或暂缓。
- Sol 须核对数学定义、目标方向和参数来源，亲自运行人类基线，检查简单起点与传统搜索，并复核最佳公开结果档案。
- 每个配置至少独立复算一个关键量，运行一个合法样例和一个故意破坏的样例，并检查篡改声明分数不能改变重算结果。
- 定义或证明有缺口时保持未完成。不得放宽验证条件绕过问题。
- 区分“已选配置”“待实现”“待 Sol 验收”“已通过 Sol 验收”。原研究中的“通过选型”不等于实现完成。
- 新配置只有完成上述交付和验收后，才能加入正式运行目录及验收数量。新增配置不得继承旧配置的通过状态。

## Content Style & Naming

Use descriptive Markdown headings and concise explanations. Follow existing subject-based filenames, lowercase snake_case for multiword filenames and JSON keys, and stable kebab-case candidate IDs such as `graph-cage`. Preserve existing JSON structure and two-space indentation. Keep related Markdown and JSON inventories aligned; cite primary sources and identify exact parameters, objective direction, verification costs, and uncertainties.

## Research & Testing Guidelines

Apply the criteria in `research/benchmark_selection_principles.md`: distinguish feasible constructions from proofs of optimality, and distinguish verified baselines from unverified literature claims. Do not present sampling or floating-point checks as mathematical certificates. When adding a baseline, record its provenance and whether its witness and score have been independently verified. Preserve the distinction between accepted, conditional, and rejected candidates.

## Commits & Pull Requests

Git history is unavailable in this checkout, so no established commit convention can be inferred. Use a short, descriptive imperative commit subject. Pull requests should describe the research or data changes, cite relevant sources, identify changed inventories, and summarize validation and unresolved limitations. Link a related issue when available.

## Language

- Use ASD-STE100 for English technical text. Use approved words and defined technical terms.
- For Chinese text, apply the same principles: use common words, short sentences, and clear actions.
- Use one term for one concept. Explain a technical term at first use.
- Keep each sentence to one main idea. Remove words that add no information.
- State facts, proposals, and unknowns separately. Give measured values when available.
- Do not use the Chinese sentence pattern “不是……而是……”.
