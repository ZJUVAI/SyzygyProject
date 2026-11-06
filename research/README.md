# 数学构造发现 benchmark：研究与选型

2026-11-04更新：首批20个任务共35个配置，每题1–3个，均通过Sol验收。本轮由Luna实现14个新增配置，Sol复核。见[配置选型](configuration_selection.md)及[JSON](configuration_selection.json)。项目要求见[AGENTS.md](../AGENTS.md)。下文保留早期研究范围与数量。

当前入口：**[逐项核查汇总](confirmation_summary.md)** · [JSON](confirmation_summary.json) · [CSV](confirmation_summary.csv)。

2026-11-03：Luna 与主代理核查覆盖 **12 类、110 个候选任务家族**。91 个已确认适合选型；17 个仍待补证；2 个目前只核到须排除的配置。通过的配置记录为 94 条。仍未达到100个已确认家族。

首批建议 **10 类、20 个任务、21 个配置**。本轮只做调研与交互式选型，没有实现求解器或通用评分器。

用户已放宽基线要求：有公开可验证的人类构造、有明确单标量、所选配置未被证明最优，即可通过选型。历史人类基线可以使用。独立重算另作标记。

## 文件入口

- `confirmation_summary.*`：当前统一状态、参数、基线、来源与首批建议。
- `confirmation_geometry.*`、`confirmation_discrete.*`、`confirmation_algebra.*`：Luna分方向记录。
- `confirmation_discrete_supplement.*`：组合设计与编码的补充核查。
- `discovery_candidates_v2.*`：110家族的原候选目录；其旧状态文字由当前汇总取代。
- `benchmark_selection_principles.md`：类别、任务、配置、标量与证据口径。
- `baseline_examples/`：已保存的构造与重算结果。已解决的历史例子不因存档而重新准入。
- `sota_task_coverage.*`：系统论文原题去向；家族映射不代表所有配置已确认。
- `sources/`：保存的来源。

## 已修正的关键问题

- 排除已解的小参数，包括Golomb ≤28标记、部分周期序列、若干几何实例。
- Borcea二阶方差版本已有2026证明；改查仍开放的一阶版本。
- Smale旧常数1的猜想已有反例；保留最优常数尚未确定的构造任务。
- AC3最大值与最大绝对值分开。旧150步见证的绝对目标分数约2.42690，不能写成1.45810。
- K28直线交叉数基线是构造上界7234；7233是理论下界。
- 晶格覆盖密度2.900024对应7维；原6维标签已修正。

确认基于列出的来源。它不保证检索无遗漏，也不保证现纪录一定能改进。首批是选型建议；正式发布时仍须冻结实例、精度和资料版本。

## 首批实现

20个任务、21个配置的实现与Sol验收结果见[统一验收报告](../reports/acceptance.md)。本目录保留选型研究的历史状态；实现状态以 `tasks/*/task.json` 为准。
