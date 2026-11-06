# 项目计划

此文件是唯一的项目规划和研究结论入口。任务参数以各任务的 `task.json` 为准。公开来源保存在 `records.json`，SOTA 构造及复算信息保存在 `sota.json` 和 `data/`。自己的最佳构造保存在 `best/<配置ID>/`。

## 固定规则

- 保留20个任务，当前共35个配置。参数、种子与重复运行分别记录。已证明最优的配置退役，旧ID不复用。
- 每个配置有标量目标、方向、约束和同参数的人类构造对照。公开报告值与复算值分开。
- 正式成绩从构造独立重算。使用精确计算或保守区间。无效构造不计分。
- 简单起点和传统搜索不得读取对照见证。模型隔离实验与本地代码辅助搜索分开。
- 兼容分数采用冻结对照。超过对照不等于刷新公开纪录。跨任务汇总公式尚未冻结。
- 默认生成300秒、验证60秒、单线程。Linux地址空间限制4GiB；macOS记录未执行此限制。

## 当前状态

历史任务实现验收覆盖35个配置。完整模型对比实验尚未开展。服务器后续搜索已复核8个任务、14个配置；T009仅完成一个种子，仍待续跑。T005-C01另有接近所引公开值的独立结果。保留的最佳构造可在各任务的 `best/` 中重放。

| 任务 | 参数 | 后续搜索 |
|---|---|---|
| N001 | {"q": 7, "power": 5} | 待继续 |
| T001 | {"n": 26, "container": "unit square"}；{"n": 32, "container": "unit square"}；{"n": 50, "container": "unit square"} | 已复核 |
| T002 | {"n": 26}；{"n": 29}；{"n": 38} | 待继续 |
| T005 | {"n": 26, "container": "unit square", "radii": "variable"}；{"n": 32, "container": "unit square", "radii": "variable"} | C01已有独立结果 |
| T009 | {"n": 16, "space": "S2", "objective": "minimum pairwise angular separation in radians"}；{"n": 17, "space": "S2", "objective": "minimum pairwise angular separation in radians"}；{"n": 19, "space": "S2", "objective": "minimum pairwise angular separation in radians"} | 待继续 |
| T014 | {"n": 11}；{"n": 12}；{"n": 16} | 已复核 |
| T035 | {"degree": 4, "girth": 10} | 待继续 |
| T044 | {"marks": 29}；{"marks": 30}；{"marks": 32} | 待继续 |
| T057 | {"max_cardinality": 512, "integer_interval": [-1000000, 1000000]} | 待继续 |
| T060 | {"v": 24, "k": 14, "t": 4} | 待继续 |
| T066 | {"n": 68, "k": 15, "q": 2} | 待继续 |
| T067 | {"n": 17, "distance": 6} | 待继续 |
| T073 | {"L": 100}；{"L": 80}；{"L": 120} | 已复核 |
| T079 | {"steps": 208, "support": ["-1/4", "1/4"], "nonnegative": true} | 已复核 |
| T080 | {"steps": 20, "support": ["-1/4", "1/4"], "nonnegative": true} | 已复核 |
| T081 | {"steps": 208, "support": ["-1/4", "1/4"], "signed_values_allowed": true, "integral": 1} | 已复核 |
| T082 | {"steps": 51, "support": "[0,2]", "range": "0≤f≤1", "integral": 1} | 已复核 |
| T089 | {"n": 29, "entries": "±1"} | 已复核 |
| T097 | {"target": "2^192-2^64-3"}；{"target": "2^221-5"}；{"target": "2^521-3"} | 待继续 |
| T099 | {"k": 343} | 待继续 |

## 待办

1. 在Mac原生Python3.13环境安装固定依赖，运行公共测试及任务测试。
2. 继续其余任务。每个配置保存构造、种子、预算、环境和重放命令。
3. 改善T073搜索算法后重新测量。现有best保留旧结果，尚未运行的新代码不算成绩。
4. 核对新结果与同参数公开来源，再由主代理验收。不得自动把程序运行成功标记为Sol验收。
5. 冻结跨配置汇总规则后，再开展隔离的完整模型比较。

## 已知限制

- T081已超过旧的非负208步对照。绝对峰值与正峰值是不同目标。公开更强报告还使用300、600、800步，不能当作208步结果。来源：https://github.com/teorth/optimizationproblems/blob/main/constants/1d.md 。
- T057开发代理曾意外显示human.py；不纳入隔离的冷启动模型比较。
- T009、T057的独立数值复算只作交叉检查，正式成绩仍采用验证器的精确或区间依据。
- 时间截断结果受机器速度影响。部分旧程序未输出迭代数。
- Mac实机尚未验证。服务器旧Python不满足最低版本，其4项T009测试因缺少math.nextafter失败；此前有效环境的完整测试通过。

## 维护方式

以后只在本文件更新计划、结论、状态和待办。不再维护research或reports。任务的机器可读参数、来源、见证和复算结果随任务代码更新。临时运行数据写入各任务的runs目录，不提交Git。原始研究及完整历史实验已移到仓库外备份。

## 上游接口

SimpleTES使用`mathbench/simpletes_evaluator.py`，对应T073-C01。DREAM-RSI使用`mathbench/dream_rsi_evaluator.py`，对应T005-C02。与对应任务的instruction.txt和init_program.py配套。这里只完成接口级验证，尚未运行完整上游模型实验。

## 本轮整理验证

15个保留的最佳构造通过独立进程严格重放。18项公共测试通过。全套202项测试中198项通过；4项T009测试仍因当前服务器Python3.8缺少math.nextafter失败。没有放宽数学检查来消除这些失败。

## 完整候选选型档案

保留原始T001–T100全部100项候选，以及后续修订、排除理由和来源核查。候选数量不等于已实现任务数量。原始目录中的旧MVP建议不再作为当前准入依据。后续修订记录优先；实际运行参数以任务目录的task.json为准。原始资料仍在仓库外备份。以下JSON保留原字段和值，不再建立并行研究文件。字段中的旧research文件名仅表示历史来源，不要求恢复旧目录。

### 100项索引

| ID | 任务 | 类别 | 历史准入状态 |
|---|---|---|---|
| T001 | Equal-circle packing in fixed containers | 几何装填与覆盖 | pending_open_configuration_audit |
| T002 | Packing unit squares in squares | 几何装填与覆盖 | pending_open_configuration_audit |
| T003 | Equilateral-triangle packing in a square | 几何装填与覆盖 | pending_open_configuration_audit |
| T004 | Maximum polygon packing (CG:SHOP 2024) | 几何装填与覆盖 | pending_open_configuration_audit |
| T005 | Unequal-circle packing: maximum sum of radii | 几何装填与覆盖 | pending_open_configuration_audit |
| T006 | Erdős unequal squares: maximum total side length | 几何装填与覆盖 | pending_open_configuration_audit |
| T007 | Circles covering circles | 几何装填与覆盖 | pending_open_configuration_audit |
| T008 | Covering a square with unit squares | 几何装填与覆盖 | pending_open_configuration_audit |
| T009 | Tammes problem / spherical codes | 球面与极值点集 | pending_open_configuration_audit |
| T010 | Riesz energy minimization on the sphere (Thomson at s=1) | 球面与极值点集 | pending_open_configuration_audit |
| T011 | Minimum-size spherical t-design | 球面与极值点集 | pending_open_configuration_audit |
| T012 | Maximum-volume polytope with N vertices on a sphere | 球面与极值点集 | pending_open_configuration_audit |
| T013 | Heilbronn problem for a free convex region | 球面与极值点集 | pending_open_configuration_audit |
| T014 | Heilbronn triangle problem in a square | 球面与极值点集 | pending_open_configuration_audit |
| T015 | Minimum maximum-to-minimum pair-distance ratio | 球面与极值点集 | pending_open_configuration_audit |
| T016 | Largest small n-gon | 球面与极值点集 | pending_open_configuration_audit |
| T017 | Erdős minimum distinct-distance problem | 球面与极值点集 | pending_open_configuration_audit |
| T018 | Largest point set with no empty convex hexagon | 球面与极值点集 | excluded_closed_task |
| T019 | Erdős–Szekeres happy-ending number f(k) | 球面与极值点集 | pending_open_configuration_audit |
| T020 | Minimum-dilation triangulation | 几何图与计算几何 | pending_open_configuration_audit |
| T021 | Minimum-weight triangulation | 几何图与计算几何 | pending_open_configuration_audit |
| T022 | Minimum convex partition of a point set | 几何图与计算几何 | pending_open_configuration_audit |
| T023 | Minimum coverage by convex polygons (CG:SHOP 2023) | 几何图与计算几何 | pending_open_configuration_audit |
| T024 | Minimum partition into plane subgraphs (CG:SHOP 2022) | 几何图与计算几何 | pending_open_configuration_audit |
| T025 | Minimum non-obtuse triangulation (CG:SHOP 2025) | 几何图与计算几何 | pending_open_configuration_audit |
| T026 | Minimum-area simple polygonalization | 几何图与计算几何 | pending_open_configuration_audit |
| T027 | Maximum-area simple polygonalization | 几何图与计算几何 | pending_open_configuration_audit |
| T028 | Rectilinear crossing number of K_n | 几何图与计算几何 | pending_open_configuration_audit |
| T029 | Erdős maximum unit distances for n planar points | 几何图与计算几何 | pending_open_configuration_audit |
| T030 | Orchard planting / maximum 3-rich lines | 几何图与计算几何 | pending_open_configuration_audit |
| T031 | No-three-in-line maximum on an n×n grid | 几何图与计算几何 | pending_open_configuration_audit |
| T032 | Simple perfect squared squares: minimum primitive side at fixed order | 铺砌与分割 | pending_open_configuration_audit |
| T033 | Mrs. Perkins’s quilt | 铺砌与分割 | pending_open_configuration_audit |
| T034 | Klarner order of a polyomino | 铺砌与分割 | pending_open_configuration_audit |
| T035 | (d,g)-cage order | 极值图与超图 | pending_open_configuration_audit |
| T036 | Degree–diameter problem | 极值图与超图 | pending_open_configuration_audit |
| T037 | Zarankiewicz number Z_{s,t}(m,n) | 极值图与超图 | pending_open_configuration_audit |
| T038 | Forbidden-subgraph extremal number ex(n,F) | 极值图与超图 | pending_open_configuration_audit |
| T039 | Graph saturation number sat(n,F) | 极值图与超图 | pending_open_configuration_audit |
| T040 | Classical Ramsey number lower-bound construction | 极值图与超图 | pending_open_configuration_audit |
| T041 | Hypergraph Turán number ex_r(n,F) | 极值图与超图 | pending_open_configuration_audit |
| T042 | Erdős–Rogers function f_{s,t}(n) | 极值图与超图 | pending_open_configuration_audit |
| T043 | Minimum triangles at fixed edge count | 极值图与超图 | pending_open_configuration_audit |
| T044 | Optimal Golomb ruler length | 加法组合与离散构造 | pending_open_configuration_audit |
| T045 | Minimum diameter of a B_h set of integers, h≥3 | 加法组合与离散构造 | pending_open_configuration_audit |
| T046 | Difference triangle sets | 加法组合与离散构造 | pending_open_configuration_audit |
| T047 | Maximum cap set in F_3^n | 加法组合与离散构造 | pending_open_configuration_audit |
| T048 | Largest 3-term-progression-free subset of [n] | 加法组合与离散构造 | pending_open_configuration_audit |
| T049 | Minimum difference basis for [n] | 加法组合与离散构造 | pending_open_configuration_audit |
| T050 | Maximum sum-free subset of a finite group | 加法组合与离散构造 | excluded_closed_task |
| T051 | Schur number S(k) lower-bound coloring | 加法组合与离散构造 | pending_open_configuration_audit |
| T052 | van der Waerden number lower-bound coloring | 加法组合与离散构造 | pending_open_configuration_audit |
| T053 | Longest finite sequence with discrepancy at most C | 加法组合与离散构造 | pending_open_configuration_audit |
| T054 | Largest square-difference-free subset of [N] | 加法组合与离散构造 | pending_open_configuration_audit |
| T055 | Finite-set sum–product growth minimization | 加法组合与离散构造 | pending_open_configuration_audit |
| T056 | Minimum finite-field Kakeya set size | 加法组合与离散构造 | pending_open_configuration_audit |
| T057 | Sum–difference I: normalized logarithmic ratio | 加法组合与离散构造 | pending_open_configuration_audit |
| T058 | Sum–difference II: unnormalized logarithmic ratio | 加法组合与离散构造 | pending_open_configuration_audit |
| T059 | Sum–difference III: finite certificate for asymptotic exponent | 加法组合与离散构造 | pending_open_configuration_audit |
| T060 | Covering number C(v,k,t) | 组合设计 | pending_open_configuration_audit |
| T061 | Covering array CAN(t,k,v) | 组合设计 | pending_open_configuration_audit |
| T062 | Orthogonal array minimum-run construction | 组合设计 | pending_open_configuration_audit |
| T063 | Packing number D(v,k,t) | 组合设计 | pending_open_configuration_audit |
| T064 | Social golfer maximum schedule length | 组合设计 | pending_open_configuration_audit |
| T065 | Maximum number of mutually orthogonal Latin squares | 组合设计 | pending_open_configuration_audit |
| T066 | Best minimum distance of linear codes | 编码理论 | pending_open_configuration_audit |
| T067 | Maximum size of a binary code A(n,d) | 编码理论 | pending_open_configuration_audit |
| T068 | Constant-weight code A(n,d,w) | 编码理论 | pending_open_configuration_audit |
| T069 | Constant-dimension subspace code A_q(n,d;k) | 编码理论 | pending_open_configuration_audit |
| T070 | Covering code size | 编码理论 | pending_open_configuration_audit |
| T071 | Maximum permutation code size | 编码理论 | pending_open_configuration_audit |
| T072 | Maximum deletion-correcting code size | 编码理论 | pending_open_configuration_audit |
| T073 | LABS minimum aperiodic autocorrelation energy | 序列与平坦多项式 | pending_open_configuration_audit |
| T074 | LABS peak sidelobe level (PSL) | 序列与平坦多项式 | pending_open_configuration_audit |
| T075 | Periodic binary autocorrelation energy | 序列与平坦多项式 | pending_open_configuration_audit |
| T076 | Binary sequence maximum out-of-phase autocorrelation (periodic merit) | 序列与平坦多项式 | pending_open_configuration_audit |
| T077 | Littlewood polynomials: minimum supremum modulus | 序列与平坦多项式 | pending_open_configuration_audit |
| T078 | Littlewood polynomials: maximum infimum modulus | 序列与平坦多项式 | pending_open_configuration_audit |
| T079 | First Autocorrelation Inequality (AC1) | 极值分析 | pending_open_configuration_audit |
| T080 | Second Autocorrelation Inequality (AC2) | 极值分析 | pending_open_configuration_audit |
| T081 | Third Autocorrelation Inequality (AC3) | 极值分析 | pending_open_configuration_audit |
| T082 | Erdős Minimum Overlap | 极值分析 | pending_open_configuration_audit |
| T083 | Autocorrelation lower envelope for difference bases | 极值分析 | pending_open_configuration_audit |
| T084 | Sign uncertainty principle (Fourier sign changes) | 极值分析 | pending_open_configuration_audit |
| T085 | Cohn–Elkies linear-programming bound for sphere packing | 极值分析 | pending_open_configuration_audit |
| T086 | General one-dimensional Gagliardo–Nirenberg sharp constant | 极值分析 | pending_open_configuration_audit |
| T087 | Rudin spherical harmonic Lp extremizer | 极值分析 | pending_open_configuration_audit |
| T088 | Ovals curvature Schrödinger eigenvalue | 极值分析 | pending_open_configuration_audit |
| T089 | Maximum determinant of sign matrices | 矩阵、格与代数极值 | pending_open_configuration_audit |
| T090 | Minkowski lattice packing density | 矩阵、格与代数极值 | pending_open_configuration_audit |
| T091 | Sendov extremal critical-point distance | 矩阵、格与代数极值 | excluded_closed_task |
| T092 | Schmeisser polynomial critical-point barycenter constant | 矩阵、格与代数极值 | pending_open_configuration_audit |
| T093 | Borcea p-moment critical-point distance constant | 矩阵、格与代数极值 | pending_open_configuration_audit |
| T094 | Noncommutative matrix AM–GM ratio | 矩阵、格与代数极值 | pending_open_configuration_audit |
| T095 | Minimum Mahler measure of noncyclotomic integer polynomials | 矩阵、格与代数极值 | pending_open_configuration_audit |
| T096 | Integer Chebyshev polynomial construction | 矩阵、格与代数极值 | pending_open_configuration_audit |
| T097 | Shortest addition chain | 数论与算术构造 | pending_open_configuration_audit |
| T098 | Integer complexity | 数论与算术构造 | pending_open_configuration_audit |
| T099 | Narrow admissible prime k-tuples | 数论与算术构造 | pending_open_configuration_audit |
| T100 | Factoring N! into N balanced factors | 数论与算术构造 | pending_open_configuration_audit |

### 原始100项候选目录

<details>
<summary>原始100项候选目录：完整记录</summary>

迁入来源：`benchmark_100_candidates.json`；原文件SHA-256：`494a79400bfc7ccd3a7c1cc1e3f94b555315fda0e3c65d6aacc6da3041db5227`。

```json
{
  "title": "数学构造benchmark 100任务候选表",
  "date": "2026-11-03",
  "categories": 12,
  "tasks": 100,
  "proposed_mvp_tasks": 20,
  "proposed_mvp_configurations": null,
  "published_configurations": null,
  "warning": "历史100项索引，包含已整题排除的T018/T050/T091；现行发现轨以discovery_candidates_v2为准。原MVP建议已撤回，待开放配置重新验收。",
  "tasks_catalog": [
    {
      "id": "T001",
      "name": "Equal-circle packing in fixed containers",
      "category": "几何装填与覆盖",
      "definition": "Place n congruent disks without overlap in a square and minimize the square side (equivalently maximize the common disk radius in a unit square).",
      "solution_format": "disk centers and radius, or normalized center coordinates",
      "scalar_objective": "maximum common radius in unit square (equivalently minimum container side for unit disks)",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "圆数量",
        "container": "单位正方形为主；圆形/矩形等独立基线容器配置"
      },
      "human_baseline": "Packomania lists best-known values, coordinates, drawings, contact graphs, and attribution codes for n up to 10000; it marks proven optima. Human attribution in records, AI involvement unknown.",
      "primary_sources": [
        "https://packomania.com/csq/",
        "https://packomania.com/"
      ],
      "verification_cost": "medium; pairwise distance and wall-clearance checks; upper-bound optimality is generally hard",
      "risks": "Packomania is a changing best-known catalogue, not a proof for most n; choose frozen version/instances and verify contact tolerances.",
      "recommendation": "MVP候选",
      "reason": "Named classical continuous optimization problem, dense public records and coordinates, natural scalar objective.",
      "research_origin": "geometry.json",
      "source_id": "geo-circle-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T002",
      "name": "Packing unit squares in squares",
      "category": "几何装填与覆盖",
      "definition": "Pack n non-overlapping unit squares, allowing arbitrary rotation, into the smallest enclosing square.",
      "solution_format": "square centers and orientations; enclosing side s",
      "scalar_objective": "minimum enclosing-square side s(n)",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "正方形数量",
        "container": "正方形主轨；其他容器须独立基线"
      },
      "human_baseline": "Erich Friedman’s 2009 survey gives best-known bounds/packings for n≤100 and historical authors. It proves selected n and reports named constructions by Göbel, Trump, Wainwright, Hämäläinen, Bidwell, Cantrell, and others; computer-search involvement is explicit for some later records. AI involvement unknown.",
      "primary_sources": [
        "https://erich-friedman.github.io/papers/squares/squares.html",
        "https://kingbird.myphotos.cc/packing/squares_in_squares.html"
      ],
      "verification_cost": "medium; non-overlap and enclosure directly checkable; optimality proof hard",
      "risks": "Do not treat upper-bound construction as proven optimum except rows marked/proven in the paper; use exact coordinate reconstruction.",
      "recommendation": "MVP候选",
      "reason": "Named longstanding problem, unusually clear human history, explicit scalar and published benchmark range.",
      "research_origin": "geometry.json",
      "source_id": "geo-unit-squares-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T003",
      "name": "Equilateral-triangle packing in a square",
      "category": "几何装填与覆盖",
      "definition": "Pack n unit equilateral triangles, arbitrary orientations, inside the smallest square.",
      "solution_format": "triangle placements and square side",
      "scalar_objective": "minimum square side",
      "direction": "minimize",
      "configuration_parameters": "n; unit side triangles; rotations allowed",
      "human_baseline": "Friedman’s page gives per-n constructions and named records: Friedman (1996), Maurizio Morandi (2008), with later results; AI involvement unknown.",
      "primary_sources": [
        "https://erich-friedman.github.io/packing/triinsqu/"
      ],
      "verification_cost": "medium",
      "risks": "Page updated in 2026; freeze selected historical instance and confirm exact coordinates; many records are upper bounds only.",
      "recommendation": "后备候选",
      "reason": "Good archived scalar problem and human constructions, pending data extraction and current-best reconciliation.",
      "research_origin": "geometry.json",
      "source_id": "geo-triangles-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T004",
      "name": "Maximum polygon packing (CG:SHOP 2024)",
      "category": "几何装填与覆盖",
      "definition": "Select a subset of given polygonal items and place them inside a container polygon without overlap, using translations only, maximizing the official weight/area objective.",
      "solution_format": "selected polygon IDs and translations",
      "scalar_objective": "total selected item area/weight as defined by challenge",
      "direction": "maximize",
      "configuration_parameters": "official CG:SHOP 2024 item/container instances; no rotation per challenge definition",
      "human_baseline": "Official challenge and paper document 2024 competition, data, ranking, and participating solvers; Shadoks paper describes their feasible solutions. AI involvement unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2024/",
        "https://arxiv.org/abs/2403.16203",
        "https://arxiv.org/abs/2403.20123"
      ],
      "verification_cost": "medium; polygon containment and non-overlap checks",
      "risks": "Confirm official scoring is exactly total area/weight (and all rules); internal optimum NP-hard, so use returned feasible value or valid bound.",
      "recommendation": "后备候选",
      "reason": "Strong competition benchmark; exact task scalar and feasibility semantics must match the 2024 specification.",
      "research_origin": "geometry.json",
      "source_id": "geo-maximum-polygon-packing",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T005",
      "name": "Unequal-circle packing: maximum sum of radii",
      "category": "几何装填与覆盖",
      "definition": "Pack n or a source-defined number of circles in a fixed container, maximizing their total perimeter subject to containment and non-overlap.",
      "solution_format": "circle centers/radii",
      "scalar_objective": "sum_i r_i",
      "direction": "maximize",
      "configuration_parameters": "fixed container and either fixed n or source-defined permitted counts",
      "human_baseline": "Friedman’s catalog lists a ‘Packing Copies to Maximize Total Perimeter’ section, including circles in squares, but specific page outcomes/authors are not verified here; unknown.",
      "primary_sources": [
        "https://www.packomania.com/csqv/csqv.html",
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/36.html"
      ],
      "verification_cost": "medium",
      "risks": "Variable radii/count may be part of optimization; exact source problem needs reading. Do not define own penalty.",
      "recommendation": "MVP候选",
      "reason": "Has a natural scalar and named catalog, but human baseline/details need direct source audit.",
      "research_origin": "geometry.json",
      "source_id": "geo-maximum-circles-perimeter-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T006",
      "name": "Erdős unequal squares: maximum total side length",
      "definition": "在单位正方形中放置 n 个可旋转、大小可不同、内部不重叠的正方形。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "sum_i side_i",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "正方形数量",
        "rotation": "允许任意旋转；平行边子类单列配置"
      },
      "human_baseline": "Halasz (1984)、Erdős–Soifer (1995)、Campbell–Staton (2005) 有显式构造；例如 n=k²+2 的历史下界 k+1/(k+1)。选定非平方数配置后须重建原文布局。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/55.html",
        "https://doi.org/10.1080/00029890.2005.11920180"
      ],
      "verification_cost": "中：多边形相交与边界精确谓词。",
      "risks": "不同于等尺寸正方形装填；历史公式的旋转和零边长约定须锁定。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-free-squares",
      "category": "几何装填与覆盖",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T007",
      "name": "Circles covering circles",
      "category": "几何装填与覆盖",
      "definition": "Place n unit disks to cover the largest possible circular target disk.",
      "solution_format": "unit-disk centers and target radius",
      "scalar_objective": "maximum target radius covered",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "覆盖圆数量",
        "target": "单位圆/单位正方形等各固定配置"
      },
      "human_baseline": "Friedman’s table reports named discoveries and proven records (e.g. Bezdek, Fejes Tóth, Melissen, Tan) for n values, along with a 2026 proof attribution for several; AI involvement is unknown, so historical attribution must not be read as AI-free.",
      "primary_sources": [
        "https://erich-friedman.github.io/packing/circovcir/"
      ],
      "verification_cost": "medium; union containment check and radius calculation; optimality proof hard",
      "risks": "Dynamic page has post-cutoff updates; freeze a dated snapshot and select explicit constructions with machine-readable coordinates if possible.",
      "recommendation": "后备候选",
      "reason": "Strong archive with per-n scalar results and named human construction/proof history.",
      "research_origin": "geometry.json",
      "source_id": "geo-circles-cover-circle",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T008",
      "name": "Covering a square with unit squares",
      "category": "几何装填与覆盖",
      "definition": "Among coverings of a square by n unit squares (overlap allowed), maximize the side of the covered target square.",
      "solution_format": "square placements including orientations",
      "scalar_objective": "maximum target-square side s(n)",
      "direction": "maximize",
      "configuration_parameters": "n; covering squares have side 1; overlap allowed",
      "human_baseline": "Friedman and Paterson’s paper gives constructions/bounds and named sources; known optimality only for n=2,3,5,10 and square n per the survey. Authors of unattributed examples are given; AI involvement unknown.",
      "primary_sources": [
        "https://erich-friedman.github.io/papers/covering/covering.html",
        "https://erich-friedman.github.io/papers/covering.pdf"
      ],
      "verification_cost": "medium; exact coverage of target square requires geometric union check; optimum proofs difficult",
      "risks": "Only keep instances with archived explicit configurations; source says many bounds are not exact optima.",
      "recommendation": "后备候选",
      "reason": "Published named covering problem with natural scalar and identified optimal cases plus constructions.",
      "research_origin": "geometry.json",
      "source_id": "geo-unit-square-cover-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T009",
      "name": "Tammes problem / spherical codes",
      "category": "球面与极值点集",
      "definition": "Place N points on S² to maximize their minimum pairwise angular separation (equivalently chord distance).",
      "solution_format": "N unit vectors",
      "scalar_objective": "minimum pairwise angular distance",
      "direction": "maximize",
      "configuration_parameters": "N; dimension 3 for cited tables",
      "human_baseline": "Henry Cohn’s table lists constructions through N=32 with nearest-pair inner products and rattler counts; Sloane’s tables include downloadable coordinates. Records are not all proven optima. Historical human attribution; AI use unknown.",
      "primary_sources": [
        "https://cohn.mit.edu/spherical-codes/",
        "https://neilsloane.com/packings/",
        "https://cohn.mit.edu/sloane/"
      ],
      "verification_cost": "Low for feasibility; global optimality is hard.",
      "risks": "Use a frozen N row and report best-known versus proven status; do not count distinct container variants as separate tasks.",
      "recommendation": "MVP候选",
      "reason": "Named problem, public coordinates, natural scalar.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-tammes",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T010",
      "name": "Riesz energy minimization on the sphere (Thomson at s=1)",
      "category": "球面与极值点集",
      "definition": "For fixed N points on S², minimize the sum over unordered pairs of distance raised to −s; Thomson is s=1.",
      "solution_format": "N unit vectors / coordinate file",
      "scalar_objective": "Σ(i<j) ||xi−xj||^(−s)",
      "direction": "minimize",
      "configuration_parameters": "N and exponent s; fix s=1 for Thomson",
      "human_baseline": "Cambridge Riesz Energy Database, s=1, lists 53 lowest-known minima for N=512–9913, with energy, symmetry, and downloadable coordinates; N=512 energy 124673.9055677. These are lowest located minima, not all certified global minima. AI use unknown.",
      "primary_sources": [
        "https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/index.html",
        "https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html"
      ],
      "verification_cost": "Low-medium; evaluate all pair terms with suitable precision.",
      "risks": "Freeze N,s and do not call a located minimum globally optimal without proof.",
      "recommendation": "后备候选",
      "reason": "Maintained data has exact coordinate files and natural energy scalar; genuinely different from Tammes.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-riesz",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T011",
      "name": "Minimum-size spherical t-design",
      "category": "球面与极值点集",
      "definition": "For fixed dimension and strength t, find an equal-weight spherical t-design using the fewest points.",
      "solution_format": "point coordinates plus moment identities/certificate",
      "scalar_objective": "number of points N",
      "direction": "minimize",
      "configuration_parameters": "fix dimension d and strength t; S² is the best documented library",
      "human_baseline": "Hardin–Sloane library provides putatively optimal designs and coordinates. Their paper reports a 24-point 7-design first found by McLaren (1963), and records existence/minimal-size claims; it explicitly distinguishes analytic proofs from numerical coordinates. AI use unknown.",
      "primary_sources": [
        "https://neilsloane.com/sphdesigns/",
        "https://cohn.mit.edu/sloane/",
        "https://doi.org/10.1007/BF02711518"
      ],
      "verification_cost": "Medium-high; check all polynomial moments, with exactness needed for a proof.",
      "risks": "Small residual is not proof of exact design or minimum N; choose rows with exact coordinates and lower-bound certificate. Exact moment identities need certificates; approximate designs are a separately named track.",
      "recommendation": "后备候选",
      "reason": "Natural integer objective and public constructions, but per-instance proof/verification burden is high.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-spherical-design",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T012",
      "name": "Maximum-volume polytope with N vertices on a sphere",
      "category": "球面与极值点集",
      "definition": "Choose at most N vertices on the unit sphere in R³ to maximize convex-hull volume.",
      "solution_format": "unit-vector coordinates / named polyhedron",
      "scalar_objective": "convex-hull volume",
      "direction": "maximize",
      "configuration_parameters": "vertex cap N; unit sphere in R³",
      "human_baseline": "Sloane tables include maximal-volume arrangements and downloadable coordinates. A 2026 paper resolves N=9 exactly: volume 3√(2√3−3), attained by a triaugmented triangular prism of specified shape. Human theorem and construction; AI use unknown.",
      "primary_sources": [
        "https://cohn.mit.edu/sloane/",
        "https://arxiv.org/abs/2608.04392"
      ],
      "verification_cost": "Medium to calculate hull volume; optimum proof depends on N.",
      "risks": "Clarify at-most versus exactly N vertices. N=9 is a calibration, not open discovery.",
      "recommendation": "后备候选",
      "reason": "Distinct natural volume objective with an exact value and explicit human construction.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-max-poly-volume",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T013",
      "name": "Heilbronn problem for a free convex region",
      "category": "球面与极值点集",
      "definition": "Place N points in any unit-area convex region to maximize the smallest triangle area among triples, normalized by the convex hull area.",
      "solution_format": "point coordinates",
      "scalar_objective": "minimum triple triangle area divided by convex-hull area",
      "direction": "maximize",
      "configuration_parameters": "N; convex hull is free and normalized to area 1",
      "human_baseline": "Tej Stead’s table provides coordinates and a rational-arithmetic verifier. For N=8, A=0.0800001393294664…; David Cantrell found the construction (2007), and Tej Stead proved optimality (2026). The value is the root of 2060x^5−2332x^4+1064x^3−240x^2+26x−1.",
      "primary_sources": [
        "https://math.tejstead.com/heilbronn/convex/",
        "https://math.tejstead.com/heilbronn/"
      ],
      "verification_cost": "Low for candidate coordinates; upper-bound proof varies by N.",
      "risks": "Living page has later AI-assisted records; use N=8 and label provenance explicitly.",
      "recommendation": "后备候选",
      "reason": "Specific human construction, proof, coordinates, natural scalar.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-heilbronn-free",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T014",
      "name": "Heilbronn triangle problem in a square",
      "category": "球面与极值点集",
      "definition": "Choose n points in a unit square to maximize the area of the smallest triangle determined by any three chosen points.",
      "solution_format": "n point coordinates",
      "scalar_objective": "minimum area over all point triples",
      "direction": "maximize",
      "configuration_parameters": "n; unit square domain",
      "human_baseline": "Tej Stead maintains a dedicated Heilbronn-problem page linked by Friedman’s catalog; this audit did not verify specific authors, numeric records, or downloadable data, so baseline is unknown.",
      "primary_sources": [
        "https://math.tejstead.com/heilbronn/square/",
        "https://github.com/spiralulam/heilbronn"
      ],
      "verification_cost": "low for a given point set (enumerate triples); optimum determination is hard",
      "risks": "An instance is n and domain; published records and coordinate data must be verified before admission. Do not use nested optimum as scorer.",
      "recommendation": "MVP候选",
      "reason": "Natural computable scalar, but the human-baseline requirement is not established by the sources checked.",
      "research_origin": "geometry.json",
      "source_id": "geo-heilbronn-triangle-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T015",
      "name": "Minimum maximum-to-minimum pair-distance ratio",
      "category": "球面与极值点集",
      "definition": "Choose N points in R^d to minimize maximum pair distance divided by minimum pair distance; scale and translation are immaterial.",
      "solution_format": "N coordinates",
      "scalar_objective": "max pair distance / min pair distance",
      "direction": "minimize",
      "configuration_parameters": "N,d; choose 2D N=5 or 7 for proved records",
      "human_baseline": "Friedman’s records state r²=(3+√5)/2 for N=5 and r²=4 for N=7, proved by Bateman and Erdős (1951); N=8 is proved by Bezdek and Fodor (1999). Diagrams are published. Newer rows include 2026 contributors; AI use there unknown.",
      "primary_sources": [
        "https://erich-friedman.github.io/packing/maxmin/",
        "https://doi.org/10.1007/BF02574074"
      ],
      "verification_cost": "Low for a candidate; global optimum proof hard for larger N.",
      "risks": "Do not constrain points to an arbitrary box; avoid recent AI-assisted rows if using a human-only baseline.",
      "recommendation": "后备候选",
      "reason": "Named problem with direct ratio objective and human-proved values.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-minmax-ratio",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T016",
      "name": "Largest small n-gon",
      "category": "球面与极值点集",
      "definition": "Among convex n-gons of diameter at most 1, maximize area.",
      "solution_format": "cyclic vertex coordinates with diameter normalized",
      "scalar_objective": "polygon area",
      "direction": "maximize",
      "configuration_parameters": "n vertices; diameter bound 1; convexity",
      "human_baseline": "Reinhardt (1922) proved regular n-gons optimal for every odd n. Exact/global records also exist for n=4,6,8,10,12; Henrion–Messine used GloptiPoly for n=10,12 with global/numerical guarantees, and Audet et al. gave exact algebraic equations for small even cases.",
      "primary_sources": [
        "https://optimization-online.org/wp-content/uploads/2020/09/8019.pdf",
        "https://arxiv.org/abs/1103.4456",
        "https://www.mcs.anl.gov/~more/cops/bcops/polygon.html"
      ],
      "verification_cost": "Low for area/diameter/convexity; global certificate specialized.",
      "risks": "Choose a fixed n and distinguish proof from local numerical record.",
      "recommendation": "后备候选",
      "reason": "Named extremal task, natural area scalar, many concrete human results.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-largest-small-polygon",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T017",
      "name": "Erdős minimum distinct-distance problem",
      "category": "球面与极值点集",
      "definition": "For a fixed N, choose N distinct planar points that determine as few distinct positive pairwise Euclidean distances as possible.",
      "solution_format": "N point coordinates; normalize by similarity",
      "scalar_objective": "number of distinct pairwise distances",
      "direction": "minimize",
      "configuration_parameters": "N; Euclidean plane; arbitrary point coordinates",
      "human_baseline": "Erdős (1946) introduced D(N). A square lattice construction gives O(N/sqrt(log N)) distinct distances for square-grid sizes; Guth and Katz (Annals 2015) prove every N-point planar set determines at least cN/log N distances. For N=4 a square gives exactly 2 distances and is a simple exact calibration. AI use unknown for historical constructions.",
      "primary_sources": [
        "https://annals.math.princeton.edu/wp-content/uploads/annals-v181-n1-p02-p.pdf"
      ],
      "verification_cost": "Low for a fixed exact/rational coordinate set; global optimum proof is hard.",
      "risks": "A construction yields an upper bound on the minimum, not a proof of optimality. Use exact small-N calibration or compare distinct-distance count only; do not require an uncertified inner optimum.",
      "recommendation": "后备候选",
      "reason": "Distinct natural integer objective and major human construction/theorem history, but public coordinate/result benchmark files were not verified here.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-distinct-distances",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T018",
      "name": "Largest point set with no empty convex hexagon",
      "category": "球面与极值点集",
      "definition": "Find a largest finite point set in general position with no empty convex 6-gon.",
      "solution_format": "point coordinates",
      "scalar_objective": "number of points",
      "direction": "maximize",
      "configuration_parameters": "forbidden polygon size 6; no three collinear",
      "human_baseline": "Overmars (2003) found 29 points with no empty hexagon. Gerken and Nicolás proved every 30-point set contains one, so optimum is 29. A public paper gives the construction/search; formal verification work supplies a SAT certificate for the upper bound. Human result with computer-assisted search/proof.",
      "primary_sources": [
        "https://citeseerx.ist.psu.edu/document?doi=40b403e751d8807c5609b9eb571711077489bf45&repid=rep1&type=pdf",
        "https://arxiv.org/abs/2403.00737",
        "https://arxiv.org/abs/2403.17370"
      ],
      "verification_cost": "Low for candidate set; global upper proof is high.",
      "risks": "Solved calibration; retrieve point coordinates from Overmars paper/data before admitting.",
      "recommendation": "删除：整个任务已解",
      "reason": "Exact maximum, named construction, natural cardinality scalar.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-empty-hexagon-free",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "最大无空凸六边形点集=29；h(6)=30已在2024证明并形式验证。旧表误将精确30归于Gerken/Nicolas；两人2006证明的是存在有限阈值。",
      "discovery_entry_status": "excluded_closed_task"
    },
    {
      "id": "T019",
      "name": "Erdős–Szekeres happy-ending number f(k)",
      "category": "球面与极值点集",
      "definition": "Find the minimum N such that every N points in general position in the plane contain k points in convex position.",
      "solution_format": "For lower-bound witness, coordinates of N−1 points with no convex k-gon; score N−1. Exact f(k) only with matching upper proof.",
      "scalar_objective": "largest point-set size avoiding a convex k-gon",
      "direction": "maximize",
      "configuration_parameters": {
        "convex_subset_size": "k"
      },
      "human_baseline": "Erdős–Szekeres (1935) proved finiteness and conjectured f(k)=2^{k−2}+1; exact f(3)=3 through f(6)=17 are known, with Peters (2006) computer proof for f(6)=17. Suk (2017) gives f(k)=2^{k+o(k)}.",
      "primary_sources": [
        "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0EC7876789232266D60439A4C00D86D9/S144618110000300Xa.pdf/computer_solution_to_the_17point_erdosszekeres_problem.pdf",
        "https://arxiv.org/abs/1604.08657"
      ],
      "verification_cost": "Geometric general-position and convexity checks are low with exact coordinates; upper proof is difficult.",
      "risks": "A lower-bound point set is finite and checkable but does not prove f(k); coordinates may be algebraic and need exact predicates.",
      "recommendation": "后备候选",
      "reason": "Named geometric extremal problem with clear scalar and well-documented historic constructions/proof boundary.",
      "research_origin": "discrete_round2.json",
      "source_id": "happy-ending",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T020",
      "name": "Minimum-dilation triangulation",
      "category": "几何图与计算几何",
      "definition": "For a fixed point set, triangulate it to minimize the maximum ratio of triangulation shortest-path distance to straight-line distance over all point pairs.",
      "solution_format": "triangulation edge list",
      "scalar_objective": "maximum pairwise stretch (dilation)",
      "direction": "minimize",
      "configuration_parameters": "Point set; 2014 library has 210 instances with 10–70 points",
      "human_baseline": "UNICAMP archive provides 210 MDTP instances and results for Brandt, Gaiowski, de Rezende, de Souza (2014). Fekete, Keldenich, Perk (SoCG 2025) give exact algorithms and optimal regular n-gon results through n=100, with methods up to 30,000 points.",
      "primary_sources": [
        "https://www.ic.unicamp.br/~cid/Problem-instances/Dilation/MDTP/index.html",
        "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.48",
        "https://arxiv.org/abs/2502.18189"
      ],
      "verification_cost": "Medium-high; all-pairs paths and accurate sums of radicals.",
      "risks": "Do not assume every instance has certified optimum; use published exact instances/results or compare feasible values with bounds.",
      "recommendation": "MVP候选",
      "reason": "Named task has public instance/results packages, substantial human baseline, natural scalar.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-min-dilation-triangulation",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T021",
      "name": "Minimum-weight triangulation",
      "category": "几何图与计算几何",
      "definition": "Triangulate a fixed planar point set with straight edges minimizing the sum of edge lengths.",
      "solution_format": "triangulation edge list",
      "scalar_objective": "sum of Euclidean edge lengths",
      "direction": "minimize",
      "configuration_parameters": "point set; no Steiner vertices; hull edges included",
      "human_baseline": "Haas (SoCG 2018) reports certified optima on public benchmark classes up to 30 million uniform/normal points, TSPLIB up to 85,900, and VLSI up to 744,710; earlier Beirouti–Snoeyink exact uniform cases reached 80,000. Human algorithmic records; AI use unknown.",
      "primary_sources": [
        "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2018.44",
        "https://arxiv.org/abs/1802.06415",
        "https://arxiv.org/abs/cs/0601002"
      ],
      "verification_cost": "Medium to compute edge sum; global optimum is NP-hard in general.",
      "risks": "Need match a source instance to its solution/certificate. Never use uncertified inner optimum as answer.",
      "recommendation": "后备候选",
      "reason": "Strong natural task and human results, but this pass did not verify a convenient instance/solution archive.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-min-weight-triangulation",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T022",
      "name": "Minimum convex partition of a point set",
      "category": "几何图与计算几何",
      "definition": "给定平面有限点集，在其凸包内构造无交叉直线图，使每个输入点为顶点且每个有界面凸，不允许Steiner点，最小化有界面数。",
      "solution_format": "noncrossing diagonals or convex piece vertex lists",
      "scalar_objective": "number of convex bounded faces",
      "direction": "minimize",
      "configuration_parameters": {
        "point_set": "固定点集实例；退化、共线、允许边界角等遵循CG:SHOP2020规则"
      },
      "human_baseline": "Published exact and integer-programming formulations exist, but a standardized public instance corpus with per-instance human values was not verified in this audit. Baseline unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2020/",
        "https://arxiv.org/abs/2012.07939"
      ],
      "verification_cost": "Low for checking a proposed partition; proving minimum is harder.",
      "risks": "原代理将点集与polygon版本混写；此处固定为CG:SHOP2020点集版本。不能把允许Steiner点、简单polygon最优剖分等不同问题的基线移来。",
      "recommendation": "后备候选",
      "reason": "Natural scalar exists but public baseline and exact formulation need further source audit.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-min-convex-partition",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T023",
      "name": "Minimum coverage by convex polygons (CG:SHOP 2023)",
      "category": "几何图与计算几何",
      "definition": "Cover a given polygonal region with as few convex polygons as possible under the competition’s exact allowed-piece rules.",
      "solution_format": "list of convex polygon pieces",
      "scalar_objective": "number of convex pieces",
      "direction": "minimize",
      "configuration_parameters": "polygon instance and competition constraints; use official 2023 instances",
      "human_baseline": "Official CG:SHOP 2023 challenge archive reports 22 teams and publishes instances/ranking; Copenhagen identifies William Bille Meyling, Mikkel Abrahamsen, André Nusser as first-place team (announced 2023). AI involvement unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2023/",
        "https://barc.ku.dk/news/bachelor-project-at-barc-wins-computational-geometry-challenge/",
        "https://arxiv.org/abs/2303.07007"
      ],
      "verification_cost": "medium; piece validity/coverage and piece-count checking",
      "risks": "Must reproduce challenge’s exact formulation; objective is a computable count but feasible coverage validation should be robust. Do not use count as an inner optimum oracle.",
      "recommendation": "后备候选",
      "reason": "Public benchmark, official human leaderboard, and an intrinsic integer scalar objective.",
      "research_origin": "geometry.json",
      "source_id": "geo-minimum-convex-cover",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T024",
      "name": "Minimum partition into plane subgraphs (CG:SHOP 2022)",
      "category": "几何图与计算几何",
      "definition": "Partition a geometric graph into the minimum number of planar subgraphs under the official challenge’s edge/vertex rules.",
      "solution_format": "color or partition of input edges into planar classes",
      "scalar_objective": "number of parts/colors",
      "direction": "minimize",
      "configuration_parameters": "official CG:SHOP 2022 graph instances and rule set",
      "human_baseline": "Official CG:SHOP archive states this was the 2022 task; teams published algorithm/ranking materials (e.g. Crombez et al. Shadoks approach). AI involvement unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2022/",
        "https://pageperso.lis-lab.fr/guilherme.fonseca/CGSHOP22slides.pdf"
      ],
      "verification_cost": "medium; crossing checks per part",
      "risks": "Exact task formalization and leaderboard records need confirmation; scalar optimum is hard, score feasible partition’s part count only.",
      "recommendation": "后备候选",
      "reason": "Credible competition task and natural objective, but exact primary-result source and instance scorer need audit.",
      "research_origin": "geometry.json",
      "source_id": "geo-min-partition-plane-subgraphs",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T025",
      "name": "Minimum non-obtuse triangulation (CG:SHOP 2025)",
      "category": "几何图与计算几何",
      "definition": "Triangulate an input point set / polygon with all triangles non-obtuse and minimize the competition-defined triangulation size.",
      "solution_format": "triangle vertex triples",
      "scalar_objective": "number of triangles or Steiner vertices as specified by challenge",
      "direction": "minimize",
      "configuration_parameters": "official CG:SHOP 2025 instances and the precise challenge objective",
      "human_baseline": "A challenge paper is published as ‘Minimum Non-Obtuse Triangulations: The CG:SHOP Challenge 2025’; official CG:SHOP archive should contain results and instances. Specific winners/scores not verified in this audit; AI involvement unknown.",
      "primary_sources": [
        "https://arxiv.org/abs/2504.04412",
        "https://cgshop.ibr.cs.tu-bs.de/"
      ],
      "verification_cost": "medium; angle and triangulation checks",
      "risks": "The competition objective may include Steiner points or other penalties; not admissible until precise scalar and human ranking are independently checked.",
      "recommendation": "后备候选",
      "reason": "Named recent contest problem, but exact objective and human baseline facts remain incomplete.",
      "research_origin": "geometry.json",
      "source_id": "geo-min-nonobtuse-triangulation",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T026",
      "name": "Minimum-area simple polygonalization",
      "category": "几何图与计算几何",
      "definition": "Given a planar point set, choose a simple polygon whose vertex set is exactly the input and minimize its area.",
      "solution_format": "cyclic permutation of point indices",
      "scalar_objective": "polygon area",
      "direction": "minimize",
      "configuration_parameters": "input point set; source datasets FHKPS and GEN; point count fixed per instance",
      "human_baseline": "CG:SHOP 2019 produced a ranking and multiple published teams/algorithms; CG challenge paper (Demaine, Fekete, Keldenich, Krupke, Mitchell, 2022) documents it. Public benchmark site has instance/solution and result files. AI involvement unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2019/",
        "https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Poly/",
        "https://doi.org/10.1145/3504000"
      ],
      "verification_cost": "low; simple polygon check and shoelace area exact for rational input",
      "risks": "NP-hard inner optimum; do not score against purported optimum unless certified. Compare returned polygon’s computable area, or use only benchmark instances with verified optimum values.",
      "recommendation": "后备候选",
      "reason": "Competition gives real human baselines and public data; the scored scalar is the submitted polygon’s directly computable area, not an oracle optimum.",
      "research_origin": "geometry.json",
      "source_id": "geo-area-optimal-polygon-min",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T027",
      "name": "Maximum-area simple polygonalization",
      "category": "几何图与计算几何",
      "definition": "Given a planar point set, choose a simple polygon through every point exactly once that maximizes area.",
      "solution_format": "cyclic permutation of point indices",
      "scalar_objective": "polygon area",
      "direction": "maximize",
      "configuration_parameters": "input point set; FHKPS/GEN benchmark instances",
      "human_baseline": "CG:SHOP 2019 ranking and papers cover Max-Area; public benchmark data includes results and solution permutations. Human team names are available in challenge papers; AI involvement unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2019/",
        "https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Poly/",
        "https://doi.org/10.1145/3504000"
      ],
      "verification_cost": "low; simple polygon validation plus shoelace area",
      "risks": "NP-hard inner optimum. Use objective value of feasible returned polygon; comparing gap requires a valid upper bound, never an unverified optimum.",
      "recommendation": "后备候选",
      "reason": "Public human competition results, concrete solutions, and a directly computed natural scalar.",
      "research_origin": "geometry.json",
      "source_id": "geo-area-optimal-polygon-max",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T028",
      "name": "Rectilinear crossing number of K_n",
      "category": "几何图与计算几何",
      "definition": "Place n points in general position in the plane and minimize the number of crossings in the straight-line drawing of K_n.",
      "solution_format": "Exact coordinates or order type; objective number of crossing edge pairs.",
      "scalar_objective": "number of crossings",
      "direction": "minimize",
      "configuration_parameters": {
        "vertices": "n"
      },
      "human_baseline": "Exact values are known through small orders (K_9=36, K_10=62 and published tables extend further); Ábrego–Fernández-Merchant and collaborators maintain best-known bounds and constructions; all exact statuses must be frozen from the survey.",
      "primary_sources": [
        "https://arxiv.org/abs/cs/0009023",
        "https://www.csun.edu/~sf70713/publications/survey.pdf",
        "https://www.crossingnumbers.org/projects/crossingconstants/rectilinear.php"
      ],
      "verification_cost": "Medium for exact coordinates/order type; proving minimum hard.",
      "risks": "Do not merge with topological crossing number; numerical optimization coordinates need exact orientation tests.",
      "recommendation": "后备候选",
      "reason": "Standard well-defined geometric optimization with published record configurations and scalar objective.",
      "research_origin": "discrete_round2.json",
      "source_id": "rectilinear-crossing-kn",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T029",
      "name": "Erdős maximum unit distances for n planar points",
      "category": "几何图与计算几何",
      "definition": "Maximize the number of unit-distance pairs among n distinct points in the Euclidean plane.",
      "solution_format": "Exact-coordinate point set; objective unit-distance pair count.",
      "scalar_objective": "number of unit-distance pairs",
      "direction": "maximize",
      "configuration_parameters": {
        "points": "n"
      },
      "human_baseline": "Alexeev, Mixon & Parshall (2024/2025) report that for n≤21 their upper bounds match best-known lower bounds and fully enumerate densest unit-distance graphs; exact values are thus recorded through 21. No claim about AI-generated or later constructions is used as human baseline.",
      "primary_sources": [
        "https://arxiv.org/abs/2412.11914"
      ],
      "verification_cost": "Witness edge count is checkable with exact algebraic coordinates; global maximum is hard beyond small n.",
      "risks": "Distinguish exact n≤21 values from open larger n and avoid scoring floating-point near-unit distances; freeze the 2024/2025 paper version and accompanying data.",
      "recommendation": "后备候选",
      "reason": "Strong finite exact table through n=21, but a changing frontier and exact-coordinate validation are material.",
      "research_origin": "discrete_round2.json",
      "source_id": "unit-distance",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T030",
      "name": "Orchard planting / maximum 3-rich lines",
      "category": "几何图与计算几何",
      "definition": "给定N个互异实平面点，最大化恰好包含三个输入点的不同直线数；允许三点共线，不能施加“任意三点不共线”的一般位置条件。",
      "solution_format": "point coordinates and counted lines",
      "scalar_objective": "number of distinct lines containing exactly three input points",
      "direction": "maximize",
      "configuration_parameters": {
        "N": "输入点数",
        "coordinates": "整数、有理或精确代数数表示需固定"
      },
      "human_baseline": "Sloane’s A003035 table gives values (e.g. N=7→6, 11→16, 14→26); cubic-curve constructions by Burr, Grünbaum and Sloane provide explicit examples. 2026 work gives t3(15)=31 and excludes 32 with a certificate. Historical human constructions; newer computational component identified.",
      "primary_sources": [
        "https://arxiv.org/abs/1208.4714",
        "https://oeis.org/A003035"
      ],
      "verification_cost": "Medium; exact collinearity/incidence checks.",
      "risks": "恰好3点的直线不等于所有至少3点的直线；源数据的共线约定必须一致。相等/共线关系需精确谓词。",
      "recommendation": "后备候选",
      "reason": "Named integer optimization and public historical values, but a reusable coordinate record for exact selected N needs audit.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-orchard",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T031",
      "name": "No-three-in-line maximum on an n×n grid",
      "category": "几何图与计算几何",
      "definition": "Select as many lattice points as possible from [n]×[n] with no three collinear.",
      "solution_format": "Grid point list; objective cardinality.",
      "scalar_objective": "number of selected points",
      "direction": "maximize",
      "configuration_parameters": {
        "grid_order": "n"
      },
      "human_baseline": "Dudeney posed the problem; constructions of 2n points are known for many n, but the universal 2n conjecture remains open. Wolfram/House of Graphs style databases list configurations; exact finite maxima are only known for selected small n, so a primary record source must be frozen.",
      "primary_sources": [
        "https://arxiv.org/abs/2209.01447"
      ],
      "verification_cost": "Low for collinearity checks; optimum proof hard.",
      "risks": "Recent preprints and recreational databases may contain construction records without optimality proofs; label upper/lower status carefully.",
      "recommendation": "后备候选",
      "reason": "Clear scalar and established construction tradition, but candidate records need more authoritative curation.",
      "research_origin": "discrete_round2.json",
      "source_id": "no-three-in-line",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T032",
      "name": "Simple perfect squared squares: minimum primitive side at fixed order",
      "category": "铺砌与分割",
      "definition": "固定小正方形数量N，将一个整数边长正方形分割为边长互不相同的小正方形，要求simple、所有边长gcd=1，最小化外框边长。",
      "solution_format": "Bouwkamp code or exact tile placements",
      "scalar_objective": "primitive outer-square side length",
      "direction": "minimize",
      "configuration_parameters": {
        "N": "固定order，例如21校准、55历史构造轨"
      },
      "human_baseline": "Duijvestijn (1978)：N21唯一构造primitive side112，已知最优校准。Squaring.net order55页列 Bernard Moss (2020) side740 的历史构造；本次未下载重算。",
      "primary_sources": [
        "https://www.squaring.net/sq/ss/spss/o21/spsso21.html",
        "https://www.squaring.net/sq/ss/spss/o55/spsso55.html",
        "https://www.squaring.net/downloads/downloads.html~"
      ],
      "verification_cost": "Low-medium; exact integer tiling and distinct sizes; global proof is enumeration-based.",
      "risks": "不是把固定目标最低order21当可持续发现任务；须验证Bouwkamp码、simple条件与gcd；side740仅历史baseline。",
      "recommendation": "MVP候选",
      "reason": "Named dissection, exact natural integer objective, public construction code, proof of minimality.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-perfect-squared-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T033",
      "name": "Mrs. Perkins’s quilt",
      "category": "铺砌与分割",
      "definition": "For fixed n×n square, dissect into the fewest smaller integer-sided squares whose side lengths have gcd 1.",
      "solution_format": "integer square tiling / side lengths and positions",
      "scalar_objective": "number of smaller squares",
      "direction": "minimize",
      "configuration_parameters": "Fix outer side n; integer alignment; tile-side gcd 1",
      "human_baseline": "For n=13, the catalogue gives an optimal 11-square dissection with sides 1,1,2,2,2,3,3,4,6,6,7; no fewer than 11 is possible. Squaring.net lists results through n=120, while warning most later rows are best known rather than proven. Conway, Guy, Gay, Pegg and computer searches are documented.",
      "primary_sources": [
        "https://www.squaring.net/sq/ss/quilts/mrs-perkins-quilts.html",
        "https://mathworld.wolfram.com/MrsPerkinssQuilt.html"
      ],
      "verification_cost": "Low for a proposed tiling/gcd; exact minimality varies by n.",
      "risks": "Use proven n=13 calibration; do not claim later best-known values are optimal.",
      "recommendation": "后备候选",
      "reason": "Explicit human layout, natural integer objective, clear proof status.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-mrs-perkins",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T034",
      "name": "Klarner order of a polyomino",
      "category": "铺砌与分割",
      "definition": "For a fixed polyomino P, find the fewest congruent copies (translations, rotations, reflections allowed) that tile any rectangle.",
      "solution_format": "rectangle dimensions and copy placements",
      "scalar_objective": "minimum number of copies of P",
      "direction": "minimize",
      "configuration_parameters": "fixed polyomino shape; allowed orientations stated",
      "human_baseline": "polyominoes.org lists P-pentomino order 2 and an explicit 2×5 tiling. The Handbook of Discrete and Computational Geometry defines order and records a Y-pentomino’s 5×10 rectangle (10 copies), with results by Klarner and Reid.",
      "primary_sources": [
        "https://polyominoes.org/data/5P",
        "https://www.csun.edu/~ctoth/Handbook/chap14.pdf",
        "https://sicherman.net/mikereid/p5_rect.html"
      ],
      "verification_cost": "Low for a placement; proving no smaller order may require exhaustive search.",
      "risks": "Shape P is an instance parameter; P-pentomino order 2 is trivial. Use only a nontrivial shape with source-supported minimality.",
      "recommendation": "后备候选",
      "reason": "Named scalar problem and constructions exist, but candidate shapes and optimality evidence require selection.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-polyomino-order",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T035",
      "name": "(d,g)-cage order",
      "category": "极值图与超图",
      "definition": "For fixed degree d and girth g, find the smallest order n of a d-regular graph of girth exactly g.",
      "solution_format": "Adjacency list/matrix of a d-regular graph with a verifiable girth certificate; objective is vertex count.",
      "scalar_objective": "number of vertices n",
      "direction": "minimize",
      "configuration_parameters": {
        "degree": "d",
        "girth": "g"
      },
      "human_baseline": "Exoo, Jajcay, Goedgebeur et al. (2025 preprint) improved eleven upper bounds; e.g. n(4,10)≤320. Exoo–Jajcay (2013) survey distinguishes known cages from upper-bound constructions; optimality is proved only for some parameter pairs.",
      "primary_sources": [
        "https://arxiv.org/abs/2511.07247",
        "https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS16"
      ],
      "verification_cost": "Medium for a supplied graph; high to prove global minimality.",
      "risks": "Report incumbent order separately from proven minimum; exact optimality certificates are often absent.",
      "recommendation": "后备候选",
      "reason": "Natural scalar objective, rich named record tables, and independently checkable graph witnesses.",
      "research_origin": "discrete.json",
      "source_id": "graph-cage",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T036",
      "name": "Degree–diameter problem",
      "category": "极值图与超图",
      "definition": "For maximum degree d and diameter k, maximize the order of a simple graph.",
      "solution_format": "Graph adjacency list plus proof/check of maximum degree and diameter; objective vertex count.",
      "scalar_objective": "number of vertices n",
      "direction": "maximize",
      "configuration_parameters": {
        "maximum_degree": "d",
        "diameter": "k"
      },
      "human_baseline": "The large degree/diameter graph table (Miller, Širáň and contributors; updated tables) records best known orders and marks the few proven optimal cases; Moore bound is an upper bound, not an attained baseline.",
      "primary_sources": [
        "https://doi.org/10.17632/d75dzbjd4k.3"
      ],
      "verification_cost": "Medium for witness; exact optimum usually unknown.",
      "risks": "Must label best-known vs proven; table updates and graph conventions (regular vs maximum degree) need freezing.",
      "recommendation": "后备候选",
      "reason": "A clear extremal objective and extensive human constructions; feasible to score witness size.",
      "research_origin": "discrete.json",
      "source_id": "degree-diameter",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T037",
      "name": "Zarankiewicz number Z_{s,t}(m,n)",
      "category": "极值图与超图",
      "definition": "固定左右部大小m,n，构造二部图，禁止存在s个左顶点与t个右顶点形成完整二部子图，最大化边数。若同时禁止交换角色的情形，须单列配置。",
      "solution_format": "Bipartite adjacency matrix; objective number of 1 entries.",
      "scalar_objective": "number of edges",
      "direction": "maximize",
      "configuration_parameters": {
        "part_sizes": "m,n",
        "forbidden_biclique": "s,t"
      },
      "human_baseline": "Published exact values and bounds are surveyed in the extremal graph literature; small square cases have SAT-verified tables (Mubayi et al. / 2022 SAT study corrects known table errors). Explicit finite-field constructions give human lower bounds.",
      "primary_sources": [
        "https://arxiv.org/abs/2203.02283",
        "https://arxiv.org/abs/2202.05507",
        "https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/BGKRSW96/bgkrsw96.pdf"
      ],
      "verification_cost": "Medium for forbidden biclique and edge count; optimality high.",
      "risks": "Older tables contain errors; pin a source version and instance. General asymptotics remain open.",
      "recommendation": "后备候选",
      "reason": "Clean extremal scalar, abundant constructions, and small instances admit exact machine checks.",
      "research_origin": "discrete.json",
      "source_id": "zaran-bipartite",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T038",
      "name": "Forbidden-subgraph extremal number ex(n,F)",
      "definition": "固定 n 与有限禁止图族 F，构造 F-free 简单图。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "number of edges",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "顶点数",
        "F": "例如 {C4} 或 {C3,C4}，作为配置"
      },
      "human_baseline": "Afzaly–McKay 公开 sparse6 构造表：ex(10,C4)=16；禁止 C3,C4 时 n=10 的构造为15条边。较大行区分最优与仅下界。",
      "primary_sources": [
        "https://users.cecs.anu.edu.au/~bdm/data/extremal.html"
      ],
      "verification_cost": "低至中；固定小 F 的子图检查。",
      "risks": "高阶 F 或很大 n 会使验证昂贵；Zarankiewicz 的二部限制与此相关，按族分层汇总。",
      "recommendation": "MVP候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-forbidden-graph",
      "category": "极值图与超图",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T039",
      "name": "Graph saturation number sat(n,F)",
      "category": "极值图与超图",
      "definition": "Minimize edges in an n-vertex F-saturated graph: it is F-free, but adding any missing edge creates F.",
      "solution_format": "Graph adjacency list; objective edge count.",
      "scalar_objective": "number of edges",
      "direction": "minimize",
      "configuration_parameters": {
        "vertices": "n",
        "forbidden_graph": "F"
      },
      "human_baseline": "Bollobás (1965) initiated the problem; for cliques, classical constructions and recent papers give exact formulas for many ranges. Current papers state the standard definition and bounds.",
      "primary_sources": [
        "https://arxiv.org/abs/2605.07179"
      ],
      "verification_cost": "Medium for candidate; exact optimum often requires proof.",
      "risks": "Newer specific F parameter results must be checked against publication status; easy families have formulaic answers.",
      "recommendation": "后备候选",
      "reason": "Natural minimization objective with established theory; curate a small frozen set of nontrivial F,n cases.",
      "research_origin": "discrete.json",
      "source_id": "saturation",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T040",
      "name": "Classical Ramsey number lower-bound construction",
      "category": "极值图与超图",
      "definition": "For fixed s,t, construct the largest N-vertex graph with neither an s-clique nor an independent t-set, equivalently improve the lower bound R(s,t)≥N+1.",
      "solution_format": "Graph adjacency list; independently verify forbidden-clique/independent-set conditions; scalar N.",
      "scalar_objective": "number of vertices N",
      "direction": "maximize",
      "configuration_parameters": {
        "s,t": "禁止clique与independent set大小；图Ramsey扩展另作为有关联配置，不重复立项"
      },
      "human_baseline": "Exoo et al. (1997) catalogued 656 nonisomorphic (5,5,42)-graphs, implying R(5,5)≥43; Radziszowski Dynamic Survey rev. 18 (2026) records 43≤R(5,5)≤46, with the upper bound by Angeltveit–McKay (2024).",
      "primary_sources": [
        "https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf",
        "https://users.cecs.anu.edu.au/~bdm/data/ramsey.html",
        "https://arxiv.org/abs/2409.15709"
      ],
      "verification_cost": "High; exact clique and independence checks scale exponentially, though certificates are finite and reproducible.",
      "risks": "A one-unit increase is meaningful but only if exact validation is performed; do not score heuristic estimates or claim exact Ramsey values from a lower-bound witness.",
      "recommendation": "后备候选",
      "reason": "Excellent human baseline and natural scalar, but restrict to modest s,t and require exact verifier/certificate.",
      "research_origin": "discrete.json",
      "source_id": "classical-ramsey",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T041",
      "name": "Hypergraph Turán number ex_r(n,F)",
      "category": "极值图与超图",
      "definition": "Maximize edges in an r-uniform n-vertex hypergraph avoiding a fixed forbidden r-graph F.",
      "solution_format": "List of r-subsets; objective edge count.",
      "scalar_objective": "number of hyperedges",
      "direction": "maximize",
      "configuration_parameters": {
        "uniformity": "r",
        "vertices": "n",
        "forbidden_hypergraph": "F"
      },
      "human_baseline": "Keevash's survey and the Erdős problems archive record open cases and constructions. The 3-uniform K4 problem has Turán's construction at density 5/9, but exact density remains open; finite n entries can have exact/conjectured distinctions.",
      "primary_sources": [
        "https://people.maths.ox.ac.uk/keevash/papers/turan-survey.pdf",
        "https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/ExactHypergraphTuranT3n4.html"
      ],
      "verification_cost": "High; checking F-freeness is manageable for small n, global optimality is difficult.",
      "risks": "Do not blur finite exact values with asymptotic Turán density; choose frozen small n and explicit F.",
      "recommendation": "后备候选",
      "reason": "Canonical research problem with natural edge-count objective and published constructions/bounds.",
      "research_origin": "discrete.json",
      "source_id": "turan-hypergraph",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T042",
      "name": "Erdős–Rogers function f_{s,t}(n)",
      "category": "极值图与超图",
      "definition": "固定2≤s<t与n，在n顶点K_t-free图G中，最小化α_s(G)，其中α_s(G)是G中诱导子图不含K_s的最大顶点集大小。s=2时α_2是独立数。",
      "solution_format": "图G；有限小规模下由独立精确算法计算α_s，或提交相应可检查证书。",
      "scalar_objective": "α_s(G)=max{|U|:G[U] is K_s-free}",
      "direction": "minimize",
      "configuration_parameters": {
        "vertices": "n",
        "forbidden_clique": "s",
        "independent_set_forbidden_size": "t (target alpha < t)"
      },
      "human_baseline": "Erdős–Rogers introduced the function; extensive probabilistic and explicit bounds are surveyed in recent graph Ramsey literature. Specific finite graph records need source-level validation before use.",
      "primary_sources": [
        "https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf"
      ],
      "verification_cost": "高：内层最大子集问题通常指数复杂；仅限能精确求解的小配置，不进MVP。",
      "risks": "原代理误写为K_s-free图上最大独立数（空图平凡达到n），此处已修为标准Erdős–Rogers最小化问题；须同时验证K_t-free与内层α_s。",
      "recommendation": "后备候选",
      "reason": "A recognized graph extremal function with natural scalar, but poor witness-only evaluation and no curated finite database confirmed.",
      "research_origin": "discrete_round2.json",
      "source_id": "erdos-rogers",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T043",
      "name": "Minimum triangles at fixed edge count",
      "definition": "固定 n,m，输出恰有 m 条边的简单图，使三角形数最少。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "triangle count",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "顶点数",
        "m": "边数"
      },
      "human_baseline": "Razborov (2008) 的三角形密度定理及 Lovász–Simonovits 构造提供经典基线；非平凡有限 n,m 的显式构造与可达边数须逐项固定。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/46.html",
        "https://people.cs.uchicago.edu/~razborov/files/triangles.pdf"
      ],
      "verification_cost": "低：精确数三角形。",
      "risks": "渐近最优密度不是每个有限配置的最优值；不得用 asymptotic 数字冒充精确基线。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-min-triangles",
      "category": "极值图与超图",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T044",
      "name": "Optimal Golomb ruler length",
      "category": "加法组合与离散构造",
      "definition": "For m integer marks, place distinct marks so all positive pairwise differences are distinct and minimize the largest mark.",
      "solution_format": "Increasing integer mark list starting at 0; objective final mark.",
      "scalar_objective": "ruler length",
      "direction": "minimize",
      "configuration_parameters": {
        "marks": "m"
      },
      "human_baseline": "Shearer (1990) exhaustively proved optimal lengths 127,151,177 for m=14,15,16; distributed.net completed proof of optimality through m=28 (2022 records), and CSPLib has the standard benchmark. Distinguish proven optima from larger-m best known rulers.",
      "primary_sources": [
        "https://research.ibm.com/publications/some-new-optimum-golomb-rulers",
        "https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob006/",
        "https://distributed.net/ogr/"
      ],
      "verification_cost": "Low for ruler; optimality proof high for large m.",
      "risks": "Open sizes beyond proven range must be scored as incumbent length, not as proven optimum; preserve provenance and certificate status.",
      "recommendation": "MVP候选",
      "reason": "Ideal scalar objective, a standard benchmark and exceptionally clear historical human record.",
      "research_origin": "discrete.json",
      "source_id": "golomb-ruler",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T045",
      "name": "Minimum diameter of a B_h set of integers, h≥3",
      "category": "加法组合与离散构造",
      "definition": "For fixed m and h≥3, choose m integers with all h-term sums (repetition convention fixed) distinct, minimizing the diameter.",
      "solution_format": "Sorted integer set; objective maximum minus minimum.",
      "scalar_objective": "diameter",
      "direction": "minimize",
      "configuration_parameters": {
        "set_size": "m",
        "sum order": "h≥3",
        "repetitions": "fixed by benchmark"
      },
      "human_baseline": "Bose–Chowla (1962) give finite-field B_h constructions; modern additive-combinatorics papers provide bounds. The h=2 case is the Golomb/Sidon ruler task and is deliberately excluded here as a duplicate.",
      "primary_sources": [
        "https://doi.org/10.1007/BF02566968",
        "https://arxiv.org/abs/2104.12711"
      ],
      "verification_cost": "Low for witness; exact optimum difficult.",
      "risks": "Must distinguish unordered multisets with repetitions from distinct-element sums and from modular B_h sets; h=2 merges with Golomb rulers.",
      "recommendation": "后备候选",
      "reason": "Natural generalization with human algebraic constructions; finite exact baselines need dedicated verification.",
      "research_origin": "discrete_round2.json",
      "source_id": "bh-ruler-higher",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T046",
      "name": "Difference triangle sets",
      "category": "加法组合与离散构造",
      "definition": "Construct several rows of marks with all within-row positive differences distinct globally; minimize maximum span under fixed row/mark counts.",
      "solution_format": "Rows of integer marks; objective maximum row span.",
      "scalar_objective": "maximum span",
      "direction": "minimize",
      "configuration_parameters": {
        "rows": "r",
        "marks_per_row": "m"
      },
      "human_baseline": "Published difference-triangle-set constructions and tabu search literature report best-known spans; Golomb rulers are the one-row special case.",
      "primary_sources": [
        "https://doi.org/10.1016/j.cor.2004.11.002",
        "https://cs.uwaterloo.ca/~vanbeek/Publications/sillito.pdf"
      ],
      "verification_cost": "Low for a witness.",
      "risks": "Overlaps Golomb ruler at r=1; careful definition variants (all differences vs row-tagged) must be frozen.",
      "recommendation": "后备候选",
      "reason": "A legitimate adjacent optimization family with published records, but merge one-row case into Golomb rulers.",
      "research_origin": "discrete.json",
      "source_id": "difference-triangle",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T047",
      "name": "Maximum cap set in F_3^n",
      "category": "加法组合与离散构造",
      "definition": "Find a largest subset of the vector space F_3^n containing no affine line (three distinct points summing to zero).",
      "solution_format": "Point list in F_3^n; objective cardinality.",
      "scalar_objective": "number of points",
      "direction": "maximize",
      "configuration_parameters": {
        "dimension": "n"
      },
      "human_baseline": "Pellegrino (1970) proved maximum 20 for n=4. Kleinberg–Sawin–Speyer (2016) gave constructions and Ellenberg–Gijswijt (2017) exponential upper bound; human lower-bound records are published for higher n, with exact values limited.",
      "primary_sources": [
        "https://doi.org/10.4007/annals.2017.185.1.8",
        "https://arxiv.org/abs/1605.09223"
      ],
      "verification_cost": "Low for witness and no-line property; proving optimality difficult.",
      "risks": "Modern record tables may have changed; distinguish exact small dimensions from best-known lower bounds.",
      "recommendation": "后备候选",
      "reason": "Canonical additive extremal problem, clear point-count objective, and unusually visible human construction frontier.",
      "research_origin": "discrete.json",
      "source_id": "cap-set",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T048",
      "name": "Largest 3-term-progression-free subset of [n]",
      "category": "加法组合与离散构造",
      "definition": "Find a largest subset of {1,…,n} containing no nontrivial 3-term arithmetic progression.",
      "solution_format": "Integer set; objective cardinality.",
      "scalar_objective": "set cardinality",
      "direction": "maximize",
      "configuration_parameters": {
        "interval_length": "n"
      },
      "human_baseline": "Behrend (1946) gave classical constructions; exact small-n values are known computationally and Roth's theorem gives qualitative upper bounds. Pin exact-value source/version for each n.",
      "primary_sources": [
        "https://doi.org/10.1073/pnas.32.12.331"
      ],
      "verification_cost": "Low for witness, exponential for maximality.",
      "risks": "Closely related to cap sets but distinct ambient group; avoid treating parameter variants as different tasks.",
      "recommendation": "后备候选",
      "reason": "Natural cardinality objective, but benchmark exact records need authoritative tables and manageable n.",
      "research_origin": "discrete.json",
      "source_id": "progression-free",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T049",
      "name": "Minimum difference basis for [n]",
      "category": "加法组合与离散构造",
      "definition": "Find a smallest set A of integers such that every integer 1,…,n is a difference of two elements of A.",
      "solution_format": "Sorted integer set; objective cardinality (or span if a different canonical version is chosen).",
      "scalar_objective": "number of elements of A",
      "direction": "minimize",
      "configuration_parameters": {
        "target_interval": "n",
        "ambient_domain": "integer interval, fixed convention"
      },
      "human_baseline": "Rédei–Rényi and Leech difference-basis constructions; the prior finite witness at n=6166 has128 marks, giving128²/6166≈2.6571. Original128-element list still needs retrieval; not a same-config value for all n.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/7.html",
        "https://arxiv.org/html/2511.02864v1#S6.SS3"
      ],
      "verification_cost": "Low for coverage; proving minimality difficult.",
      "risks": "Several inequivalent definitions (difference set vs difference basis, interval endpoint, signed differences); human baseline source requires additional research.",
      "recommendation": "后备候选",
      "reason": "Natural minimum-cardinality task but needs definition and authoritative record table curation.",
      "research_origin": "discrete.json",
      "source_id": "difference-basis",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T050",
      "name": "Maximum sum-free subset of a finite group",
      "category": "加法组合与离散构造",
      "definition": "Maximize |A| in a fixed finite abelian group subject to no x,y,z∈A with x+y=z (convention fixed).",
      "solution_format": "Element list; objective cardinality.",
      "scalar_objective": "set cardinality",
      "direction": "maximize",
      "configuration_parameters": {
        "group": "fixed finite abelian group"
      },
      "human_baseline": "For integers [n], the maximum is floor((n+1)/2), giving an exact calibration; finite group extremal classifications are known in many cases.",
      "primary_sources": [
        "https://doi.org/10.3792/pja/1195520891",
        "https://doi.org/10.1112/jlms/s1-44.1.131"
      ],
      "verification_cost": "Low for witness, exact optimum varies.",
      "risks": "Integer interval is formulaic; broad finite-group versions need more specific literature and are not one task.",
      "recommendation": "删除：整个任务已解",
      "reason": "Useful calibration only for interval case; broader version lacks canonical benchmark instances.",
      "research_origin": "discrete.json",
      "source_id": "sum-free",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "当前定义为有限阿贝尔群；Green–Ruzsa已确定每个有限阿贝尔群的最大sum-free子集大小。",
      "discovery_entry_status": "excluded_closed_task"
    },
    {
      "id": "T051",
      "name": "Schur number S(k) lower-bound coloring",
      "category": "加法组合与离散构造",
      "definition": "For fixed k colors, construct a coloring of [N] with no monochromatic x+y=z; maximize N, the certified lower bound for S(k).",
      "solution_format": "Color assignment [N]→[k] with exact check of all x+y=z; scalar N.",
      "scalar_objective": "largest colorable N",
      "direction": "maximize",
      "configuration_parameters": {
        "colors": "k"
      },
      "human_baseline": "Heule (AAAI 2018) proved S(5)=160 using a DRAT-certified SAT computation; S(6)≥536 and S(7)≥1680 are cited constructions by Fredricksen–Sweet (2000). Schur numbers S(1..4)=1,4,13,44 are exact.",
      "primary_sources": [
        "https://ojs.aaai.org/index.php/AAAI/article/download/12209/12068",
        "https://www.cs.utexas.edu/~marijn/Schur/"
      ],
      "verification_cost": "Low for lower-bound coloring; proving exact value needs a large SAT/DRAT proof.",
      "risks": "Score a coloring's N only, not an exact S(k) claim absent an upper proof; weak Schur numbers are a separate convention and should be excluded/merged only by explicit scope.",
      "recommendation": "后备候选",
      "reason": "Canonical extremal coloring task with explicit human witnesses, exact small values, and strong proof artifacts.",
      "research_origin": "discrete_round2.json",
      "source_id": "schur-number",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T052",
      "name": "van der Waerden number lower-bound coloring",
      "category": "加法组合与离散构造",
      "definition": "For fixed r colors and AP length k, construct the longest r-coloring of [N] with no monochromatic k-term arithmetic progression.",
      "solution_format": "Coloring of [N]; scalar N.",
      "scalar_objective": "largest AP-free coloring order N",
      "direction": "maximize",
      "configuration_parameters": {
        "colors": "r",
        "progression_length": "k"
      },
      "human_baseline": "Marijn Heule's 2005 EJC survey/paper tables W(2,5)=178, W(2,6)=1132 and many best known lower-bound colorings; Berlekamp (1968) and later recurrence constructions provide explicit records.",
      "primary_sources": [
        "https://www.cs.utexas.edu/~marijn/publications/waerden.pdf",
        "https://arxiv.org/abs/1705.09673",
        "https://www.combinatorics.org/ojs/index.php/eljc/article/view/v18i1p64"
      ],
      "verification_cost": "Low for a coloring witness by enumerating arithmetic progressions; upper/exact proof is costly.",
      "risks": "Closely related to Ramsey lower-bound construction but a distinct named AP-avoidance family; freeze coloring convention and don't label lower bounds as exact W(r,k).",
      "recommendation": "后备候选",
      "reason": "Natural construction objective with published numerical records and cheap witness validation.",
      "research_origin": "discrete_round2.json",
      "source_id": "van-der-waerden-lower",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T053",
      "name": "Longest finite sequence with discrepancy at most C",
      "category": "加法组合与离散构造",
      "definition": "For a fixed discrepancy cap C, find the largest prefix length N of a ±1 sequence such that every homogeneous initial segment along every arithmetic progression has absolute sum at most C.",
      "solution_format": "Sign sequence of length N; exact scalar N.",
      "scalar_objective": "sequence length N",
      "direction": "maximize",
      "configuration_parameters": {
        "discrepancy_cap": "C"
      },
      "human_baseline": "Konev–Lisitsa (2015) reported a discrepancy-3 sequence of length 127,645, improving 17,000, with inductive construction rules; Tao (2015) proved the infinite Erdős discrepancy conjecture.",
      "primary_sources": [
        "https://arxiv.org/abs/1407.2510",
        "https://arxiv.org/abs/1509.05363"
      ],
      "verification_cost": "Low for a supplied finite sequence; proving maximality requires exhaustive/combinatorial upper certificates.",
      "risks": "The unbounded infinite theorem itself is not a finite optimization task; freeze exact prefix discrepancy convention and evaluate witness length only.",
      "recommendation": "后备候选",
      "reason": "A named finite extremal version has a concrete human record and exact scalar witness.",
      "research_origin": "discrete_round2.json",
      "source_id": "erdos-discrepancy-finite",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T054",
      "name": "Largest square-difference-free subset of [N]",
      "category": "加法组合与离散构造",
      "definition": "Maximize |A| for A⊂[N] with no distinct a,b∈A such that |a−b| is a perfect square.",
      "solution_format": "Integer set; objective cardinality.",
      "scalar_objective": "number of elements",
      "direction": "maximize",
      "configuration_parameters": {
        "interval_length": "N"
      },
      "human_baseline": "Ruzsa (1984) gave an explicit construction of square-difference-free sets; Green–Sawhney (preprint 2024, updated 2025) prove |A|≪N exp(−c√log N). These are asymptotic bounds, not exact finite-N maxima.",
      "primary_sources": [
        "https://doi.org/10.1007/BF02454169",
        "https://arxiv.org/abs/2411.17448"
      ],
      "verification_cost": "Low for a finite set; proof of maximum difficult.",
      "risks": "Asymptotic rather than exact finite record frontier; parameters N give highly correlated instances.",
      "recommendation": "后备候选",
      "reason": "Strong named extremal family and human constructions, but current upper-bound citation needs verification and finite record table.",
      "research_origin": "discrete_round2.json",
      "source_id": "furstenberg-sarkozy",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T055",
      "name": "Finite-set sum–product growth minimization",
      "category": "加法组合与离散构造",
      "definition": "固定集合大小m与环境环R（有限域F_p或有坐标界的整数），构造A⊂R、|A|=m，最小化max(|A+A|,|A·A|)。",
      "solution_format": "Finite integer set A; objective the larger of sumset/product-set cardinalities.",
      "scalar_objective": "max(|A+A|,|A·A|)",
      "direction": "minimize",
      "configuration_parameters": {
        "m": "集合大小",
        "R": "F_p及素数p，或整数及坐标上界B"
      },
      "human_baseline": "Erdős–Szemerédi (1983) established a power-growth theorem for integer sets; later Solymosi and others improve exponents. No canonical exact finite-n construction table for this min-max objective was verified in this pass.",
      "primary_sources": [
        "https://annals.math.princeton.edu/2003/157-3/p07",
        "https://arxiv.org/abs/math/0402285",
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/45.html"
      ],
      "verification_cost": "Low for a finite set and exact integer operations; global optimum hard.",
      "risks": "Integer interval bound B affects the problem substantially and may be artificial; no verified human optimum table. Restrict to conditional exploratory instances only.",
      "recommendation": "后备候选",
      "reason": "A real finite optimization scalar, but a standardized published finite benchmark frontier was not confirmed.",
      "research_origin": "discrete_round2.json",
      "source_id": "sum-product-growth",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T056",
      "name": "Minimum finite-field Kakeya set size",
      "category": "加法组合与离散构造",
      "definition": "For fixed finite field F_q and dimension d, minimize |K| over K⊂F_q^d containing a full affine line in every direction.",
      "solution_format": "Point list or characteristic function; objective |K|.",
      "scalar_objective": "number of points",
      "direction": "minimize",
      "configuration_parameters": {
        "field_order": "q",
        "dimension": "d"
      },
      "human_baseline": "Dvir (2009) proved |K|≥c_d q^d by the polynomial method; explicit constructions are known. An October 2026 exposition reports an exact exhaustive result |K|=13 for F_3^3, but that source is secondary, so require primary-paper confirmation before adopting this numeric record.",
      "primary_sources": [
        "https://arxiv.org/abs/0803.2336",
        "https://arxiv.org/abs/1503.06639"
      ],
      "verification_cost": "Low for candidate set; exact minimum needs exhaustive or mathematical lower bound.",
      "risks": "Small finite cases and field characteristic matter; separate proven minimum from construction upper bound; record 2026 claim as pending primary confirmation.",
      "recommendation": "后备候选",
      "reason": "Natural finite extremal objective with strong theory, but exact record data are currently thin.",
      "research_origin": "discrete_round2.json",
      "source_id": "finite-kakeya",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T057",
      "name": "Sum–difference I: normalized logarithmic ratio",
      "definition": "输出至少两个不同整数组成的集合 A；计算其和集与差集。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "log(|A+A|/|A|)/log(|A-A|/|A|)",
      "direction": "maximize",
      "configuration_parameters": {
        "cardinality": "固定上限，如512；不是把固定17元素改作上限512",
        "integer_range": "如[-10^6,10^6]"
      },
      "human_baseline": "Pigarev–Freiman 的17元构造在 Martin–O'Bryant (2006/2007) 中重列；|A+A|=59、|A-A|=55，score=1.0597930945472454；本次已独立重算。",
      "primary_sources": [
        "https://personal.math.ubc.ca/~gerg/papers/downloads/MSHMSTD.pdf",
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/42.html"
      ],
      "verification_cost": "低：O(|A|²) 整数集合运算。",
      "risks": "该历史人类构造不是2026世界纪录；与II/III分母不同。新的含AI论文另列。",
      "recommendation": "MVP候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-sumdiff-I",
      "category": "加法组合与离散构造",
      "publication_status": "candidate_only",
      "baseline_audit": "example_witness_recomputed_not_full_task_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T058",
      "name": "Sum–difference II: unnormalized logarithmic ratio",
      "definition": "输出有限整数集 A，优化差集大小相对和集大小的指数。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "log(|A-A|)/log(|A+A|)",
      "direction": "maximize",
      "configuration_parameters": {
        "size_bound": "有限大小/坐标界需固定"
      },
      "human_baseline": "人类高维非负整数 simplex 构造给出渐近指数 log(1+sqrt(2))/log(2)≈1.27155；明确有限维实例须用足够大的进制嵌入整数并精确计分。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/43.html",
        "https://arxiv.org/html/2511.02864v1#S6.SS25"
      ],
      "verification_cost": "低至中：有限输出时计和集差集。",
      "risks": "渐近常数不是任意有限配置的可达baseline；有限实例尚待固定。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-sumdiff-II",
      "category": "加法组合与离散构造",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T059",
      "name": "Sum–difference III: finite certificate for asymptotic exponent",
      "definition": "输出含0的非负整数集 U，满足 Gyarmati–Hennecart–Ruzsa 有限证书定理的条件，用其证明渐近指数下界。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "1+log(|U-U|/|U+U|)/log(2 max(U)+1)",
      "direction": "maximize",
      "configuration_parameters": {
        "integer_bound": "max U 上限",
        "size_bound": "显式输出规模上限"
      },
      "human_baseline": "Gyarmati–Hennecart–Ruzsa (2007)：U={0,1,3,6,13,17,21}，和集26、差集39、q=43，score=1.107802056693651；本次已重算有限表达式。",
      "primary_sources": [
        "https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf",
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/44.html"
      ],
      "verification_cost": "低：整数集合运算。",
      "risks": "必须验证原证书条件（严格 |U-U|<2maxU+1 等）；后续1.14465等大构造不可直接当小配置baseline。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-sumdiff-III",
      "category": "加法组合与离散构造",
      "publication_status": "candidate_only",
      "baseline_audit": "example_witness_recomputed_not_full_task_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T060",
      "name": "Covering number C(v,k,t)",
      "category": "组合设计",
      "definition": "Find the fewest k-subsets of a v-set such that every t-subset is included in at least one selected block.",
      "solution_format": "List of k-subsets; objective block count.",
      "scalar_objective": "number of blocks",
      "direction": "minimize",
      "configuration_parameters": {
        "v": "points",
        "k": "block size",
        "t": "covering strength"
      },
      "human_baseline": "La Jolla Combinatorics Repository (Dan Gordon; frozen 2026) stores tens of thousands of best-known covers and lower bounds; individual construction records identify contributors/methods.",
      "primary_sources": [
        "https://dmgordon.org/ljcr/",
        "https://ljcr.dmgordon.org/cover.html"
      ],
      "verification_cost": "Low-medium for coverage; proving minimum needs lower bound.",
      "risks": "Repository baseline may be best-known rather than optimum; freeze data snapshot and preserve authorship metadata.",
      "recommendation": "MVP候选",
      "reason": "One of the strongest candidates: standardized finite objects, natural scalar, and large human record corpus.",
      "research_origin": "discrete.json",
      "source_id": "covering-design",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T061",
      "name": "Covering array CAN(t,k,v)",
      "category": "组合设计",
      "definition": "Minimize rows N of a k-column v-ary array so every t selected columns contain every v^t tuple at least once.",
      "solution_format": "N×k array over v symbols; objective N.",
      "scalar_objective": "number of rows N",
      "direction": "minimize",
      "configuration_parameters": {
        "strength": "t",
        "columns": "k",
        "levels": "v"
      },
      "human_baseline": "NIST Covering Array Library lists actual arrays for strengths 2–6 and 2–6 levels, plus best-known sizes to 20,000 columns (strength 2) and 10,000 (strengths 3–6); NIST and Colbourn records are human constructions/bounds.",
      "primary_sources": [
        "https://csrc.nist.gov/Projects/Automated-Combinatorial-Testing-for-Software/Covering-Array-Library",
        "https://math.nist.gov/coveringarrays/coveringarray.html"
      ],
      "verification_cost": "Low for explicit array; minimum proof varies.",
      "risks": "Keep uniform alphabet case separate from variable-strength/general mixed-level variants; NIST best-known size tables do not always include arrays.",
      "recommendation": "MVP候选",
      "reason": "Excellent benchmark corpus and easily verifiable scalar optimization.",
      "research_origin": "discrete.json",
      "source_id": "covering-array",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T062",
      "name": "Orthogonal array minimum-run construction",
      "category": "组合设计",
      "definition": "For fixed strength t, levels and columns, construct an orthogonal array with the fewest rows (or maximize columns for fixed rows), each t-column tuple appearing equally often.",
      "solution_format": "Array with explicit index lambda; objective rows or columns, with one direction fixed per instance.",
      "scalar_objective": "number of rows N; λ=N/q^t is variable",
      "direction": "minimize",
      "configuration_parameters": {
        "t": "强度",
        "q": "字母表大小",
        "k": "列数；index λ不固定，随行数N优化"
      },
      "human_baseline": "Neil Sloane's library contains 200+ explicit arrays; Eendebak–Schoen catalogue complete non-isomorphic arrays for selected small parameters. OA( N,k,s,t) must meet divisibility/Rao bounds.",
      "primary_sources": [
        "https://neilsloane.com/oadir/index.html"
      ],
      "verification_cost": "Low for explicit array; minimality moderate/high.",
      "risks": "Do not conflate OA existence, maximum columns, and minimum-run objectives; fix one scalar per instance. Strength-2 binary OAs are essentially Hadamard matrices.",
      "recommendation": "后备候选",
      "reason": "Curated human constructions and simple exact validator; good if objective/configuration are fixed consistently.",
      "research_origin": "discrete.json",
      "source_id": "orthogonal-array",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T063",
      "name": "Packing number D(v,k,t)",
      "category": "组合设计",
      "definition": "Maximize the number of k-subsets on v points such that no t-subset is contained in more than one block.",
      "solution_format": "List of blocks; objective block count.",
      "scalar_objective": "number of blocks",
      "direction": "maximize",
      "configuration_parameters": {
        "v": "points",
        "k": "block size",
        "t": "packing strength"
      },
      "human_baseline": "La Jolla covering repository focuses on coverings, while classical packing bounds and constructions are published; candidate instance-level records require dedicated database/source review.",
      "primary_sources": [
        "https://dmgordon.org/ljcr/"
      ],
      "verification_cost": "Low for packing property.",
      "risks": "No unified current record table confirmed in this pass; may overlap partial Steiner designs.",
      "recommendation": "后备候选",
      "reason": "Good scalar and verification, but human-record baseline needs further curation.",
      "research_origin": "discrete.json",
      "source_id": "packing-design",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T064",
      "name": "Social golfer maximum schedule length",
      "category": "组合设计",
      "definition": "Partition players into groups of fixed size each round, avoiding any pair meeting twice; maximize number of rounds.",
      "solution_format": "Round-by-round partitions; objective number of rounds.",
      "scalar_objective": "number of rounds",
      "direction": "maximize",
      "configuration_parameters": {
        "players": "P",
        "group_size": "g",
        "groups_per_round": "fixed/implied"
      },
      "human_baseline": "CSPLib problem 010 defines the canonical 32 golfers in groups of four and its generalization; published constraint-programming literature reports solved/optimal schedules for small parameter sets, but benchmark records need per-instance capture.",
      "primary_sources": [
        "https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob010/",
        "https://www.csplib.org/Problems/prob010/"
      ],
      "verification_cost": "Low for pair uniqueness; maximality requires a bound/proof.",
      "risks": "Could degenerate into mere feasibility when target rounds fixed; use maximize rounds and instances with documented human optima.",
      "recommendation": "后备候选",
      "reason": "Natural schedule objective and benchmark tradition, but require verified per-instance baseline.",
      "research_origin": "discrete.json",
      "source_id": "social-golfer",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T065",
      "name": "Maximum number of mutually orthogonal Latin squares",
      "category": "组合设计",
      "definition": "For order n, maximize the number of pairwise orthogonal Latin squares (MOLS).",
      "solution_format": "List of Latin squares; objective count.",
      "scalar_objective": "number of MOLS",
      "direction": "maximize",
      "configuration_parameters": {
        "order": "n"
      },
      "human_baseline": "Bruck–Ryser–Chowla gives nonexistence restrictions; complete values are known for several small orders, while the standard MOLS tables record constructions and bounds.",
      "primary_sources": [
        "https://doi.org/10.1016/0012-365X(74)90148-4",
        "https://www.dcs.gla.ac.uk/~pat/cpM/jchoco/latinSquares/papers/10%5B1%5D.1.1.49.7739.pdf"
      ],
      "verification_cost": "Low for square/orthogonality checks; maximality often hard.",
      "risks": "Exact optimum open for some n; source table version and proof status must be frozen.",
      "recommendation": "后备候选",
      "reason": "Canonical extremal design quantity, simple verifier, and substantive human theory.",
      "research_origin": "discrete.json",
      "source_id": "latin-mols",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T066",
      "name": "Best minimum distance of linear codes",
      "category": "编码理论",
      "definition": "For fixed (n,k,q), construct a q-ary linear [n,k] code with maximum minimum Hamming distance d.",
      "solution_format": "Generator matrix over GF(q), with independently checked rank and minimum distance.",
      "scalar_objective": "Minimum Hamming distance d(C)",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "block length",
        "k": "dimension",
        "q": "finite-field order; use distinct benchmark rows, not one task per q/n"
      },
      "human_baseline": "Human-computed database: Markus Grassl, John Cannon and Greg White's Magma BKLC tables; Magma reports 33,152 best-known binary codes, all binary entries through n=31 optimal. Row-wise d and construction need retrieval from the database. This is historical human computation, not AI.",
      "primary_sources": [
        "https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html",
        "https://codetables.de/"
      ],
      "verification_cost": "Medium for small k (enumerate q^k codewords); high beyond that. Restrict benchmark to enumerable dimensions or certificate-backed distance.",
      "risks": "Minimum-distance inner enumeration grows exponentially; restrict k (and n) and verify row construction. Database values are best-known, not all proven optimal. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.",
      "recommendation": "MVP候选",
      "reason": "Canonical construction problem and extensively maintained human table, with one exact scalar and matrix output.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa06",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T067",
      "name": "Maximum size of a binary code A(n,d)",
      "category": "编码理论",
      "definition": "Construct a subset C of {0,1}^n with pairwise Hamming distance at least d and maximum cardinality.",
      "solution_format": "List of binary words; verify distinctness and pairwise distances.",
      "scalar_objective": "|C|",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "block length",
        "d": "minimum distance"
      },
      "human_baseline": "A. E. Brouwer's classical tables and ongoing bounds; specific construction/value must be fixed per row. Human literature/database; no AI baseline assumed.",
      "primary_sources": [
        "https://aeb.win.tue.nl/codes/binary.html"
      ],
      "verification_cost": "O(|C|^2 n) for lower-bound witness; proving optimality substantially harder.",
      "risks": "Many instances have only bounds, not exact optimum; select a published construction row and compare witness cardinality, not claim optimality.",
      "recommendation": "后备候选",
      "reason": "Canonical extremal scalar and substantial human research; requires careful row selection and verifiable explicit witnesses.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa09",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T068",
      "name": "Constant-weight code A(n,d,w)",
      "category": "编码理论",
      "definition": "Find a largest family of w-subsets of an n-set with pairwise symmetric difference at least d.",
      "solution_format": "List of w-subsets/bitmasks; verify all weights and pairwise Hamming distances.",
      "scalar_objective": "Code size |C|",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "ambient length",
        "d": "minimum Hamming distance",
        "w": "constant word weight"
      },
      "human_baseline": "Brouwer, Shearer, Sloane and Smith (1990) compiled bounds; many later explicit constructions and improved bounds. Pin row and construction before benchmark inclusion; human baseline, no AI assumed.",
      "primary_sources": [
        "https://aeb.win.tue.nl/codes/Andw.html"
      ],
      "verification_cost": "Low/medium: O(|C|^2 n), often under a second for small instances.",
      "risks": "Do not confuse lower-bound construction with known optimum; duplicate of general nonlinear code only if constant-weight constraint is not central. Fixed rows needed. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.",
      "recommendation": "后备候选",
      "reason": "Named classical family, explicit construction tables and a cheap exact scalar verifier.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa10",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T069",
      "name": "Constant-dimension subspace code A_q(n,d;k)",
      "category": "编码理论",
      "definition": "Find the largest set of k-dimensional subspaces of GF(q)^n with pairwise subspace distance at least d.",
      "solution_format": "Basis matrices/RREFs for subspaces; exact rank/intersection verification.",
      "scalar_objective": "Code size |C|",
      "direction": "maximize",
      "configuration_parameters": {
        "q": "field order",
        "n": "ambient dimension",
        "k": "subspace dimension",
        "d": "minimum subspace distance"
      },
      "human_baseline": "Heinlein, Kiermaier, Kurz and Wassermann (2016, updated 2019) maintain Tables of Subspace Codes; the paper explicitly describes best lower/upper bounds and constructions. Fix an exact table row for score/construction.",
      "primary_sources": [
        "https://arxiv.org/abs/1601.02864",
        "https://subspacecodes.uni-bayreuth.de/"
      ],
      "verification_cost": "Medium: pairwise intersection ranks O(|C|^2 n^3) with finite-field linear algebra.",
      "risks": "Many rows are intervals rather than exact optima; select modest dimensions and public construction records. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.",
      "recommendation": "后备候选",
      "reason": "Canonical research objective, maintained human database and exact simple witness verifier.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa11",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T070",
      "name": "Covering code size",
      "category": "编码理论",
      "definition": "For fixed binary length n and covering radius R, construct a smallest set C whose radius-R Hamming balls cover the whole cube.",
      "solution_format": "List of codewords; verify full coverage by exhaustive enumeration for small n.",
      "scalar_objective": "Code size |C|",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "length",
        "R": "covering radius"
      },
      "human_baseline": "Cohen, Honkala, Litsyn and Lobstein (1997) survey and tabulate covering codes; select a small open/nontrivial instance and recover explicit construction.",
      "primary_sources": [
        "https://neilsloane.com/doc/CR.html"
      ],
      "verification_cost": "Low for small n (2^n point coverage), exponential and unsuitable for large n.",
      "risks": "Inner covering check scales exponentially; exact optimum often unknown. Only small finite instances qualify.",
      "recommendation": "后备候选",
      "reason": "Natural one-scalar design task with historical constructions, but verifier cost bounds useful scale.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa18",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T071",
      "name": "Maximum permutation code size",
      "definition": "固定 n,d，输出 S_n 的子集，使任意两排列的 Hamming 距离至少 d。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "number of codewords",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "排列阶数",
        "d": "最小Hamming距离"
      },
      "human_baseline": "Bereg et al. (2019) Partition and Extension 给出显式人类构造与数值表；Ding–Fu–Kløve–Wei (2002)、Gao et al. (2008) 等经典构造可复现。需固定具体表格行。",
      "primary_sources": [
        "https://arxiv.org/abs/1804.08252",
        "https://arxiv.org/abs/0801.3987"
      ],
      "verification_cost": "低至中 O(M²n)。",
      "risks": "大群的生成元不是自动可快速验证的完整码；初期只接受显式小码。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-permutation-code",
      "category": "编码理论",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T072",
      "name": "Maximum deletion-correcting code size",
      "definition": "固定 q,n,t，输出 q 元长度 n 的码，任意不同码字的 t-deletion balls 不相交。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "number of codewords",
      "direction": "maximize",
      "configuration_parameters": {
        "q": "字母表大小",
        "n": "码长",
        "t": "可纠正删除数"
      },
      "human_baseline": "Varshamov–Tenengolts (1965) / Levenshtein (1966) 的二元单删除码有明确同余公式；按给定 n 枚举其码字可以得到可重算历史人类baseline。",
      "primary_sources": [
        "https://arxiv.org/abs/math/0207197",
        "https://neilsloane.com/doc/dijen.pdf"
      ],
      "verification_cost": "中：每码字枚举删除结果或两两 LCS；规模受限。",
      "risks": "VT明确同余构造见Sloane (2002)原稿；固定n后枚举得到人类基线，不能将其当全部有限n都已证最优。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-deletion-code",
      "category": "编码理论",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T073",
      "name": "LABS minimum aperiodic autocorrelation energy",
      "category": "序列与平坦多项式",
      "definition": "For s_i in {±1}, length L, minimize E=Σ_{k=1}^{L−1}(Σ_{i=1}^{L−k}s_i s_{i+k})².",
      "solution_format": "Binary sign sequence.",
      "scalar_objective": "E (equivalently merit factor L²/(2E))",
      "direction": "minimize",
      "configuration_parameters": {
        "L": "sequence length; select fixed rows, do not count lengths as separate task families"
      },
      "human_baseline": "Packebusch–Mertens (2015/2016) exact optima for lengths<=66 in the cited paper; Militzer author page has explicit historical evolutionary sequences. Do not describe historical records as latest.",
      "primary_sources": [
        "https://arxiv.org/abs/1512.02475",
        "https://militzer.berkeley.edu/sequences.html"
      ],
      "verification_cost": "Low: O(L²) integer arithmetic.",
      "risks": "Energy and merit factor are strictly monotone transforms for fixed L, so they are the same task and must not be counted twice. Best known versus proven optimum must be labeled.",
      "recommendation": "MVP候选",
      "reason": "Canonical researched objective, explicit human sequence tables, extremely cheap exact scalar verifier.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa21",
      "publication_status": "candidate_only",
      "baseline_audit": "example_witness_recomputed_not_full_task_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T074",
      "name": "LABS peak sidelobe level (PSL)",
      "category": "序列与平坦多项式",
      "definition": "For binary sign sequence s of length L, minimize max_{1≤k<L}|Σ_{i=1}^{L−k}s_i s_{i+k}|.",
      "solution_format": "Binary sign sequence.",
      "scalar_objective": "PSL=max absolute nonzero aperiodic autocorrelation",
      "direction": "minimize",
      "configuration_parameters": {
        "L": "sequence length"
      },
      "human_baseline": "Dmitriev and Jedwab (2005) studied typical PSL; later Best-Known Peak Sidelobe Level Values (2021) reports constructed sequences and search results. Retrieve row-specific construction before instantiation.",
      "primary_sources": [
        "https://www.sfu.ca/~jed/Research/PSL.html",
        "https://arxiv.org/abs/1212.4930",
        "https://arxiv.org/abs/2104.10477"
      ],
      "verification_cost": "Low O(L²).",
      "risks": "PSL optima can conflict with LABS energy; do not present as interchangeable with merit factor. Current row baseline needed.",
      "recommendation": "后备候选",
      "reason": "Independent standard objective with its own human literature and one exact integer score.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa22",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T075",
      "name": "Periodic binary autocorrelation energy",
      "category": "序列与平坦多项式",
      "definition": "For s∈{±1}^L, minimize the sum of squares of nonzero periodic autocorrelations C(k)=Σ_i s_i s_{i+k mod L}.",
      "solution_format": "Binary sign sequence.",
      "scalar_objective": "Σ_{k=1}^{L−1} C(k)^2",
      "direction": "minimize",
      "configuration_parameters": {
        "L": "period length"
      },
      "human_baseline": "经典Legendre/Paley周期序列，以及Yan–Chen–Li (2014)、Yan–Gong (2014)等显式构造。p≡3(mod4)的Legendre符号序列（0项设1）给每个非零周期自相关−1，可作为已解校准：能量p−1、PSL1。非已解长度须另选行级人类构造。",
      "primary_sources": [
        "https://arxiv.org/abs/1401.2530",
        "https://arxiv.org/abs/1411.4340",
        "https://doi.org/10.1016/j.tcs.2009.02.021"
      ],
      "verification_cost": "Low O(L²).",
      "risks": "Be precise about periodic versus aperiodic correlation and normalization; known perfect sequences may make selected cases trivial.",
      "recommendation": "后备候选",
      "reason": "Natural scalar and mature literature, but needs row-specific open headroom and cited human record.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa24",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T076",
      "name": "Binary sequence maximum out-of-phase autocorrelation (periodic merit)",
      "category": "序列与平坦多项式",
      "definition": "For fixed length L, construct a binary sequence minimizing the maximum absolute nonzero periodic autocorrelation.",
      "solution_format": "Binary sign sequence.",
      "scalar_objective": "max_{k≠0}|Σ_i s_i s_{i+k mod L}|",
      "direction": "minimize",
      "configuration_parameters": {
        "L": "period length"
      },
      "human_baseline": "经典Legendre/Paley周期序列，以及Yan–Chen–Li (2014)、Yan–Gong (2014)等显式构造。p≡3(mod4)的Legendre符号序列（0项设1）给每个非零周期自相关−1，可作为已解校准：能量p−1、PSL1。非已解长度须另选行级人类构造。",
      "primary_sources": [
        "https://arxiv.org/abs/1401.2530",
        "https://arxiv.org/abs/1411.4340",
        "https://doi.org/10.1016/j.tcs.2009.02.021"
      ],
      "verification_cost": "Low O(L²).",
      "risks": "Related but distinct from aperiodic PSL; ensure periodic definition and cited baseline align exactly.",
      "recommendation": "后备候选",
      "reason": "Natural exact scalar and historical research, but needs a fixed, sourced comparison row.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa45",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T077",
      "name": "Littlewood polynomials: minimum supremum modulus",
      "definition": "输出长度 L 的±1系数多项式 P，最小化整个单位圆上的归一化最大模。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "max_{|z|=1}|P(z)|/sqrt(L)",
      "direction": "minimize",
      "configuration_parameters": {
        "L": "系数个数"
      },
      "human_baseline": "Rudin–Shapiro 递推给出人类显式多项式和上界 sqrt(2)（L为2的幂）；Odlyzko (2018) 对有限长度做过大量数值搜索。记录数值需全域认证。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html",
        "https://arxiv.org/abs/1907.09464"
      ],
      "verification_cost": "中至高：三角多项式全域极值；不是只采样。",
      "risks": "核实第二来源与所用构造定义；文献中的网格最优不是严格全域最优。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-littlewood-sup",
      "category": "序列与平坦多项式",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T078",
      "name": "Littlewood polynomials: maximum infimum modulus",
      "definition": "输出长度 L 的±1系数多项式 P，最大化整个单位圆上的归一化最小模。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "min_{|z|=1}|P(z)|/sqrt(L)",
      "direction": "maximize",
      "configuration_parameters": {
        "L": "系数个数；注意奇偶造成的单位根"
      },
      "human_baseline": "Littlewood 的平坦多项式问题、Odlyzko (2018) 数值构造、Balister et al. 的 Flat Littlewood Polynomials 提供人类基线来源；具体 L 的系数和严格最小模尚须定位。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html",
        "https://arxiv.org/abs/1907.09464"
      ],
      "verification_cost": "中至高：全域下界证书。",
      "risks": "并非最小sup的单调改写；当前只有文献入口，不能宣称有限实例humanbaseline已齐。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-littlewood-inf",
      "category": "序列与平坦多项式",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T079",
      "name": "First Autocorrelation Inequality (AC1)",
      "category": "极值分析",
      "definition": "Find nonnegative integrable f supported on [-1/4,1/4], integral 1, minimizing max_{t in [-1/2,1/2]} (f*f)(t).",
      "solution_format": "Exact piecewise-polynomial or rational step function with proof of support, positivity and unit mass.",
      "scalar_objective": "Phi1=max_t(f*f)(t)",
      "direction": "minimize",
      "configuration_parameters": {
        "support": "fixed [-1/4,1/4]",
        "representation": "piecewise polynomial degree and breakpoints; configure separately"
      },
      "human_baseline": "SimpleTES (2026 paper table 11 reports human 1.509730; AI-assisted results separate: AlphaEvolve 1.505300; SimpleTES 1.503871). Human attribution cites prior sources [15,82,147], which should be independently checked before benchmark release.",
      "primary_sources": [
        "https://arxiv.org/abs/0907.1379",
        "https://math.bme.hu/~matolcsi/sch0914.pdf",
        "https://arxiv.org/abs/2604.19341"
      ],
      "verification_cost": "Medium/high: exact convolution per polynomial segment, certify global maximum via roots/interval arithmetic.",
      "risks": "Sampling the continuum maximum is not a proof; enforce exact mass and nonnegativity. Human baseline provenance needs citation-level audit.",
      "recommendation": "MVP候选",
      "reason": "Named established objective, human record and one scalar; strict certificate possible with piecewise-polynomial representation.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa01",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T080",
      "name": "Second Autocorrelation Inequality (AC2)",
      "category": "极值分析",
      "definition": "Find nonnegative integrable f supported on [-1/4,1/4], integral 1, maximizing ||f*f||_2^2/(||f*f||_1 ||f*f||_infinity).",
      "solution_format": "Exact piecewise-polynomial or rational step function with proof of support, positivity and unit mass.",
      "scalar_objective": "Phi2=||f*f||_2^2/(||f*f||_1||f*f||_infinity)",
      "direction": "maximize",
      "configuration_parameters": {
        "support": "fixed [-1/4,1/4]",
        "representation": "piecewise polynomial degree and breakpoints; configure separately"
      },
      "human_baseline": "SimpleTES (2026 table 11) reports best human 0.901500; AI-assisted: AlphaEvolve V2 0.961000; SimpleTES 0.962694.",
      "primary_sources": [
        "https://arxiv.org/abs/0907.1379",
        "https://math.bme.hu/~matolcsi/sch0914.pdf",
        "https://arxiv.org/abs/2604.19341"
      ],
      "verification_cost": "High: exact convolution and certified L2/L1/L-infinity evaluation; maximum requires root isolation/interval methods.",
      "risks": "A sampled supremum gives unsound scores; human record citation chain needs audit. Objective's denominator conventions must be fixed.",
      "recommendation": "MVP候选",
      "reason": "Explicit published extremal objective with named human and AI baselines; admits rigorous certificates using algebraic pieces.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa02",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T081",
      "name": "Third Autocorrelation Inequality (AC3)",
      "category": "极值分析",
      "definition": "Find real integrable f supported on [-1/4,1/4], integral 1, minimizing max_t |(f*f)(t)| over [-1/2,1/2].",
      "solution_format": "Exact piecewise-polynomial or rational step function, with exact integral and certified global supremum.",
      "scalar_objective": "Phi3=max_t |(f*f)(t)|",
      "direction": "minimize",
      "configuration_parameters": {
        "support": "fixed [-1/4,1/4]",
        "representation": "piecewise polynomial degree and breakpoints; configure separately"
      },
      "human_baseline": "SimpleTES (2026 table 11) reports best human 1.458100; AI-assisted results include AlphaEvolve 1.455700 and SimpleTES 1.453675. Paper flags some AI comparisons as using a corrected verifier.",
      "primary_sources": [
        "https://arxiv.org/abs/0907.1379",
        "https://math.bme.hu/~matolcsi/sch0914.pdf",
        "https://arxiv.org/abs/2604.19341"
      ],
      "verification_cost": "High: exact convolution; certify absolute maximum by polynomial critical-point isolation or interval arithmetic.",
      "risks": "Continuum maximum cannot be sampled; verifier versions differed in prior AI comparisons; audit human sources.",
      "recommendation": "MVP候选",
      "reason": "Named objective, scalar and human baseline are directly tabulated; exact semialgebraic witnesses can be certified.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa03",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T082",
      "name": "Erdős Minimum Overlap",
      "category": "极值分析",
      "definition": "Let f:[0,2]→[0,1] be a step function with ∫_0^2 f(x)dx=1. Define g(x)=1−f(x) for x∈[0,2] and g(x)=0 outside [0,2]. Minimize Ψ(f)=sup_{t∈R} ∫_R f(x)g(x+t)dx = sup_{t∈R} ∫_[0,2]∩[-t,2-t] f(x)(1−f(x+t))dx. Both f and g are zero outside [0,2]; this is essential. Include both shift directions and do not use finite M(N) as the same score.",
      "solution_format": "Exact rational step function with breakpoints and values, exact mass, and a rigorous maximization over all shifts s (piecewise polynomial plus root isolation/interval arithmetic).",
      "scalar_objective": "Ψ(f)=sup_{t∈R}∫_R f(x)g(x+t)dx, where f,g are supported on [0,2] and g=1−f on [0,2] (lower is better). Equivalent to the intersection-range integral; both positive and negative shifts are included.",
      "direction": "minimize",
      "configuration_parameters": {
        "step_count": "number of equal-width intervals on [0,2] (e.g. 15 or 51); representation setting, not a separate task"
      },
      "human_baseline": "Haugland (2016) reports human step-function upper-bound witnesses for this continuous normalized objective: 15 steps gives 0.38153155 (rounded upward); 51 steps gives 0.3809268534330870. These are reported construction scores, not independently reproduced here. AI-assisted results are separate.",
      "primary_sources": [
        "https://arxiv.org/abs/1609.08000",
        "https://arxiv.org/abs/2201.05704"
      ],
      "verification_cost": "Finite exact task low/medium; limiting witness high (integral/profile derivation and rigorous discretization error certificate).",
      "risks": "Both f and its complement g must be supported on [0,2], with g=1−f only inside [0,2] and zero outside. If 1−f is incorrectly zero-extended as a function equal to 1 outside, endpoint shifts spuriously score 1. Use sup over all real t, equivalently include both positive and negative shifts; a nonsymmetric candidate cannot be scored using only one shift direction. Certify the piecewise functional over every shift interval, not on a grid. The finite partition M(N)/N is related but not the same candidate score.",
      "recommendation": "MVP候选",
      "reason": "Named limiting extremal problem with Haugland continuous step-function upper-bound constructions and a natural scalar. The support convention for both f and g makes the score well-defined and comparable to the published 0.38 values.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa04",
      "publication_status": "candidate_only",
      "baseline_audit": "example_witness_recomputed_not_full_task_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T083",
      "name": "Autocorrelation lower envelope for difference bases",
      "definition": "构造可积函数 f，最大化位移 t∈[0,1] 上自相关的最小值，经L1质量归一化。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "min_{0<=t<=1} ∫f(x)f(x+t)dx / ||f||_1²",
      "direction": "maximize",
      "configuration_parameters": {
        "representation": "支持区间、分段复杂度需固定；不能改变位移区间的尺度后混比"
      },
      "human_baseline": "Barnard–Steinerberger 文献给出历史构造下界0.37（带边界修正的arcsine分布）；具体有界阶梯函数与0.37的适用参数待核。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/6.html",
        "https://arxiv.org/html/2511.02864v1#S6.SS2"
      ],
      "verification_cost": "中至高：全位移区间的下包络认证。",
      "risks": "奇异函数、边界点及积分容错曾导致原系统虚高得分，初期不选。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-difference-autocorrelation",
      "category": "极值分析",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T084",
      "name": "Sign uncertainty principle (Fourier sign changes)",
      "category": "极值分析",
      "definition": "For even real f∈L1(R), define A(f)=inf{r>0:f(x)≥0 for |x|≥r}; with f(0), fhat(0)<0, seek constructions making A(f)A(fhat) small, hence an upper bound on the best universal constant C in A(f)A(fhat)≥C.",
      "solution_format": "Explicit even real function with a rigorous Fourier transform/sign certificate and certified sign-change radii; use compactly supported piecewise-polynomial or Gaussian-polynomial forms with analytic transforms.",
      "scalar_objective": "A(f)A(fhat), which is an upper bound on the sharp constant C",
      "direction": "minimize",
      "configuration_parameters": {
        "Fourier_convention": "fix once",
        "function_family": "certifiable analytic family; degree/support settings are representation parameters"
      },
      "human_baseline": "Gonçalves, Oliveira e Silva and Steinerberger (2016): upper bound 0.353 and lower bound 0.2025. Cohn and Gonçalves (2017): upper bound 0.32831. Georgiev et al. (2025) AlphaEvolve-assisted construction: 0.321591. Cohn–de Laat–Gonçalves announced unpublished 0.3102 in 2025; distinguish this human result from AI-assisted AlphaEvolve.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/11.html",
        "https://arxiv.org/abs/1712.04438"
      ],
      "verification_cost": "High: certify signs of f and Fourier transform on unbounded domains, plus exact/rigorous threshold radii.",
      "risks": "A finite sample grid cannot certify eventual sign. Human 0.3102 is reported as unpublished in the AlphaEvolve problem page; use the published 0.32831 as baseline unless the unpublished artifact is publicly reproducible.",
      "recommendation": "后备候选",
      "reason": "Named sharp-constant problem, natural one-number witness objective, and documented human published bounds; only include with rigorous Fourier-tail/sign certification.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa46",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T085",
      "name": "Cohn–Elkies linear-programming bound for sphere packing",
      "category": "极值分析",
      "definition": "For a fixed dimension d, construct an admissible radial function f with f(0)>0, Fourier transform nonnegative and f(x)≤0 outside a specified radius, minimizing the normalized Cohn–Elkies upper bound on packing density.",
      "solution_format": "Exact polynomial-times-Gaussian or rigorously certified radial function with Fourier positivity and sign constraints, plus computed bound.",
      "scalar_objective": "Normalized linear-programming upper bound C(d)",
      "direction": "minimize",
      "configuration_parameters": {
        "d": "Euclidean dimension",
        "function_family": "radial basis / polynomial-Gaussian representation; exact certificate settings separate"
      },
      "human_baseline": "Cohn and Elkies (2003) introduced the LP bound; Viazovska (2017) proved its sharpness for E8, and Cohn, Kumar, Miller, Radchenko and Viazovska (2017) for Leech lattice dimension 24. For other dimensions, use published human LP bounds; choose an explicit row before acceptance.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/13.html",
        "https://arxiv.org/abs/math/0110009",
        "https://arxiv.org/abs/1603.04246",
        "https://arxiv.org/abs/1603.06518"
      ],
      "verification_cost": "High: global Fourier positivity and sign verification on continuous domains; interval/analytic certificates required.",
      "risks": "Do not score sampled radial values. Dimensions 8 and 24 have solved packing optima; select open dimensions and compare only a certified bound.",
      "recommendation": "后备候选",
      "reason": "Canonical scalar optimization with exceptional human constructions and rich public research, but the continuous certificate is demanding.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa52",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T086",
      "name": "General one-dimensional Gagliardo–Nirenberg sharp constant",
      "category": "极值分析",
      "definition": "For fixed admissible (j,p,q,r,m,θ), maximize ||D^j u||_p/(||D^m u||_r^θ ||u||_q^(1−θ)) over nonzero test functions u on R, with the scale relation in the AlphaEvolve problem statement.",
      "solution_format": "Explicit analytic or piecewise-polynomial function with rigorous norm and derivative-integral evaluation; certificate for a lower bound on C.",
      "scalar_objective": "||D^j u||_p / (||D^m u||_r^θ ||u||_q^(1−θ)) for the submitted u",
      "direction": "maximize",
      "configuration_parameters": {
        "j": "derivative order",
        "m": "higher derivative order",
        "p,q,r,theta": "admissible exponents; select one fixed row"
      },
      "human_baseline": "Classical Gagliardo (1958) and Nirenberg (1959) inequalities establish finiteness for the stated admissible regime. The AlphaEvolve paper states that the tested constants are known theoretically; it supplies the explicit solved special case aa49 but does not identify a single general-parameter human score. A fixed row and its sharp-constant reference remain待核实.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/15.html",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "High: improper integrals and derivative norms require certified tails; upper-bound proof of the sharp constant is harder than a witness score.",
      "risks": "General family is too broad as written; configure a single parameter tuple and distinguish a rigorous lower-bound witness from the unknown sharp constant.",
      "recommendation": "后备候选",
      "reason": "Natural one-number extremal objective and rich research, but benchmark needs a concrete row with an explicit human sharp value and certified witness evaluator.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa48",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T087",
      "name": "Rudin spherical harmonic Lp extremizer",
      "category": "极值分析",
      "definition": "For fixed d≥2, degree D and p∈{4,∞}, maximize ||u||_Lp(S^d)/||u||_L2(S^d) over real degree-D spherical harmonics, with sphere measure normalized to one.",
      "solution_format": "Harmonic coefficient vector in an exact orthonormal basis; certify norm ratio, using exact polynomial integration for p=4 or global optimization on sphere for p=∞.",
      "scalar_objective": "||u||_p/||u||_2 for the submitted spherical harmonic",
      "direction": "maximize",
      "configuration_parameters": {
        "d": "sphere dimension",
        "D": "harmonic degree",
        "p": "4 or infinity"
      },
      "human_baseline": "AlphaEvolve repository problem 57 and Georgiev et al. (2025) identify the finite-dimensional extremal problem, but the exact row-level human record/value was not retrieved in this pass; mark score待核实 before inclusion.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/57.html",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "Medium for p=4 (finite algebraic integral); high for p=∞ (continuous sphere supremum).",
      "risks": "Need a published human construction/value for a specific (d,D,p); continuum maximization for p=∞ cannot be sampled as proof.",
      "recommendation": "后备候选",
      "reason": "Clean single scalar and finite-dimensional search space; baseline evidence and strict p=∞ verifier remain incomplete.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa53",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T088",
      "name": "Ovals curvature Schrödinger eigenvalue",
      "category": "极值分析",
      "definition": "Minimize the lowest periodic eigenvalue λ0 of Hγ=−d²/ds²+κ(s)² over simple closed convex plane curves of length 2π.",
      "solution_format": "Certified convex curve (e.g. rational Fourier curvature/tangent data satisfying closure and total turning) and rigorous eigenvalue upper bound; lower-bound claims need proof.",
      "scalar_objective": "λ0(Hγ)",
      "direction": "minimize",
      "configuration_parameters": {
        "length": "fixed 2π",
        "curve_representation": "Fourier coefficients/breakpoints and exact closure constraints"
      },
      "human_baseline": "Benguria and Loss (2004) identified the circle/equality family with value 1, giving C≤1; Linde's 2015 work gives a global lower bound C>0.81 and numerical evaluation C>0.8246 (as summarized in later research). AlphaEvolve (2025) recovered the circle but not the noncircular equality family. Human constructions are explicit.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/19.html",
        "https://doi.org/10.1007/s00023-004-0186-8",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "High: certify convexity/closure and periodic Schrödinger ground-state eigenvalue; use validated spectral bounds.",
      "risks": "Circle immediately attains the known upper value 1; to create a useful benchmark, target a different construction such as recovery of noncircular equality family, but that is structural and not a scalar improvement.",
      "recommendation": "后备候选",
      "reason": "A named spectral variational problem with explicit human extremizers, but the scalar is already attained by the circle and meaningful discovery headroom is limited.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa54",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T089",
      "name": "Maximum determinant of sign matrices",
      "category": "矩阵、格与代数极值",
      "definition": "Find A in {−1,+1}^{29x29} maximizing |det A|.",
      "solution_format": "29x29 sign matrix; exact determinant certificate; optionally a proving upper-bound certificate if optimality is claimed.",
      "scalar_objective": "|det A| (equivalently the normalized determinant in the cited benchmark)",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "阶数；原论文实例29，新配置例如31"
      },
      "human_baseline": "Orrick and Solomon's classical record, as reported by Ye et al. (2026): |det|=320·7^12·2^28 (normalized 0.935673). SimpleTES recovers it; this is AI-assisted and is not the human baseline.",
      "primary_sources": [
        "https://maths-people.anu.edu.au/~brent/maxdet/order29/",
        "https://arxiv.org/abs/math/0304410"
      ],
      "verification_cost": "Low: Bareiss exact determinant; optimality verification is separate and harder.",
      "risks": "Do not score only existence of Hadamard; exact determinant is the natural scalar. Published value is a best-known lower bound, not necessarily proved global maximum.",
      "recommendation": "MVP候选",
      "reason": "Explicit known scalar record, human construction, exact cheap evaluator; fixed order is configuration.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa05",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T090",
      "name": "Minkowski lattice packing density",
      "category": "矩阵、格与代数极值",
      "definition": "For a fixed dimension and specified lattice class, construct a lattice packing maximizing sphere-packing density.",
      "solution_format": "Basis matrix plus rigorous determinant/minimum-vector-length certificate.",
      "scalar_objective": "Packing density (equivalently inverse covolume at fixed minimum distance)",
      "direction": "maximize",
      "configuration_parameters": {
        "dimension": "d",
        "lattice_class": "all lattices or specified symmetry"
      },
      "human_baseline": "Minkowski (1896) introduced the problem; human constructions include root lattices, with exact densest lattice results known in some low dimensions (e.g. dimension 8 and 24 via Viazovska and collaborators for all packings). Row-specific lattice optima vary.",
      "primary_sources": [
        "https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/",
        "https://arxiv.org/abs/1603.04246",
        "https://arxiv.org/abs/1603.06518"
      ],
      "verification_cost": "High: shortest-vector and determinant certification; dimension-dependent.",
      "risks": "May be closed in famous dimensions or difficult to verify in open dimensions; source domain is geometric construction, suitable only with exact finite certificates.",
      "recommendation": "后备候选",
      "reason": "A single meaningful continuous scalar and extensive human constructions, but certificates and open-instance screening are demanding.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa39",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T091",
      "name": "Sendov extremal critical-point distance",
      "category": "矩阵、格与代数极值",
      "definition": "For fixed degree n, maximize over degree-n complex polynomials with all roots in the unit disk the quantity max_k min_j |z_k−w_j|, where z_k are roots and w_j roots of f′; this is the sharp constant C(n).",
      "solution_format": "Polynomial coefficients or roots, with certified root/critical-point distances; provide exact algebraic or interval-certified roots.",
      "scalar_objective": "max_k min_j |z_k−w_j| for the submitted polynomial",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "polynomial degree; choose a single unresolved medium degree"
      },
      "human_baseline": "The human construction f(z)=z^n−1 gives C(n)≥1 exactly. Sendov conjectured C(n)=1. Meir–Sharma proved n<6; Brown n<7 and n<8; Brown–Xiang proved n≤8 (1999); Tao proved the sufficiently large-degree regime. Medium degrees remain open in the 2025 paper.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/20.html",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "Medium for candidate polynomial: certify roots and derivative roots; proving global supremum ≤1 is a deep theorem.",
      "risks": "For n≤8 or sufficiently large n human theory proves the conjectured value; choose a genuinely unresolved medium n. Numerical polynomial candidate is only a lower-bound witness.",
      "recommendation": "删除：整个任务已解",
      "reason": "Strong named open family and exact human construction at scalar 1; select a medium degree and rigorously certify root distances.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa55",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "2026年Sendov证明使当前标量C(n)=1；z^n−1已取等号。该定义下所有次数无纪录提升空间。",
      "discovery_entry_status": "excluded_closed_task"
    },
    {
      "id": "T092",
      "name": "Schmeisser polynomial critical-point barycenter constant",
      "category": "矩阵、格与代数极值",
      "definition": "For fixed n, determine the least C(n) such that for each degree-n polynomial with roots in the unit disk and every convex combination of its roots, some critical point lies within distance C(n) of that combination.",
      "solution_format": "Explicit polynomial roots and convex weights for lower-bound witness; exact derivative roots and certified distances.",
      "scalar_objective": "min_j |Σ_k l_k z_k−w_j| for the submitted polynomial and weights",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "degree n≥2",
        "weights": "simplex weights; part of optimization variables"
      },
      "human_baseline": "Schmeisser conjectured C(n)=1; the AlphaEvolve repository states the conjectured value but no numeric human construction or row-specific best lower bound was verified in this scan. Treat numerical baseline as待核实.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/21.html",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "Medium/high: polynomial root certification and optimization over a continuum of convex weights.",
      "risks": "Human construction/record not verified; worst-case optimization includes a continuous simplex and polynomial family. Need a finite witness protocol.",
      "recommendation": "后备候选",
      "reason": "Natural scalar extremal constant and cited human conjecture, but presently lacks a verified numeric construction baseline.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa56",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T093",
      "name": "Borcea p-moment critical-point distance constant",
      "category": "矩阵、格与代数极值",
      "definition": "For fixed (p,n), maximize the worst root-to-nearest-critical-point distance over degree-n polynomials whose roots satisfy n^−1Σ|z_i|^p≤1; this defines C(p,n).",
      "solution_format": "Polynomial roots and derivative roots with exact/interval algebraic data; verify moment constraint and distances.",
      "scalar_objective": "max_{root ζ} min_{critical ξ}|ξ−ζ| for the submitted normalized polynomial",
      "direction": "maximize",
      "configuration_parameters": {
        "p": "moment exponent, 1≤p<∞",
        "n": "degree n≥2"
      },
      "human_baseline": "Borcea (1996) proved Sendov's conjecture for polynomials with at most seven distinct zeros. Khavinson, Pereira, Putinar, Saff and Shimorin (2011) formulated Borcea's variance conjectures; AlphaEvolve paper notes Borcea's conjecture C(p,n)=1 and verifies special cases (p,n)=(1,3),(2,4) in the cited literature. No general numeric row baseline retrieved.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/22.html",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "High: root and derivative root enclosures plus moment constraint; global sharpness unverified.",
      "risks": "Related to Sendov but genuinely adds a p-moment condition; parameter p=∞ recovers Sendov-like behavior. Need a concrete open row and numeric human lower construction.",
      "recommendation": "后备候选",
      "reason": "A distinct published strengthening with a single scalar; current baseline data are insufficient for a frozen benchmark row.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa57",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T094",
      "name": "Noncommutative matrix AM–GM ratio",
      "category": "矩阵、格与代数极值",
      "definition": "固定n,m,d和一个明确的酉不变范数，提交n个d×d半正定矩阵A_i，最小化有放回与无放回的长度m乘积范数平均值之比。",
      "solution_format": "Finite PSD matrices with rational/algebraic entries; exact products, norms, and ratio or certified eigenvalue bounds.",
      "scalar_objective": "[n^(−m) Σ_{j1,…,jm} ||A_j1⋯A_jm||] / [((n−m)!/n!) Σ_{distinct j1,…,jm} ||A_j1⋯A_jm||]",
      "direction": "minimize",
      "configuration_parameters": {
        "n,m,d": "固定，小n和m限制枚举成本",
        "norm": "例如operator norm，必须固定"
      },
      "human_baseline": "Duchi (2012) posed noncommutative AM–GM conjectures; Recht and Ré (2012) gave commentary/counterexample context. De Sa (2020) constructed counterexamples to a related matrix inequality. Exact parameter-row record and theorem status need primary-source audit.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/47.html",
        "https://proceedings.mlr.press/v23/recht12.html"
      ],
      "verification_cost": "Medium/high: exact matrix products and spectral norms; PSD/eigenvalue constraints need certification.",
      "risks": "分母必须严格正；PSD和所选范数都需验证。原代理未抄明确方向，本表按官方47题取inf修正。乘积枚举n^m，仅小配置适合快速验证。",
      "recommendation": "后备候选",
      "reason": "Published matrix inequality family offers a natural scalar ratio, but objective direction and row-level baseline need exact primary-source reconstruction.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa61",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T095",
      "name": "Minimum Mahler measure of noncyclotomic integer polynomials",
      "category": "矩阵、格与代数极值",
      "definition": "For fixed degree bound d, find a noncyclotomic monic integer polynomial minimizing Mahler measure M(P)=∏ max(1,|root|).",
      "solution_format": "Integer polynomial with irreducibility/noncyclotomic proof and certified roots/Mahler measure.",
      "scalar_objective": "Mahler measure M(P)",
      "direction": "minimize",
      "configuration_parameters": {
        "degree_bound": "d",
        "class": "monic integer, irreducible, noncyclotomic"
      },
      "human_baseline": "Lehmer (1933)给出degree10多项式 x^10+x^9−x^7−x^6−x^5−x^4−x^3+x+1，Mahler measure约1.176280818。这是经典历史人类构造；不就2026最新状态作未经核实断言。",
      "primary_sources": [
        "https://doi.org/10.2307/1968172",
        "https://www.research.ed.ac.uk/files/1874954/Smyth240707.pdf"
      ],
      "verification_cost": "Medium/high: irreducibility and roots/Mahler measure require exact algebraic certification.",
      "risks": "For degree bounded and broad coefficient sizes the search space is ill-defined; specify coefficient/degree constraints and distinguish known lower bound from conjectured minimum.",
      "recommendation": "后备候选",
      "reason": "Famous named scalar challenge and human construction, but parameterization and exact certification need careful design.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa34",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T096",
      "name": "Integer Chebyshev polynomial construction",
      "definition": "给定区间 E 与次数上限 n，构造非零整数系数多项式 P，最小化其在 E 上的sup范数。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "||P||_E^(1/n)",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "固定次数上限，归一化指数固定为该n",
        "E": "例如[0,1]"
      },
      "human_baseline": "Pritsker (2001/2005)、Habsieger–Salvy、Flammang 等提供显式因子构造。Pritsker原稿有历史界；近年声称新界的预印本不自动作为已核人类纪录。",
      "primary_sources": [
        "https://arxiv.org/abs/math/0101166",
        "https://math.okstate.edu/people/igor/intcheb.pdf"
      ],
      "verification_cost": "中：整数多项式临界点隔离和区间端点求值。",
      "risks": "区别于实系数Chebyshev闭式问题；需要具体次数和因子指数表，不能用渐近常数当有限分数。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-integer-chebyshev",
      "category": "矩阵、格与代数极值",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T097",
      "name": "Shortest addition chain",
      "definition": "固定目标整数 n，输出从1出发的加法链，每项为之前两项之和，末项n。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "number of additions",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "目标整数；大小与位数为配置"
      },
      "human_baseline": "Flammenkamp、Clift 有精确长度数据库；Wilson/Resta 公开 n<=1024 的实际最短链。大数记录须区分历史人与近期可能AI参与的更新。",
      "primary_sources": [
        "https://wwwhomes.uni-bielefeld.de/achim/addition_chain.html",
        "https://webhost.services.iit.cnr.it/staff/giovanni.resta/ac/"
      ],
      "verification_cost": "低：逐步验证等式和长度。",
      "risks": "小数多数已知最优，适合校准；单目标最优加法链NP-hard性不能从多目标版本直接推断。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-addition-chain",
      "category": "数论与算术构造",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T098",
      "name": "Integer complexity",
      "definition": "固定正整数 n，输出只由常数1、+、×、括号组成且值为n的表达式，最小化1的个数。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "number of ones",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "目标整数；表达式按树计数，不允许共享子表达式免费复用"
      },
      "human_baseline": "Arias de Reyna–van de Lune (2014) 及 Fuller 的算法给出人类精确结果；Iraids等研究展示截至10^12的历史计算范围。具体表达式尚须从构造算法重建。",
      "primary_sources": [
        "https://arxiv.org/abs/1404.2183",
        "https://cs.uwaterloo.ca/~shallit/DC2015/iraids2.pdf"
      ],
      "verification_cost": "低至中：大整数表达式求值。",
      "risks": "已知最优值表不等于已下载表达式；与允许共享中间量的加法链不同。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-integer-complexity",
      "category": "数论与算术构造",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T099",
      "name": "Narrow admissible prime k-tuples",
      "definition": "固定 k，输出 k 个不同整数 H，使每个素数 p 下 H 不覆盖所有剩余类，最小化直径。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "max(H)-min(H)",
      "direction": "minimize",
      "configuration_parameters": {
        "k": "元组大小"
      },
      "human_baseline": "Engelsma–Sutherland/Polymath8 2013数据库有k=2..5000的元组、日期和贡献者；本次已下载并精确验证 k50直径246、k100直径558。",
      "primary_sources": [
        "https://math.mit.edu/~primegaps/",
        "https://math.mit.edu/~drew/PrimeGapsOberwolfach3.pdf"
      ],
      "verification_cost": "低：只需检验 p<=k 的素数，p>k自动成立。",
      "risks": "不是直接搜索素数；最窄admissible tuple与是否产生无穷素数簇分开。",
      "recommendation": "MVP候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-admissible-tuple",
      "category": "数论与算术构造",
      "publication_status": "candidate_only",
      "baseline_audit": "example_witness_recomputed_not_full_task_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    },
    {
      "id": "T100",
      "name": "Factoring N! into N balanced factors",
      "category": "数论与算术构造",
      "definition": "For a fixed integer N, partition prime factors of N! among N integer factors and maximize the smallest factor; C(N) is the largest c for which N! can be factored into N factors all at least c.",
      "solution_format": "N positive integers with product exactly N!; verify exact product and minimum factor.",
      "scalar_objective": "min_i a_i, with the task maximizing this minimum (lower bound on C(N))",
      "direction": "maximize",
      "configuration_parameters": {
        "N": "positive integer; choose a fixed table row"
      },
      "human_baseline": "Guy and Selfridge studied the problem; the AlphaEvolve paper cites asymptotic C(N)/N=1/e−c0/log N+O(1/log^(1+c)N). Andrew Sutherland's public GuySelfridge.m implements a human search, and exact values C(N) for N≤10^4 are listed in the cited erdos-guy-selfridge repository/OEIS A034258. Retrieve a fixed row/value before freeze; not AI baseline.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/38.html",
        "https://github.com/teorth/erdos-guy-selfridge",
        "https://math.mit.edu/~drew/GuySelfridge.m",
        "https://oeis.org/A034258",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "Low for witnesses (big integer product); exact optimum is a bin-covering problem and may be expensive.",
      "risks": "Product factorization means integer factors, not arbitrary reals; fixed N and exact table baseline are mandatory. Optimality verification can be NP-hard.",
      "recommendation": "后备候选",
      "reason": "Natural discrete construction score, exact cheap witness verification, and a public human algorithm plus extensive value table.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa62",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit"
    }
  ]
}
```

</details>

### 后续发现轨修订

<details>
<summary>后续发现轨修订：完整记录</summary>

迁入来源：`discovery_candidates_v2.json`；原文件SHA-256：`520aacd2b0bd9f641c838cfaea4e877f2c1542e445d673041b3d3df25bb70971`。

```json
{
  "title": "数学构造发现 benchmark 选型 v2",
  "date": "2026-11-03",
  "scope": "discovery_only_no_solved_calibration",
  "categories": 12,
  "candidate_families": 110,
  "retained_v1_families": 97,
  "new_candidate_families": 13,
  "excluded_v1_tasks": [
    "T018",
    "T050",
    "T091"
  ],
  "configuration_review_records": 15,
  "admitted_configurations": 94,
  "proposed_initial_tasks": 20,
  "warning": "110是候选家族数。当前通过与待补状态以confirmation_summary.json为准。独立重算不再是选型通过的前置要求。",
  "tasks_catalog": [
    {
      "id": "T001",
      "name": "Equal-circle packing in fixed containers",
      "category": "几何装填与覆盖",
      "definition": "Place n congruent disks without overlap in a square and minimize the square side (equivalently maximize the common disk radius in a unit square).",
      "solution_format": "disk centers and radius, or normalized center coordinates",
      "scalar_objective": "maximum common radius in unit square (equivalently minimum container side for unit disks)",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "圆数量",
        "container": "单位正方形为主；圆形/矩形等独立基线容器配置"
      },
      "human_baseline": "Packomania lists best-known values, coordinates, drawings, contact graphs, and attribution codes for n up to 10000; it marks proven optima. Human attribution in records, AI involvement unknown.",
      "primary_sources": [
        "https://packomania.com/csq/",
        "https://packomania.com/"
      ],
      "verification_cost": "medium; pairwise distance and wall-clearance checks; upper-bound optimality is generally hard",
      "risks": "Packomania is a changing best-known catalogue, not a proof for most n; choose frozen version/instances and verify contact tolerances.",
      "recommendation": "MVP候选",
      "reason": "Named classical continuous optimization problem, dense public records and coordinates, natural scalar objective.",
      "research_origin": "geometry.json",
      "source_id": "geo-circle-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "specific_configuration_evidence_located_not_replayed",
      "open_configuration_reviews": [
        {
          "review_id": "R001",
          "task_id": "T001",
          "parameters": {
            "n": 26,
            "container": "unit square"
          },
          "scalar": "common radius ↑",
          "human_baseline": "Nurmela–Östergård 1999: 0.096362339010",
          "frontier_evidence": "record row not marked proved optimal; no matching numerical upper bound frozen",
          "sources": [
            "https://packomania.com/csq/"
          ],
          "readiness": "source_located_not_release_ready"
        },
        {
          "review_id": "R002",
          "task_id": "T001",
          "parameters": {
            "n": 32,
            "container": "unit square"
          },
          "scalar": "common radius ↑",
          "human_baseline": "Boll et al. 2000: 0.087858157088",
          "frontier_evidence": "same caveat",
          "sources": [
            "https://packomania.com/csq/"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T002",
      "name": "Packing unit squares in squares",
      "category": "几何装填与覆盖",
      "definition": "Pack n non-overlapping unit squares, allowing arbitrary rotation, into the smallest enclosing square.",
      "solution_format": "square centers and orientations; enclosing side s",
      "scalar_objective": "minimum enclosing-square side s(n)",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "正方形数量",
        "container": "正方形主轨；其他容器须独立基线"
      },
      "human_baseline": "Erich Friedman’s 2009 survey gives best-known bounds/packings for n≤100 and historical authors. It proves selected n and reports named constructions by Göbel, Trump, Wainwright, Hämäläinen, Bidwell, Cantrell, and others; computer-search involvement is explicit for some later records. AI involvement unknown.",
      "primary_sources": [
        "https://erich-friedman.github.io/papers/squares/squares.html",
        "https://kingbird.myphotos.cc/packing/squares_in_squares.html"
      ],
      "verification_cost": "medium; non-overlap and enclosure directly checkable; optimality proof hard",
      "risks": "Do not treat upper-bound construction as proven optimum except rows marked/proven in the paper; use exact coordinate reconstruction.",
      "recommendation": "MVP候选",
      "reason": "Named longstanding problem, unusually clear human history, explicit scalar and published benchmark range.",
      "research_origin": "geometry.json",
      "source_id": "geo-unit-squares-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "specific_configuration_evidence_located_not_replayed",
      "open_configuration_reviews": [
        {
          "review_id": "R003",
          "task_id": "T002",
          "parameters": {
            "n": 26
          },
          "scalar": "unit-square container side ↓",
          "human_baseline": "Friedman 1997: (7+3sqrt(2))/2 ≈5.62132034356",
          "frontier_evidence": "maintained project reports verified interval [5.545,5.62132034356]; lower proof replay not repeated here",
          "sources": [
            "https://squaremath.org/cases/26.html"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T003",
      "name": "Equilateral-triangle packing in a square",
      "category": "几何装填与覆盖",
      "definition": "Pack n unit equilateral triangles, arbitrary orientations, inside the smallest square.",
      "solution_format": "triangle placements and square side",
      "scalar_objective": "minimum square side",
      "direction": "minimize",
      "configuration_parameters": "n; unit side triangles; rotations allowed",
      "human_baseline": "Friedman’s page gives per-n constructions and named records: Friedman (1996), Maurizio Morandi (2008), with later results; AI involvement unknown.",
      "primary_sources": [
        "https://erich-friedman.github.io/packing/triinsqu/"
      ],
      "verification_cost": "medium",
      "risks": "Page updated in 2026; freeze selected historical instance and confirm exact coordinates; many records are upper bounds only.",
      "recommendation": "后备候选",
      "reason": "Good archived scalar problem and human constructions, pending data extraction and current-best reconciliation.",
      "research_origin": "geometry.json",
      "source_id": "geo-triangles-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T004",
      "name": "Maximum polygon packing (CG:SHOP 2024)",
      "category": "几何装填与覆盖",
      "definition": "Select a subset of given polygonal items and place them inside a container polygon without overlap, using translations only, maximizing the official weight/area objective.",
      "solution_format": "selected polygon IDs and translations",
      "scalar_objective": "total selected item area/weight as defined by challenge",
      "direction": "maximize",
      "configuration_parameters": "official CG:SHOP 2024 item/container instances; no rotation per challenge definition",
      "human_baseline": "Official challenge and paper document 2024 competition, data, ranking, and participating solvers; Shadoks paper describes their feasible solutions. AI involvement unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2024/",
        "https://arxiv.org/abs/2403.16203",
        "https://arxiv.org/abs/2403.20123"
      ],
      "verification_cost": "medium; polygon containment and non-overlap checks",
      "risks": "Confirm official scoring is exactly total area/weight (and all rules); internal optimum NP-hard, so use returned feasible value or valid bound.",
      "recommendation": "后备候选",
      "reason": "Strong competition benchmark; exact task scalar and feasibility semantics must match the 2024 specification.",
      "research_origin": "geometry.json",
      "source_id": "geo-maximum-polygon-packing",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T005",
      "name": "Unequal-circle packing: maximum sum of radii",
      "category": "几何装填与覆盖",
      "definition": "Pack n or a source-defined number of circles in a fixed container, maximizing their total perimeter subject to containment and non-overlap.",
      "solution_format": "circle centers/radii",
      "scalar_objective": "sum_i r_i",
      "direction": "maximize",
      "configuration_parameters": "fixed container and either fixed n or source-defined permitted counts",
      "human_baseline": "Friedman’s catalog lists a ‘Packing Copies to Maximize Total Perimeter’ section, including circles in squares, but specific page outcomes/authors are not verified here; unknown.",
      "primary_sources": [
        "https://www.packomania.com/csqv/csqv.html",
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/36.html"
      ],
      "verification_cost": "medium",
      "risks": "Variable radii/count may be part of optimization; exact source problem needs reading. Do not define own penalty.",
      "recommendation": "MVP候选",
      "reason": "Has a natural scalar and named catalog, but human baseline/details need direct source audit.",
      "research_origin": "geometry.json",
      "source_id": "geo-maximum-circles-perimeter-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T006",
      "name": "Erdős unequal squares: maximum total side length",
      "definition": "在单位正方形中放置 n 个可旋转、大小可不同、内部不重叠的正方形。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "sum_i side_i",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "正方形数量",
        "rotation": "允许任意旋转；平行边子类单列配置"
      },
      "human_baseline": "Halasz (1984)、Erdős–Soifer (1995)、Campbell–Staton (2005) 有显式构造；例如 n=k²+2 的历史下界 k+1/(k+1)。选定非平方数配置后须重建原文布局。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/55.html",
        "https://doi.org/10.1080/00029890.2005.11920180"
      ],
      "verification_cost": "中：多边形相交与边界精确谓词。",
      "risks": "不同于等尺寸正方形装填；历史公式的旋转和零边长约定须锁定。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-free-squares",
      "category": "几何装填与覆盖",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T007",
      "name": "Circles covering circles",
      "category": "几何装填与覆盖",
      "definition": "Place n unit disks to cover the largest possible circular target disk.",
      "solution_format": "unit-disk centers and target radius",
      "scalar_objective": "maximum target radius covered",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "覆盖圆数量",
        "target": "单位圆/单位正方形等各固定配置"
      },
      "human_baseline": "Friedman’s table reports named discoveries and proven records (e.g. Bezdek, Fejes Tóth, Melissen, Tan) for n values, along with a 2026 proof attribution for several; AI involvement is unknown, so historical attribution must not be read as AI-free.",
      "primary_sources": [
        "https://erich-friedman.github.io/packing/circovcir/"
      ],
      "verification_cost": "medium; union containment check and radius calculation; optimality proof hard",
      "risks": "Dynamic page has post-cutoff updates; freeze a dated snapshot and select explicit constructions with machine-readable coordinates if possible.",
      "recommendation": "后备候选",
      "reason": "Strong archive with per-n scalar results and named human construction/proof history.",
      "research_origin": "geometry.json",
      "source_id": "geo-circles-cover-circle",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T008",
      "name": "Covering a square with unit squares",
      "category": "几何装填与覆盖",
      "definition": "Among coverings of a square by n unit squares (overlap allowed), maximize the side of the covered target square.",
      "solution_format": "square placements including orientations",
      "scalar_objective": "maximum target-square side s(n)",
      "direction": "maximize",
      "configuration_parameters": "n; covering squares have side 1; overlap allowed",
      "human_baseline": "Friedman and Paterson’s paper gives constructions/bounds and named sources; known optimality only for n=2,3,5,10 and square n per the survey. Authors of unattributed examples are given; AI involvement unknown.",
      "primary_sources": [
        "https://erich-friedman.github.io/papers/covering/covering.html",
        "https://erich-friedman.github.io/papers/covering.pdf"
      ],
      "verification_cost": "medium; exact coverage of target square requires geometric union check; optimum proofs difficult",
      "risks": "Only keep instances with archived explicit configurations; source says many bounds are not exact optima.",
      "recommendation": "后备候选",
      "reason": "Published named covering problem with natural scalar and identified optimal cases plus constructions.",
      "research_origin": "geometry.json",
      "source_id": "geo-unit-square-cover-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T009",
      "name": "Tammes problem / spherical codes",
      "category": "球面与极值点集",
      "definition": "Place N points on S² to maximize their minimum pairwise angular separation (equivalently chord distance).",
      "solution_format": "N unit vectors",
      "scalar_objective": "minimum pairwise angular distance",
      "direction": "maximize",
      "configuration_parameters": "No admitted v2 configuration. See discovery-only audit; all v1 solved calibration configurations excluded.",
      "human_baseline": "Henry Cohn’s table lists constructions through N=32 with nearest-pair inner products and rattler counts; Sloane’s tables include downloadable coordinates. Records are not all proven optima. Historical human attribution; AI use unknown.",
      "primary_sources": [
        "https://cohn.mit.edu/spherical-codes/",
        "https://neilsloane.com/packings/",
        "https://cohn.mit.edu/sloane/"
      ],
      "verification_cost": "Low for feasibility; global optimality is hard.",
      "risks": "Use a frozen N row and report best-known versus proven status; do not count distinct container variants as separate tasks.",
      "recommendation": "MVP候选",
      "reason": "Named problem, public coordinates, natural scalar.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-tammes",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [
        {
          "task": "T009",
          "config": "Tammes球面S²点数N=8、12",
          "reason": "已证明最优；排除。",
          "sources": [
            "https://cohn.mit.edu/spherical-codes/"
          ]
        }
      ],
      "configuration_parameters_v1": "N; dimension 3 for cited tables",
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T010",
      "name": "Riesz energy minimization on the sphere (Thomson at s=1)",
      "category": "球面与极值点集",
      "definition": "For fixed N points on S², minimize the sum over unordered pairs of distance raised to −s; Thomson is s=1.",
      "solution_format": "N unit vectors / coordinate file",
      "scalar_objective": "Σ(i<j) ||xi−xj||^(−s)",
      "direction": "minimize",
      "configuration_parameters": "N and exponent s; fix s=1 for Thomson",
      "human_baseline": "Cambridge Riesz Energy Database, s=1, lists 53 lowest-known minima for N=512–9913, with energy, symmetry, and downloadable coordinates; N=512 energy 124673.9055677. These are lowest located minima, not all certified global minima. AI use unknown.",
      "primary_sources": [
        "https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/index.html",
        "https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html"
      ],
      "verification_cost": "Low-medium; evaluate all pair terms with suitable precision.",
      "risks": "Freeze N,s and do not call a located minimum globally optimal without proof.",
      "recommendation": "后备候选",
      "reason": "Maintained data has exact coordinate files and natural energy scalar; genuinely different from Tammes.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-riesz",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T011",
      "name": "Minimum-size spherical t-design",
      "category": "球面与极值点集",
      "definition": "For fixed dimension and strength t, find an equal-weight spherical t-design using the fewest points.",
      "solution_format": "point coordinates plus moment identities/certificate",
      "scalar_objective": "number of points N",
      "direction": "minimize",
      "configuration_parameters": "fix dimension d and strength t; S² is the best documented library",
      "human_baseline": "Hardin–Sloane library provides putatively optimal designs and coordinates. Their paper reports a 24-point 7-design first found by McLaren (1963), and records existence/minimal-size claims; it explicitly distinguishes analytic proofs from numerical coordinates. AI use unknown.",
      "primary_sources": [
        "https://neilsloane.com/sphdesigns/",
        "https://cohn.mit.edu/sloane/",
        "https://doi.org/10.1007/BF02711518"
      ],
      "verification_cost": "Medium-high; check all polynomial moments, with exactness needed for a proof.",
      "risks": "Small residual is not proof of exact design or minimum N; choose rows with exact coordinates and lower-bound certificate. Exact moment identities need certificates; approximate designs are a separately named track.",
      "recommendation": "后备候选",
      "reason": "Natural integer objective and public constructions, but per-instance proof/verification burden is high.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-spherical-design",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T012",
      "name": "Maximum-volume polytope with N vertices on a sphere",
      "category": "球面与极值点集",
      "definition": "Choose at most N vertices on the unit sphere in R³ to maximize convex-hull volume.",
      "solution_format": "unit-vector coordinates / named polyhedron",
      "scalar_objective": "convex-hull volume",
      "direction": "maximize",
      "configuration_parameters": "vertex cap N; unit sphere in R³",
      "human_baseline": "Sloane tables include maximal-volume arrangements and downloadable coordinates. A 2026 paper resolves N=9 exactly: volume 3√(2√3−3), attained by a triaugmented triangular prism of specified shape. Human theorem and construction; AI use unknown.",
      "primary_sources": [
        "https://cohn.mit.edu/sloane/",
        "https://arxiv.org/abs/2608.04392"
      ],
      "verification_cost": "Medium to calculate hull volume; optimum proof depends on N.",
      "risks": "Clarify at-most versus exactly N vertices. N=9 is a calibration, not open discovery.",
      "recommendation": "后备候选",
      "reason": "Distinct natural volume objective with an exact value and explicit human construction.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-max-poly-volume",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T013",
      "name": "Heilbronn problem for a free convex region",
      "category": "球面与极值点集",
      "definition": "Place N points in any unit-area convex region to maximize the smallest triangle area among triples, normalized by the convex hull area.",
      "solution_format": "point coordinates",
      "scalar_objective": "minimum triple triangle area divided by convex-hull area",
      "direction": "maximize",
      "configuration_parameters": "N; convex hull is free and normalized to area 1",
      "human_baseline": "Tej Stead’s table provides coordinates and a rational-arithmetic verifier. For N=8, A=0.0800001393294664…; David Cantrell found the construction (2007), and Tej Stead proved optimality (2026). The value is the root of 2060x^5−2332x^4+1064x^3−240x^2+26x−1.",
      "primary_sources": [
        "https://math.tejstead.com/heilbronn/convex/",
        "https://math.tejstead.com/heilbronn/"
      ],
      "verification_cost": "Low for candidate coordinates; upper-bound proof varies by N.",
      "risks": "Living page has later AI-assisted records; use N=8 and label provenance explicitly.",
      "recommendation": "后备候选",
      "reason": "Specific human construction, proof, coordinates, natural scalar.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-heilbronn-free",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T014",
      "name": "Heilbronn triangle problem in a square",
      "category": "球面与极值点集",
      "definition": "Choose n points in a unit square to maximize the area of the smallest triangle determined by any three chosen points.",
      "solution_format": "n point coordinates",
      "scalar_objective": "minimum area over all point triples",
      "direction": "maximize",
      "configuration_parameters": "n; unit square domain",
      "human_baseline": "Tej Stead maintains a dedicated Heilbronn-problem page linked by Friedman’s catalog; this audit did not verify specific authors, numeric records, or downloadable data, so baseline is unknown.",
      "primary_sources": [
        "https://math.tejstead.com/heilbronn/square/",
        "https://github.com/spiralulam/heilbronn"
      ],
      "verification_cost": "low for a given point set (enumerate triples); optimum determination is hard",
      "risks": "An instance is n and domain; published records and coordinate data must be verified before admission. Do not use nested optimum as scorer.",
      "recommendation": "MVP候选",
      "reason": "Natural computable scalar, but the human-baseline requirement is not established by the sources checked.",
      "research_origin": "geometry.json",
      "source_id": "geo-heilbronn-triangle-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "specific_configuration_evidence_located_not_replayed",
      "open_configuration_reviews": [
        {
          "review_id": "R004",
          "task_id": "T014",
          "parameters": {
            "n": 11,
            "domain": "unit square"
          },
          "scalar": "minimum triangle area ↑",
          "human_baseline": "Goldberg 1972: 1/27",
          "frontier_evidence": "record construction; unrestricted optimum not established by checked page",
          "sources": [
            "https://math.tejstead.com/heilbronn/square/"
          ],
          "readiness": "source_located_not_release_ready"
        },
        {
          "review_id": "R005",
          "task_id": "T014",
          "parameters": {
            "n": 12,
            "domain": "unit square"
          },
          "scalar": "minimum triangle area ↑",
          "human_baseline": "Comellas–Yebra 2001: 0.0325988586918196…",
          "frontier_evidence": "record construction; unrestricted optimum not established by checked page",
          "sources": [
            "https://math.tejstead.com/heilbronn/square/"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "excluded_configuration_groups": [
        {
          "task": "T014",
          "config": "上一版Heilbronn正方形n=7、8",
          "reason": "已知最优，排除。较新n=9状态需核查，不自动当open。",
          "sources": [
            "https://math.tejstead.com/heilbronn/square/"
          ]
        }
      ],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T015",
      "name": "Minimum maximum-to-minimum pair-distance ratio",
      "category": "球面与极值点集",
      "definition": "Choose N points in R^d to minimize maximum pair distance divided by minimum pair distance; scale and translation are immaterial.",
      "solution_format": "N coordinates",
      "scalar_objective": "max pair distance / min pair distance",
      "direction": "minimize",
      "configuration_parameters": "N,d; choose 2D N=5 or 7 for proved records",
      "human_baseline": "Friedman’s records state r²=(3+√5)/2 for N=5 and r²=4 for N=7, proved by Bateman and Erdős (1951); N=8 is proved by Bezdek and Fodor (1999). Diagrams are published. Newer rows include 2026 contributors; AI use there unknown.",
      "primary_sources": [
        "https://erich-friedman.github.io/packing/maxmin/",
        "https://doi.org/10.1007/BF02574074"
      ],
      "verification_cost": "Low for a candidate; global optimum proof hard for larger N.",
      "risks": "Do not constrain points to an arbitrary box; avoid recent AI-assisted rows if using a human-only baseline.",
      "recommendation": "后备候选",
      "reason": "Named problem with direct ratio objective and human-proved values.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-minmax-ratio",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T016",
      "name": "Largest small n-gon",
      "category": "球面与极值点集",
      "definition": "Among convex n-gons of diameter at most 1, maximize area.",
      "solution_format": "cyclic vertex coordinates with diameter normalized",
      "scalar_objective": "polygon area",
      "direction": "maximize",
      "configuration_parameters": "n vertices; diameter bound 1; convexity",
      "human_baseline": "Reinhardt (1922) proved regular n-gons optimal for every odd n. Exact/global records also exist for n=4,6,8,10,12; Henrion–Messine used GloptiPoly for n=10,12 with global/numerical guarantees, and Audet et al. gave exact algebraic equations for small even cases.",
      "primary_sources": [
        "https://optimization-online.org/wp-content/uploads/2020/09/8019.pdf",
        "https://arxiv.org/abs/1103.4456",
        "https://www.mcs.anl.gov/~more/cops/bcops/polygon.html"
      ],
      "verification_cost": "Low for area/diameter/convexity; global certificate specialized.",
      "risks": "Choose a fixed n and distinguish proof from local numerical record.",
      "recommendation": "后备候选",
      "reason": "Named extremal task, natural area scalar, many concrete human results.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-largest-small-polygon",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T017",
      "name": "Erdős minimum distinct-distance problem",
      "category": "球面与极值点集",
      "definition": "For a fixed N, choose N distinct planar points that determine as few distinct positive pairwise Euclidean distances as possible.",
      "solution_format": "N point coordinates; normalize by similarity",
      "scalar_objective": "number of distinct pairwise distances",
      "direction": "minimize",
      "configuration_parameters": "N; Euclidean plane; arbitrary point coordinates",
      "human_baseline": "Erdős (1946) introduced D(N). A square lattice construction gives O(N/sqrt(log N)) distinct distances for square-grid sizes; Guth and Katz (Annals 2015) prove every N-point planar set determines at least cN/log N distances. For N=4 a square gives exactly 2 distances and is a simple exact calibration. AI use unknown for historical constructions.",
      "primary_sources": [
        "https://annals.math.princeton.edu/wp-content/uploads/annals-v181-n1-p02-p.pdf"
      ],
      "verification_cost": "Low for a fixed exact/rational coordinate set; global optimum proof is hard.",
      "risks": "A construction yields an upper bound on the minimum, not a proof of optimality. Use exact small-N calibration or compare distinct-distance count only; do not require an uncertified inner optimum.",
      "recommendation": "后备候选",
      "reason": "Distinct natural integer objective and major human construction/theorem history, but public coordinate/result benchmark files were not verified here.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-distinct-distances",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T019",
      "name": "Erdős–Szekeres happy-ending number f(k)",
      "category": "球面与极值点集",
      "definition": "Find the minimum N such that every N points in general position in the plane contain k points in convex position.",
      "solution_format": "For lower-bound witness, coordinates of N−1 points with no convex k-gon; score N−1. Exact f(k) only with matching upper proof.",
      "scalar_objective": "largest point-set size avoiding a convex k-gon",
      "direction": "maximize",
      "configuration_parameters": {
        "convex_subset_size": "k"
      },
      "human_baseline": "Erdős–Szekeres (1935) proved finiteness and conjectured f(k)=2^{k−2}+1; exact f(3)=3 through f(6)=17 are known, with Peters (2006) computer proof for f(6)=17. Suk (2017) gives f(k)=2^{k+o(k)}.",
      "primary_sources": [
        "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0EC7876789232266D60439A4C00D86D9/S144618110000300Xa.pdf/computer_solution_to_the_17point_erdosszekeres_problem.pdf",
        "https://arxiv.org/abs/1604.08657"
      ],
      "verification_cost": "Geometric general-position and convexity checks are low with exact coordinates; upper proof is difficult.",
      "risks": "A lower-bound point set is finite and checkable but does not prove f(k); coordinates may be algebraic and need exact predicates.",
      "recommendation": "后备候选",
      "reason": "Named geometric extremal problem with clear scalar and well-documented historic constructions/proof boundary.",
      "research_origin": "discrete_round2.json",
      "source_id": "happy-ending",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T020",
      "name": "Minimum-dilation triangulation",
      "category": "几何图与计算几何",
      "definition": "For a fixed point set, triangulate it to minimize the maximum ratio of triangulation shortest-path distance to straight-line distance over all point pairs.",
      "solution_format": "triangulation edge list",
      "scalar_objective": "maximum pairwise stretch (dilation)",
      "direction": "minimize",
      "configuration_parameters": "No admitted v2 configuration. See discovery-only audit; all v1 solved calibration configurations excluded.",
      "human_baseline": "UNICAMP archive provides 210 MDTP instances and results for Brandt, Gaiowski, de Rezende, de Souza (2014). Fekete, Keldenich, Perk (SoCG 2025) give exact algorithms and optimal regular n-gon results through n=100, with methods up to 30,000 points.",
      "primary_sources": [
        "https://www.ic.unicamp.br/~cid/Problem-instances/Dilation/MDTP/index.html",
        "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.48",
        "https://arxiv.org/abs/2502.18189"
      ],
      "verification_cost": "Medium-high; all-pairs paths and accurate sums of radicals.",
      "risks": "Do not assume every instance has certified optimum; use published exact instances/results or compare feasible values with bounds.",
      "recommendation": "MVP候选",
      "reason": "Named task has public instance/results packages, substantial human baseline, natural scalar.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-min-dilation-triangulation",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "configuration_parameters_v1": "Point set; 2014 library has 210 instances with 10–70 points",
      "latest_confirmation_status": "excluded_config"
    },
    {
      "id": "T021",
      "name": "Minimum-weight triangulation",
      "category": "几何图与计算几何",
      "definition": "Triangulate a fixed planar point set with straight edges minimizing the sum of edge lengths.",
      "solution_format": "triangulation edge list",
      "scalar_objective": "sum of Euclidean edge lengths",
      "direction": "minimize",
      "configuration_parameters": "point set; no Steiner vertices; hull edges included",
      "human_baseline": "Haas (SoCG 2018) reports certified optima on public benchmark classes up to 30 million uniform/normal points, TSPLIB up to 85,900, and VLSI up to 744,710; earlier Beirouti–Snoeyink exact uniform cases reached 80,000. Human algorithmic records; AI use unknown.",
      "primary_sources": [
        "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2018.44",
        "https://arxiv.org/abs/1802.06415",
        "https://arxiv.org/abs/cs/0601002"
      ],
      "verification_cost": "Medium to compute edge sum; global optimum is NP-hard in general.",
      "risks": "Need match a source instance to its solution/certificate. Never use uncertified inner optimum as answer.",
      "recommendation": "后备候选",
      "reason": "Strong natural task and human results, but this pass did not verify a convenient instance/solution archive.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-min-weight-triangulation",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T022",
      "name": "Minimum convex partition of a point set",
      "category": "几何图与计算几何",
      "definition": "给定平面有限点集，在其凸包内构造无交叉直线图，使每个输入点为顶点且每个有界面凸，不允许Steiner点，最小化有界面数。",
      "solution_format": "noncrossing diagonals or convex piece vertex lists",
      "scalar_objective": "number of convex bounded faces",
      "direction": "minimize",
      "configuration_parameters": {
        "point_set": "固定点集实例；退化、共线、允许边界角等遵循CG:SHOP2020规则"
      },
      "human_baseline": "Published exact and integer-programming formulations exist, but a standardized public instance corpus with per-instance human values was not verified in this audit. Baseline unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2020/",
        "https://arxiv.org/abs/2012.07939"
      ],
      "verification_cost": "Low for checking a proposed partition; proving minimum is harder.",
      "risks": "原代理将点集与polygon版本混写；此处固定为CG:SHOP2020点集版本。不能把允许Steiner点、简单polygon最优剖分等不同问题的基线移来。",
      "recommendation": "后备候选",
      "reason": "Natural scalar exists but public baseline and exact formulation need further source audit.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-min-convex-partition",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T023",
      "name": "Minimum coverage by convex polygons (CG:SHOP 2023)",
      "category": "几何图与计算几何",
      "definition": "Cover a given polygonal region with as few convex polygons as possible under the competition’s exact allowed-piece rules.",
      "solution_format": "list of convex polygon pieces",
      "scalar_objective": "number of convex pieces",
      "direction": "minimize",
      "configuration_parameters": "polygon instance and competition constraints; use official 2023 instances",
      "human_baseline": "Official CG:SHOP 2023 challenge archive reports 22 teams and publishes instances/ranking; Copenhagen identifies William Bille Meyling, Mikkel Abrahamsen, André Nusser as first-place team (announced 2023). AI involvement unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2023/",
        "https://barc.ku.dk/news/bachelor-project-at-barc-wins-computational-geometry-challenge/",
        "https://arxiv.org/abs/2303.07007"
      ],
      "verification_cost": "medium; piece validity/coverage and piece-count checking",
      "risks": "Must reproduce challenge’s exact formulation; objective is a computable count but feasible coverage validation should be robust. Do not use count as an inner optimum oracle.",
      "recommendation": "后备候选",
      "reason": "Public benchmark, official human leaderboard, and an intrinsic integer scalar objective.",
      "research_origin": "geometry.json",
      "source_id": "geo-minimum-convex-cover",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T024",
      "name": "Minimum partition into plane subgraphs (CG:SHOP 2022)",
      "category": "几何图与计算几何",
      "definition": "Partition a geometric graph into the minimum number of planar subgraphs under the official challenge’s edge/vertex rules.",
      "solution_format": "color or partition of input edges into planar classes",
      "scalar_objective": "number of parts/colors",
      "direction": "minimize",
      "configuration_parameters": "official CG:SHOP 2022 graph instances and rule set",
      "human_baseline": "Official CG:SHOP archive states this was the 2022 task; teams published algorithm/ranking materials (e.g. Crombez et al. Shadoks approach). AI involvement unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2022/",
        "https://pageperso.lis-lab.fr/guilherme.fonseca/CGSHOP22slides.pdf"
      ],
      "verification_cost": "medium; crossing checks per part",
      "risks": "Exact task formalization and leaderboard records need confirmation; scalar optimum is hard, score feasible partition’s part count only.",
      "recommendation": "后备候选",
      "reason": "Credible competition task and natural objective, but exact primary-result source and instance scorer need audit.",
      "research_origin": "geometry.json",
      "source_id": "geo-min-partition-plane-subgraphs",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T025",
      "name": "Minimum non-obtuse triangulation (CG:SHOP 2025)",
      "category": "几何图与计算几何",
      "definition": "Triangulate an input point set / polygon with all triangles non-obtuse and minimize the competition-defined triangulation size.",
      "solution_format": "triangle vertex triples",
      "scalar_objective": "number of triangles or Steiner vertices as specified by challenge",
      "direction": "minimize",
      "configuration_parameters": "official CG:SHOP 2025 instances and the precise challenge objective",
      "human_baseline": "A challenge paper is published as ‘Minimum Non-Obtuse Triangulations: The CG:SHOP Challenge 2025’; official CG:SHOP archive should contain results and instances. Specific winners/scores not verified in this audit; AI involvement unknown.",
      "primary_sources": [
        "https://arxiv.org/abs/2504.04412",
        "https://cgshop.ibr.cs.tu-bs.de/"
      ],
      "verification_cost": "medium; angle and triangulation checks",
      "risks": "The competition objective may include Steiner points or other penalties; not admissible until precise scalar and human ranking are independently checked.",
      "recommendation": "后备候选",
      "reason": "Named recent contest problem, but exact objective and human baseline facts remain incomplete.",
      "research_origin": "geometry.json",
      "source_id": "geo-min-nonobtuse-triangulation",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T026",
      "name": "Minimum-area simple polygonalization",
      "category": "几何图与计算几何",
      "definition": "Given a planar point set, choose a simple polygon whose vertex set is exactly the input and minimize its area.",
      "solution_format": "cyclic permutation of point indices",
      "scalar_objective": "polygon area",
      "direction": "minimize",
      "configuration_parameters": "input point set; source datasets FHKPS and GEN; point count fixed per instance",
      "human_baseline": "CG:SHOP 2019 produced a ranking and multiple published teams/algorithms; CG challenge paper (Demaine, Fekete, Keldenich, Krupke, Mitchell, 2022) documents it. Public benchmark site has instance/solution and result files. AI involvement unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2019/",
        "https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Poly/",
        "https://doi.org/10.1145/3504000"
      ],
      "verification_cost": "low; simple polygon check and shoelace area exact for rational input",
      "risks": "NP-hard inner optimum; do not score against purported optimum unless certified. Compare returned polygon’s computable area, or use only benchmark instances with verified optimum values.",
      "recommendation": "后备候选",
      "reason": "Competition gives real human baselines and public data; the scored scalar is the submitted polygon’s directly computable area, not an oracle optimum.",
      "research_origin": "geometry.json",
      "source_id": "geo-area-optimal-polygon-min",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T027",
      "name": "Maximum-area simple polygonalization",
      "category": "几何图与计算几何",
      "definition": "Given a planar point set, choose a simple polygon through every point exactly once that maximizes area.",
      "solution_format": "cyclic permutation of point indices",
      "scalar_objective": "polygon area",
      "direction": "maximize",
      "configuration_parameters": "input point set; FHKPS/GEN benchmark instances",
      "human_baseline": "CG:SHOP 2019 ranking and papers cover Max-Area; public benchmark data includes results and solution permutations. Human team names are available in challenge papers; AI involvement unknown.",
      "primary_sources": [
        "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2019/",
        "https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Poly/",
        "https://doi.org/10.1145/3504000"
      ],
      "verification_cost": "low; simple polygon validation plus shoelace area",
      "risks": "NP-hard inner optimum. Use objective value of feasible returned polygon; comparing gap requires a valid upper bound, never an unverified optimum.",
      "recommendation": "后备候选",
      "reason": "Public human competition results, concrete solutions, and a directly computed natural scalar.",
      "research_origin": "geometry.json",
      "source_id": "geo-area-optimal-polygon-max",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T028",
      "name": "Rectilinear crossing number of K_n",
      "category": "几何图与计算几何",
      "definition": "Place n points in general position in the plane and minimize the number of crossings in the straight-line drawing of K_n.",
      "solution_format": "Exact coordinates or order type; objective number of crossing edge pairs.",
      "scalar_objective": "number of crossings",
      "direction": "minimize",
      "configuration_parameters": {
        "vertices": "n"
      },
      "human_baseline": "Exact values are known through small orders (K_9=36, K_10=62 and published tables extend further); Ábrego–Fernández-Merchant and collaborators maintain best-known bounds and constructions; all exact statuses must be frozen from the survey.",
      "primary_sources": [
        "https://arxiv.org/abs/cs/0009023",
        "https://www.csun.edu/~sf70713/publications/survey.pdf",
        "https://www.crossingnumbers.org/projects/crossingconstants/rectilinear.php"
      ],
      "verification_cost": "Medium for exact coordinates/order type; proving minimum hard.",
      "risks": "Do not merge with topological crossing number; numerical optimization coordinates need exact orientation tests.",
      "recommendation": "后备候选",
      "reason": "Standard well-defined geometric optimization with published record configurations and scalar objective.",
      "research_origin": "discrete_round2.json",
      "source_id": "rectilinear-crossing-kn",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T029",
      "name": "Erdős maximum unit distances for n planar points",
      "category": "几何图与计算几何",
      "definition": "Maximize the number of unit-distance pairs among n distinct points in the Euclidean plane.",
      "solution_format": "Exact-coordinate point set; objective unit-distance pair count.",
      "scalar_objective": "number of unit-distance pairs",
      "direction": "maximize",
      "configuration_parameters": {
        "points": "n"
      },
      "human_baseline": "Alexeev, Mixon & Parshall (2024/2025) report that for n≤21 their upper bounds match best-known lower bounds and fully enumerate densest unit-distance graphs; exact values are thus recorded through 21. No claim about AI-generated or later constructions is used as human baseline.",
      "primary_sources": [
        "https://arxiv.org/abs/2412.11914"
      ],
      "verification_cost": "Witness edge count is checkable with exact algebraic coordinates; global maximum is hard beyond small n.",
      "risks": "Distinguish exact n≤21 values from open larger n and avoid scoring floating-point near-unit distances; freeze the 2024/2025 paper version and accompanying data.",
      "recommendation": "后备候选",
      "reason": "Strong finite exact table through n=21, but a changing frontier and exact-coordinate validation are material.",
      "research_origin": "discrete_round2.json",
      "source_id": "unit-distance",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "specific_configuration_evidence_located_not_replayed",
      "open_configuration_reviews": [
        {
          "review_id": "R006",
          "task_id": "T029",
          "parameters": {
            "n": 25
          },
          "scalar": "number of unit-distance pairs ↑",
          "human_baseline": "Engel et al. human construction:72",
          "frontier_evidence": "agent reports current interval72–73; current certificate ledger needs root replay and provenance freeze",
          "sources": [
            "https://arxiv.org/abs/2406.15317",
            "https://artwaste.land/strata/every-edge-but-one/"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T030",
      "name": "Orchard planting / maximum 3-rich lines",
      "category": "几何图与计算几何",
      "definition": "给定N个互异实平面点，最大化恰好包含三个输入点的不同直线数；允许三点共线，不能施加“任意三点不共线”的一般位置条件。",
      "solution_format": "point coordinates and counted lines",
      "scalar_objective": "number of distinct lines containing exactly three input points",
      "direction": "maximize",
      "configuration_parameters": {
        "N": "输入点数",
        "coordinates": "整数、有理或精确代数数表示需固定"
      },
      "human_baseline": "Sloane’s A003035 table gives values (e.g. N=7→6, 11→16, 14→26); cubic-curve constructions by Burr, Grünbaum and Sloane provide explicit examples. 2026 work gives t3(15)=31 and excludes 32 with a certificate. Historical human constructions; newer computational component identified.",
      "primary_sources": [
        "https://arxiv.org/abs/1208.4714",
        "https://oeis.org/A003035"
      ],
      "verification_cost": "Medium; exact collinearity/incidence checks.",
      "risks": "恰好3点的直线不等于所有至少3点的直线；源数据的共线约定必须一致。相等/共线关系需精确谓词。",
      "recommendation": "后备候选",
      "reason": "Named integer optimization and public historical values, but a reusable coordinate record for exact selected N needs audit.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-orchard",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T031",
      "name": "No-three-in-line maximum on an n×n grid",
      "category": "几何图与计算几何",
      "definition": "Select as many lattice points as possible from [n]×[n] with no three collinear.",
      "solution_format": "Grid point list; objective cardinality.",
      "scalar_objective": "number of selected points",
      "direction": "maximize",
      "configuration_parameters": {
        "grid_order": "n"
      },
      "human_baseline": "Dudeney posed the problem; constructions of 2n points are known for many n, but the universal 2n conjecture remains open. Wolfram/House of Graphs style databases list configurations; exact finite maxima are only known for selected small n, so a primary record source must be frozen.",
      "primary_sources": [
        "https://arxiv.org/abs/2209.01447"
      ],
      "verification_cost": "Low for collinearity checks; optimum proof hard.",
      "risks": "Recent preprints and recreational databases may contain construction records without optimality proofs; label upper/lower status carefully.",
      "recommendation": "后备候选",
      "reason": "Clear scalar and established construction tradition, but candidate records need more authoritative curation.",
      "research_origin": "discrete_round2.json",
      "source_id": "no-three-in-line",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T032",
      "name": "Simple perfect squared squares: minimum primitive side at fixed order",
      "category": "铺砌与分割",
      "definition": "固定小正方形数量N，将一个整数边长正方形分割为边长互不相同的小正方形，要求simple、所有边长gcd=1，最小化外框边长。",
      "solution_format": "Bouwkamp code or exact tile placements",
      "scalar_objective": "primitive outer-square side length",
      "direction": "minimize",
      "configuration_parameters": {
        "N": "固定order，例如21校准、55历史构造轨"
      },
      "human_baseline": "Duijvestijn (1978)：N21唯一构造primitive side112，已知最优校准。Squaring.net order55页列 Bernard Moss (2020) side740 的历史构造；本次未下载重算。",
      "primary_sources": [
        "https://www.squaring.net/sq/ss/spss/o21/spsso21.html",
        "https://www.squaring.net/sq/ss/spss/o55/spsso55.html",
        "https://www.squaring.net/downloads/downloads.html~"
      ],
      "verification_cost": "Low-medium; exact integer tiling and distinct sizes; global proof is enumeration-based.",
      "risks": "不是把固定目标最低order21当可持续发现任务；须验证Bouwkamp码、simple条件与gcd；side740仅历史baseline。",
      "recommendation": "MVP候选",
      "reason": "Named dissection, exact natural integer objective, public construction code, proof of minimality.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-perfect-squared-square",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "specific_configuration_evidence_located_not_replayed",
      "open_configuration_reviews": [
        {
          "review_id": "R007",
          "task_id": "T032",
          "parameters": {
            "order": 55
          },
          "scalar": "primitive outer side ↓",
          "human_baseline": "Bernard Moss 2020:740",
          "frontier_evidence": "smallest known, not proved minimum; Bouwkamp file located not replayed",
          "sources": [
            "https://www.squaring.net/sq/ss/spss/o55/spsso55.html"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "excluded_configuration_groups": [
        {
          "task": "T032",
          "config": "order=21, primitive side=112",
          "reason": "唯一最小阶简单完美平方分割；移除这一配置，order55另审。",
          "sources": [
            "https://www.squaring.net/sq/ss/spss/o21/spsso21.html"
          ]
        }
      ],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T033",
      "name": "Mrs. Perkins’s quilt",
      "category": "铺砌与分割",
      "definition": "For fixed n×n square, dissect into the fewest smaller integer-sided squares whose side lengths have gcd 1.",
      "solution_format": "integer square tiling / side lengths and positions",
      "scalar_objective": "number of smaller squares",
      "direction": "minimize",
      "configuration_parameters": "Fix outer side n; integer alignment; tile-side gcd 1",
      "human_baseline": "For n=13, the catalogue gives an optimal 11-square dissection with sides 1,1,2,2,2,3,3,4,6,6,7; no fewer than 11 is possible. Squaring.net lists results through n=120, while warning most later rows are best known rather than proven. Conway, Guy, Gay, Pegg and computer searches are documented.",
      "primary_sources": [
        "https://www.squaring.net/sq/ss/quilts/mrs-perkins-quilts.html",
        "https://mathworld.wolfram.com/MrsPerkinssQuilt.html"
      ],
      "verification_cost": "Low for a proposed tiling/gcd; exact minimality varies by n.",
      "risks": "Use proven n=13 calibration; do not claim later best-known values are optimal.",
      "recommendation": "后备候选",
      "reason": "Explicit human layout, natural integer objective, clear proof status.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-mrs-perkins",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T034",
      "name": "Klarner order of a polyomino",
      "category": "铺砌与分割",
      "definition": "For a fixed polyomino P, find the fewest congruent copies (translations, rotations, reflections allowed) that tile any rectangle.",
      "solution_format": "rectangle dimensions and copy placements",
      "scalar_objective": "minimum number of copies of P",
      "direction": "minimize",
      "configuration_parameters": "fixed polyomino shape; allowed orientations stated",
      "human_baseline": "polyominoes.org lists P-pentomino order 2 and an explicit 2×5 tiling. The Handbook of Discrete and Computational Geometry defines order and records a Y-pentomino’s 5×10 rectangle (10 copies), with results by Klarner and Reid.",
      "primary_sources": [
        "https://polyominoes.org/data/5P",
        "https://www.csun.edu/~ctoth/Handbook/chap14.pdf",
        "https://sicherman.net/mikereid/p5_rect.html"
      ],
      "verification_cost": "Low for a placement; proving no smaller order may require exhaustive search.",
      "risks": "Shape P is an instance parameter; P-pentomino order 2 is trivial. Use only a nontrivial shape with source-supported minimality.",
      "recommendation": "后备候选",
      "reason": "Named scalar problem and constructions exist, but candidate shapes and optimality evidence require selection.",
      "research_origin": "geometry_round2.json",
      "source_id": "geo2-polyomino-order",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T035",
      "name": "(d,g)-cage order",
      "category": "极值图与超图",
      "definition": "For fixed degree d and girth g, find the smallest order n of a d-regular graph of girth exactly g.",
      "solution_format": "Adjacency list/matrix of a d-regular graph with a verifiable girth certificate; objective is vertex count.",
      "scalar_objective": "number of vertices n",
      "direction": "minimize",
      "configuration_parameters": {
        "degree": "d",
        "girth": "g"
      },
      "human_baseline": "Exoo, Jajcay, Goedgebeur et al. (2025 preprint) improved eleven upper bounds; e.g. n(4,10)≤320. Exoo–Jajcay (2013) survey distinguishes known cages from upper-bound constructions; optimality is proved only for some parameter pairs.",
      "primary_sources": [
        "https://arxiv.org/abs/2511.07247",
        "https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS16"
      ],
      "verification_cost": "Medium for a supplied graph; high to prove global minimality.",
      "risks": "Report incumbent order separately from proven minimum; exact optimality certificates are often absent.",
      "recommendation": "后备候选",
      "reason": "Natural scalar objective, rich named record tables, and independently checkable graph witnesses.",
      "research_origin": "discrete.json",
      "source_id": "graph-cage",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "specific_configuration_evidence_located_not_replayed",
      "open_configuration_reviews": [
        {
          "review_id": "R008",
          "task_id": "T035",
          "parameters": {
            "degree": 4,
            "girth": 10
          },
          "scalar": "vertex count ↓",
          "human_baseline": "Exoo et al. 2025/2026:320",
          "frontier_evidence": "paper interval243–320; obtain320-vertex graph before admitting",
          "sources": [
            "https://arxiv.org/abs/2511.07247"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T036",
      "name": "Degree–diameter problem",
      "category": "极值图与超图",
      "definition": "For maximum degree d and diameter k, maximize the order of a simple graph.",
      "solution_format": "Graph adjacency list plus proof/check of maximum degree and diameter; objective vertex count.",
      "scalar_objective": "number of vertices n",
      "direction": "maximize",
      "configuration_parameters": {
        "maximum_degree": "d",
        "diameter": "k"
      },
      "human_baseline": "The large degree/diameter graph table (Miller, Širáň and contributors; updated tables) records best known orders and marks the few proven optimal cases; Moore bound is an upper bound, not an attained baseline.",
      "primary_sources": [
        "https://doi.org/10.17632/d75dzbjd4k.3"
      ],
      "verification_cost": "Medium for witness; exact optimum usually unknown.",
      "risks": "Must label best-known vs proven; table updates and graph conventions (regular vs maximum degree) need freezing.",
      "recommendation": "后备候选",
      "reason": "A clear extremal objective and extensive human constructions; feasible to score witness size.",
      "research_origin": "discrete.json",
      "source_id": "degree-diameter",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T037",
      "name": "Zarankiewicz number Z_{s,t}(m,n)",
      "category": "极值图与超图",
      "definition": "固定左右部大小m,n，构造二部图，禁止存在s个左顶点与t个右顶点形成完整二部子图，最大化边数。若同时禁止交换角色的情形，须单列配置。",
      "solution_format": "Bipartite adjacency matrix; objective number of 1 entries.",
      "scalar_objective": "number of edges",
      "direction": "maximize",
      "configuration_parameters": {
        "part_sizes": "m,n",
        "forbidden_biclique": "s,t"
      },
      "human_baseline": "Published exact values and bounds are surveyed in the extremal graph literature; small square cases have SAT-verified tables (Mubayi et al. / 2022 SAT study corrects known table errors). Explicit finite-field constructions give human lower bounds.",
      "primary_sources": [
        "https://arxiv.org/abs/2203.02283",
        "https://arxiv.org/abs/2202.05507",
        "https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/BGKRSW96/bgkrsw96.pdf"
      ],
      "verification_cost": "Medium for forbidden biclique and edge count; optimality high.",
      "risks": "Older tables contain errors; pin a source version and instance. General asymptotics remain open.",
      "recommendation": "后备候选",
      "reason": "Clean extremal scalar, abundant constructions, and small instances admit exact machine checks.",
      "research_origin": "discrete.json",
      "source_id": "zaran-bipartite",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T038",
      "name": "Forbidden-subgraph extremal number ex(n,F)",
      "definition": "固定 n 与有限禁止图族 F，构造 F-free 简单图。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "number of edges",
      "direction": "maximize",
      "configuration_parameters": "No admitted v2 configuration. See discovery-only audit; all v1 solved calibration configurations excluded.",
      "human_baseline": "Afzaly–McKay 公开 sparse6 构造表：ex(10,C4)=16；禁止 C3,C4 时 n=10 的构造为15条边。较大行区分最优与仅下界。",
      "primary_sources": [
        "https://users.cecs.anu.edu.au/~bdm/data/extremal.html"
      ],
      "verification_cost": "低至中；固定小 F 的子图检查。",
      "risks": "高阶 F 或很大 n 会使验证昂贵；Zarankiewicz 的二部限制与此相关，按族分层汇总。",
      "recommendation": "MVP候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-forbidden-graph",
      "category": "极值图与超图",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [
        {
          "task": "T038",
          "config": "n=30,F={C4}边85；n=30,F={C3,C4}边76",
          "reason": "Afzaly–McKay对应项标为精确极值，并非仅构造下界；移除这些小配置。",
          "sources": [
            "https://users.cecs.anu.edu.au/~bdm/data/extremal.html"
          ]
        }
      ],
      "configuration_parameters_v1": {
        "n": "顶点数",
        "F": "例如 {C4} 或 {C3,C4}，作为配置"
      },
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T039",
      "name": "Graph saturation number sat(n,F)",
      "category": "极值图与超图",
      "definition": "Minimize edges in an n-vertex F-saturated graph: it is F-free, but adding any missing edge creates F.",
      "solution_format": "Graph adjacency list; objective edge count.",
      "scalar_objective": "number of edges",
      "direction": "minimize",
      "configuration_parameters": {
        "vertices": "n",
        "forbidden_graph": "F"
      },
      "human_baseline": "Bollobás (1965) initiated the problem; for cliques, classical constructions and recent papers give exact formulas for many ranges. Current papers state the standard definition and bounds.",
      "primary_sources": [
        "https://arxiv.org/abs/2605.07179"
      ],
      "verification_cost": "Medium for candidate; exact optimum often requires proof.",
      "risks": "Newer specific F parameter results must be checked against publication status; easy families have formulaic answers.",
      "recommendation": "后备候选",
      "reason": "Natural minimization objective with established theory; curate a small frozen set of nontrivial F,n cases.",
      "research_origin": "discrete.json",
      "source_id": "saturation",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T040",
      "name": "Classical Ramsey number lower-bound construction",
      "category": "极值图与超图",
      "definition": "For fixed s,t, construct the largest N-vertex graph with neither an s-clique nor an independent t-set, equivalently improve the lower bound R(s,t)≥N+1.",
      "solution_format": "Graph adjacency list; independently verify forbidden-clique/independent-set conditions; scalar N.",
      "scalar_objective": "number of vertices N",
      "direction": "maximize",
      "configuration_parameters": {
        "s,t": "禁止clique与independent set大小；图Ramsey扩展另作为有关联配置，不重复立项"
      },
      "human_baseline": "Exoo et al. (1997) catalogued 656 nonisomorphic (5,5,42)-graphs, implying R(5,5)≥43; Radziszowski Dynamic Survey rev. 18 (2026) records 43≤R(5,5)≤46, with the upper bound by Angeltveit–McKay (2024).",
      "primary_sources": [
        "https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf",
        "https://users.cecs.anu.edu.au/~bdm/data/ramsey.html",
        "https://arxiv.org/abs/2409.15709"
      ],
      "verification_cost": "High; exact clique and independence checks scale exponentially, though certificates are finite and reproducible.",
      "risks": "A one-unit increase is meaningful but only if exact validation is performed; do not score heuristic estimates or claim exact Ramsey values from a lower-bound witness.",
      "recommendation": "后备候选",
      "reason": "Excellent human baseline and natural scalar, but restrict to modest s,t and require exact verifier/certificate.",
      "research_origin": "discrete.json",
      "source_id": "classical-ramsey",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T041",
      "name": "Hypergraph Turán number ex_r(n,F)",
      "category": "极值图与超图",
      "definition": "Maximize edges in an r-uniform n-vertex hypergraph avoiding a fixed forbidden r-graph F.",
      "solution_format": "List of r-subsets; objective edge count.",
      "scalar_objective": "number of hyperedges",
      "direction": "maximize",
      "configuration_parameters": {
        "uniformity": "r",
        "vertices": "n",
        "forbidden_hypergraph": "F"
      },
      "human_baseline": "Keevash's survey and the Erdős problems archive record open cases and constructions. The 3-uniform K4 problem has Turán's construction at density 5/9, but exact density remains open; finite n entries can have exact/conjectured distinctions.",
      "primary_sources": [
        "https://people.maths.ox.ac.uk/keevash/papers/turan-survey.pdf",
        "https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/ExactHypergraphTuranT3n4.html"
      ],
      "verification_cost": "High; checking F-freeness is manageable for small n, global optimality is difficult.",
      "risks": "Do not blur finite exact values with asymptotic Turán density; choose frozen small n and explicit F.",
      "recommendation": "后备候选",
      "reason": "Canonical research problem with natural edge-count objective and published constructions/bounds.",
      "research_origin": "discrete.json",
      "source_id": "turan-hypergraph",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T042",
      "name": "Erdős–Rogers function f_{s,t}(n)",
      "category": "极值图与超图",
      "definition": "固定2≤s<t与n，在n顶点K_t-free图G中，最小化α_s(G)，其中α_s(G)是G中诱导子图不含K_s的最大顶点集大小。s=2时α_2是独立数。",
      "solution_format": "图G；有限小规模下由独立精确算法计算α_s，或提交相应可检查证书。",
      "scalar_objective": "α_s(G)=max{|U|:G[U] is K_s-free}",
      "direction": "minimize",
      "configuration_parameters": {
        "vertices": "n",
        "forbidden_clique": "s",
        "independent_set_forbidden_size": "t (target alpha < t)"
      },
      "human_baseline": "Erdős–Rogers introduced the function; extensive probabilistic and explicit bounds are surveyed in recent graph Ramsey literature. Specific finite graph records need source-level validation before use.",
      "primary_sources": [
        "https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf"
      ],
      "verification_cost": "高：内层最大子集问题通常指数复杂；仅限能精确求解的小配置，不进MVP。",
      "risks": "原代理误写为K_s-free图上最大独立数（空图平凡达到n），此处已修为标准Erdős–Rogers最小化问题；须同时验证K_t-free与内层α_s。",
      "recommendation": "后备候选",
      "reason": "A recognized graph extremal function with natural scalar, but poor witness-only evaluation and no curated finite database confirmed.",
      "research_origin": "discrete_round2.json",
      "source_id": "erdos-rogers",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T043",
      "name": "Minimum triangles at fixed edge count",
      "definition": "固定 n,m，输出恰有 m 条边的简单图，使三角形数最少。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "triangle count",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "顶点数",
        "m": "边数"
      },
      "human_baseline": "Razborov (2008) 的三角形密度定理及 Lovász–Simonovits 构造提供经典基线；非平凡有限 n,m 的显式构造与可达边数须逐项固定。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/46.html",
        "https://people.cs.uchicago.edu/~razborov/files/triangles.pdf"
      ],
      "verification_cost": "低：精确数三角形。",
      "risks": "渐近最优密度不是每个有限配置的最优值；不得用 asymptotic 数字冒充精确基线。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-min-triangles",
      "category": "极值图与超图",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T044",
      "name": "Optimal Golomb ruler length",
      "category": "加法组合与离散构造",
      "definition": "For m integer marks, place distinct marks so all positive pairwise differences are distinct and minimize the largest mark.",
      "solution_format": "Increasing integer mark list starting at 0; objective final mark.",
      "scalar_objective": "ruler length",
      "direction": "minimize",
      "configuration_parameters": "No admitted v2 configuration. See discovery-only audit; all v1 solved calibration configurations excluded.",
      "human_baseline": "Shearer (1990) exhaustively proved optimal lengths 127,151,177 for m=14,15,16; distributed.net completed proof of optimality through m=28 (2022 records), and CSPLib has the standard benchmark. Distinguish proven optima from larger-m best known rulers.",
      "primary_sources": [
        "https://research.ibm.com/publications/some-new-optimum-golomb-rulers",
        "https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob006/",
        "https://distributed.net/ogr/"
      ],
      "verification_cost": "Low for ruler; optimality proof high for large m.",
      "risks": "Open sizes beyond proven range must be scored as incumbent length, not as proven optimum; preserve provenance and certificate status.",
      "recommendation": "MVP候选",
      "reason": "Ideal scalar objective, a standard benchmark and exceptionally clear historical human record.",
      "research_origin": "discrete.json",
      "source_id": "golomb-ruler",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [
        {
          "task": "T044",
          "config": "Golomb标记数m<=28，包括上一版m=10,12",
          "reason": "已证明最优，排除。m>28仅作替代候选，需逐项定位现纪录。",
          "sources": [
            "https://blogs.distributed.net/2022/11/"
          ]
        }
      ],
      "configuration_parameters_v1": {
        "marks": "m"
      },
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T045",
      "name": "Minimum diameter of a B_h set of integers, h≥3",
      "category": "加法组合与离散构造",
      "definition": "For fixed m and h≥3, choose m integers with all h-term sums (repetition convention fixed) distinct, minimizing the diameter.",
      "solution_format": "Sorted integer set; objective maximum minus minimum.",
      "scalar_objective": "diameter",
      "direction": "minimize",
      "configuration_parameters": {
        "set_size": "m",
        "sum order": "h≥3",
        "repetitions": "fixed by benchmark"
      },
      "human_baseline": "Bose–Chowla (1962) give finite-field B_h constructions; modern additive-combinatorics papers provide bounds. The h=2 case is the Golomb/Sidon ruler task and is deliberately excluded here as a duplicate.",
      "primary_sources": [
        "https://doi.org/10.1007/BF02566968",
        "https://arxiv.org/abs/2104.12711"
      ],
      "verification_cost": "Low for witness; exact optimum difficult.",
      "risks": "Must distinguish unordered multisets with repetitions from distinct-element sums and from modular B_h sets; h=2 merges with Golomb rulers.",
      "recommendation": "后备候选",
      "reason": "Natural generalization with human algebraic constructions; finite exact baselines need dedicated verification.",
      "research_origin": "discrete_round2.json",
      "source_id": "bh-ruler-higher",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T046",
      "name": "Difference triangle sets",
      "category": "加法组合与离散构造",
      "definition": "Construct several rows of marks with all within-row positive differences distinct globally; minimize maximum span under fixed row/mark counts.",
      "solution_format": "Rows of integer marks; objective maximum row span.",
      "scalar_objective": "maximum span",
      "direction": "minimize",
      "configuration_parameters": {
        "rows": "r",
        "marks_per_row": "m"
      },
      "human_baseline": "Published difference-triangle-set constructions and tabu search literature report best-known spans; Golomb rulers are the one-row special case.",
      "primary_sources": [
        "https://doi.org/10.1016/j.cor.2004.11.002",
        "https://cs.uwaterloo.ca/~vanbeek/Publications/sillito.pdf"
      ],
      "verification_cost": "Low for a witness.",
      "risks": "Overlaps Golomb ruler at r=1; careful definition variants (all differences vs row-tagged) must be frozen.",
      "recommendation": "后备候选",
      "reason": "A legitimate adjacent optimization family with published records, but merge one-row case into Golomb rulers.",
      "research_origin": "discrete.json",
      "source_id": "difference-triangle",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T047",
      "name": "Maximum cap set in F_3^n",
      "category": "加法组合与离散构造",
      "definition": "Find a largest subset of the vector space F_3^n containing no affine line (three distinct points summing to zero).",
      "solution_format": "Point list in F_3^n; objective cardinality.",
      "scalar_objective": "number of points",
      "direction": "maximize",
      "configuration_parameters": {
        "dimension": "n"
      },
      "human_baseline": "Pellegrino (1970) proved maximum 20 for n=4. Kleinberg–Sawin–Speyer (2016) gave constructions and Ellenberg–Gijswijt (2017) exponential upper bound; human lower-bound records are published for higher n, with exact values limited.",
      "primary_sources": [
        "https://doi.org/10.4007/annals.2017.185.1.8",
        "https://arxiv.org/abs/1605.09223"
      ],
      "verification_cost": "Low for witness and no-line property; proving optimality difficult.",
      "risks": "Modern record tables may have changed; distinguish exact small dimensions from best-known lower bounds.",
      "recommendation": "后备候选",
      "reason": "Canonical additive extremal problem, clear point-count objective, and unusually visible human construction frontier.",
      "research_origin": "discrete.json",
      "source_id": "cap-set",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T048",
      "name": "Largest 3-term-progression-free subset of [n]",
      "category": "加法组合与离散构造",
      "definition": "Find a largest subset of {1,…,n} containing no nontrivial 3-term arithmetic progression.",
      "solution_format": "Integer set; objective cardinality.",
      "scalar_objective": "set cardinality",
      "direction": "maximize",
      "configuration_parameters": {
        "interval_length": "n"
      },
      "human_baseline": "Behrend (1946) gave classical constructions; exact small-n values are known computationally and Roth's theorem gives qualitative upper bounds. Pin exact-value source/version for each n.",
      "primary_sources": [
        "https://doi.org/10.1073/pnas.32.12.331"
      ],
      "verification_cost": "Low for witness, exponential for maximality.",
      "risks": "Closely related to cap sets but distinct ambient group; avoid treating parameter variants as different tasks.",
      "recommendation": "后备候选",
      "reason": "Natural cardinality objective, but benchmark exact records need authoritative tables and manageable n.",
      "research_origin": "discrete.json",
      "source_id": "progression-free",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T049",
      "name": "Minimum difference basis for [n]",
      "category": "加法组合与离散构造",
      "definition": "Find a smallest set A of integers such that every integer 1,…,n is a difference of two elements of A.",
      "solution_format": "Sorted integer set; objective cardinality (or span if a different canonical version is chosen).",
      "scalar_objective": "number of elements of A",
      "direction": "minimize",
      "configuration_parameters": {
        "target_interval": "n",
        "ambient_domain": "integer interval, fixed convention"
      },
      "human_baseline": "Rédei–Rényi and Leech difference-basis constructions; the prior finite witness at n=6166 has128 marks, giving128²/6166≈2.6571. Original128-element list still needs retrieval; not a same-config value for all n.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/7.html",
        "https://arxiv.org/html/2511.02864v1#S6.SS3"
      ],
      "verification_cost": "Low for coverage; proving minimality difficult.",
      "risks": "Several inequivalent definitions (difference set vs difference basis, interval endpoint, signed differences); human baseline source requires additional research.",
      "recommendation": "后备候选",
      "reason": "Natural minimum-cardinality task but needs definition and authoritative record table curation.",
      "research_origin": "discrete.json",
      "source_id": "difference-basis",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T051",
      "name": "Schur number S(k) lower-bound coloring",
      "category": "加法组合与离散构造",
      "definition": "For fixed k colors, construct a coloring of [N] with no monochromatic x+y=z; maximize N, the certified lower bound for S(k).",
      "solution_format": "Color assignment [N]→[k] with exact check of all x+y=z; scalar N.",
      "scalar_objective": "largest colorable N",
      "direction": "maximize",
      "configuration_parameters": {
        "colors": "k"
      },
      "human_baseline": "Heule (AAAI 2018) proved S(5)=160 using a DRAT-certified SAT computation; S(6)≥536 and S(7)≥1680 are cited constructions by Fredricksen–Sweet (2000). Schur numbers S(1..4)=1,4,13,44 are exact.",
      "primary_sources": [
        "https://ojs.aaai.org/index.php/AAAI/article/download/12209/12068",
        "https://www.cs.utexas.edu/~marijn/Schur/"
      ],
      "verification_cost": "Low for lower-bound coloring; proving exact value needs a large SAT/DRAT proof.",
      "risks": "Score a coloring's N only, not an exact S(k) claim absent an upper proof; weak Schur numbers are a separate convention and should be excluded/merged only by explicit scope.",
      "recommendation": "后备候选",
      "reason": "Canonical extremal coloring task with explicit human witnesses, exact small values, and strong proof artifacts.",
      "research_origin": "discrete_round2.json",
      "source_id": "schur-number",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T052",
      "name": "van der Waerden number lower-bound coloring",
      "category": "加法组合与离散构造",
      "definition": "For fixed r colors and AP length k, construct the longest r-coloring of [N] with no monochromatic k-term arithmetic progression.",
      "solution_format": "Coloring of [N]; scalar N.",
      "scalar_objective": "largest AP-free coloring order N",
      "direction": "maximize",
      "configuration_parameters": {
        "colors": "r",
        "progression_length": "k"
      },
      "human_baseline": "Marijn Heule's 2005 EJC survey/paper tables W(2,5)=178, W(2,6)=1132 and many best known lower-bound colorings; Berlekamp (1968) and later recurrence constructions provide explicit records.",
      "primary_sources": [
        "https://www.cs.utexas.edu/~marijn/publications/waerden.pdf",
        "https://arxiv.org/abs/1705.09673",
        "https://www.combinatorics.org/ojs/index.php/eljc/article/view/v18i1p64"
      ],
      "verification_cost": "Low for a coloring witness by enumerating arithmetic progressions; upper/exact proof is costly.",
      "risks": "Closely related to Ramsey lower-bound construction but a distinct named AP-avoidance family; freeze coloring convention and don't label lower bounds as exact W(r,k).",
      "recommendation": "后备候选",
      "reason": "Natural construction objective with published numerical records and cheap witness validation.",
      "research_origin": "discrete_round2.json",
      "source_id": "van-der-waerden-lower",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T053",
      "name": "Longest finite sequence with discrepancy at most C",
      "category": "加法组合与离散构造",
      "definition": "For a fixed discrepancy cap C, find the largest prefix length N of a ±1 sequence such that every homogeneous initial segment along every arithmetic progression has absolute sum at most C.",
      "solution_format": "Sign sequence of length N; exact scalar N.",
      "scalar_objective": "sequence length N",
      "direction": "maximize",
      "configuration_parameters": {
        "discrepancy_cap": "C"
      },
      "human_baseline": "Konev–Lisitsa (2015) reported a discrepancy-3 sequence of length 127,645, improving 17,000, with inductive construction rules; Tao (2015) proved the infinite Erdős discrepancy conjecture.",
      "primary_sources": [
        "https://arxiv.org/abs/1407.2510",
        "https://arxiv.org/abs/1509.05363"
      ],
      "verification_cost": "Low for a supplied finite sequence; proving maximality requires exhaustive/combinatorial upper certificates.",
      "risks": "The unbounded infinite theorem itself is not a finite optimization task; freeze exact prefix discrepancy convention and evaluate witness length only.",
      "recommendation": "后备候选",
      "reason": "A named finite extremal version has a concrete human record and exact scalar witness.",
      "research_origin": "discrete_round2.json",
      "source_id": "erdos-discrepancy-finite",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T054",
      "name": "Largest square-difference-free subset of [N]",
      "category": "加法组合与离散构造",
      "definition": "Maximize |A| for A⊂[N] with no distinct a,b∈A such that |a−b| is a perfect square.",
      "solution_format": "Integer set; objective cardinality.",
      "scalar_objective": "number of elements",
      "direction": "maximize",
      "configuration_parameters": {
        "interval_length": "N"
      },
      "human_baseline": "Ruzsa (1984) gave an explicit construction of square-difference-free sets; Green–Sawhney (preprint 2024, updated 2025) prove |A|≪N exp(−c√log N). These are asymptotic bounds, not exact finite-N maxima.",
      "primary_sources": [
        "https://doi.org/10.1007/BF02454169",
        "https://arxiv.org/abs/2411.17448"
      ],
      "verification_cost": "Low for a finite set; proof of maximum difficult.",
      "risks": "Asymptotic rather than exact finite record frontier; parameters N give highly correlated instances.",
      "recommendation": "后备候选",
      "reason": "Strong named extremal family and human constructions, but current upper-bound citation needs verification and finite record table.",
      "research_origin": "discrete_round2.json",
      "source_id": "furstenberg-sarkozy",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T055",
      "name": "Finite-set sum–product growth minimization",
      "category": "加法组合与离散构造",
      "definition": "固定集合大小m与环境环R（有限域F_p或有坐标界的整数），构造A⊂R、|A|=m，最小化max(|A+A|,|A·A|)。",
      "solution_format": "Finite integer set A; objective the larger of sumset/product-set cardinalities.",
      "scalar_objective": "max(|A+A|,|A·A|)",
      "direction": "minimize",
      "configuration_parameters": {
        "m": "集合大小",
        "R": "F_p及素数p，或整数及坐标上界B"
      },
      "human_baseline": "Erdős–Szemerédi (1983) established a power-growth theorem for integer sets; later Solymosi and others improve exponents. No canonical exact finite-n construction table for this min-max objective was verified in this pass.",
      "primary_sources": [
        "https://annals.math.princeton.edu/2003/157-3/p07",
        "https://arxiv.org/abs/math/0402285",
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/45.html"
      ],
      "verification_cost": "Low for a finite set and exact integer operations; global optimum hard.",
      "risks": "Integer interval bound B affects the problem substantially and may be artificial; no verified human optimum table. Restrict to conditional exploratory instances only.",
      "recommendation": "后备候选",
      "reason": "A real finite optimization scalar, but a standardized published finite benchmark frontier was not confirmed.",
      "research_origin": "discrete_round2.json",
      "source_id": "sum-product-growth",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T056",
      "name": "Minimum finite-field Kakeya set size",
      "category": "加法组合与离散构造",
      "definition": "For fixed finite field F_q and dimension d, minimize |K| over K⊂F_q^d containing a full affine line in every direction.",
      "solution_format": "Point list or characteristic function; objective |K|.",
      "scalar_objective": "number of points",
      "direction": "minimize",
      "configuration_parameters": {
        "field_order": "q",
        "dimension": "d"
      },
      "human_baseline": "Dvir (2009) proved |K|≥c_d q^d by the polynomial method; explicit constructions are known. An October 2026 exposition reports an exact exhaustive result |K|=13 for F_3^3, but that source is secondary, so require primary-paper confirmation before adopting this numeric record.",
      "primary_sources": [
        "https://arxiv.org/abs/0803.2336",
        "https://arxiv.org/abs/1503.06639"
      ],
      "verification_cost": "Low for candidate set; exact minimum needs exhaustive or mathematical lower bound.",
      "risks": "Small finite cases and field characteristic matter; separate proven minimum from construction upper bound; record 2026 claim as pending primary confirmation.",
      "recommendation": "后备候选",
      "reason": "Natural finite extremal objective with strong theory, but exact record data are currently thin.",
      "research_origin": "discrete_round2.json",
      "source_id": "finite-kakeya",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T057",
      "name": "Sum–difference I: normalized logarithmic ratio",
      "definition": "输出至少两个不同整数组成的集合 A；计算其和集与差集。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "log(|A+A|/|A|)/log(|A-A|/|A|)",
      "direction": "maximize",
      "configuration_parameters": {
        "cardinality": "固定上限，如512；不是把固定17元素改作上限512",
        "integer_range": "如[-10^6,10^6]"
      },
      "human_baseline": "Pigarev–Freiman 的17元构造在 Martin–O'Bryant (2006/2007) 中重列；|A+A|=59、|A-A|=55，score=1.0597930945472454；本次已独立重算。",
      "primary_sources": [
        "https://personal.math.ubc.ca/~gerg/papers/downloads/MSHMSTD.pdf",
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/42.html"
      ],
      "verification_cost": "低：O(|A|²) 整数集合运算。",
      "risks": "该历史人类构造不是2026世界纪录；与II/III分母不同。新的含AI论文另列。",
      "recommendation": "MVP候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-sumdiff-I",
      "category": "加法组合与离散构造",
      "publication_status": "candidate_only",
      "baseline_audit": "example_witness_recomputed_not_full_task_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T058",
      "name": "Sum–difference II: unnormalized logarithmic ratio",
      "definition": "输出有限整数集 A，优化差集大小相对和集大小的指数。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "log(|A-A|)/log(|A+A|)",
      "direction": "maximize",
      "configuration_parameters": {
        "size_bound": "有限大小/坐标界需固定"
      },
      "human_baseline": "人类高维非负整数 simplex 构造给出渐近指数 log(1+sqrt(2))/log(2)≈1.27155；明确有限维实例须用足够大的进制嵌入整数并精确计分。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/43.html",
        "https://arxiv.org/html/2511.02864v1#S6.SS25"
      ],
      "verification_cost": "低至中：有限输出时计和集差集。",
      "risks": "渐近常数不是任意有限配置的可达baseline；有限实例尚待固定。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-sumdiff-II",
      "category": "加法组合与离散构造",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T059",
      "name": "Sum–difference III: finite certificate for asymptotic exponent",
      "definition": "输出含0的非负整数集 U，满足 Gyarmati–Hennecart–Ruzsa 有限证书定理的条件，用其证明渐近指数下界。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "1+log(|U-U|/|U+U|)/log(2 max(U)+1)",
      "direction": "maximize",
      "configuration_parameters": {
        "integer_bound": "max U 上限",
        "size_bound": "显式输出规模上限"
      },
      "human_baseline": "Gyarmati–Hennecart–Ruzsa (2007)：U={0,1,3,6,13,17,21}，和集26、差集39、q=43，score=1.107802056693651；本次已重算有限表达式。",
      "primary_sources": [
        "https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf",
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/44.html"
      ],
      "verification_cost": "低：整数集合运算。",
      "risks": "必须验证原证书条件（严格 |U-U|<2maxU+1 等）；后续1.14465等大构造不可直接当小配置baseline。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-sumdiff-III",
      "category": "加法组合与离散构造",
      "publication_status": "candidate_only",
      "baseline_audit": "example_witness_recomputed_not_full_task_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T060",
      "name": "Covering number C(v,k,t)",
      "category": "组合设计",
      "definition": "Find the fewest k-subsets of a v-set such that every t-subset is included in at least one selected block.",
      "solution_format": "List of k-subsets; objective block count.",
      "scalar_objective": "number of blocks",
      "direction": "minimize",
      "configuration_parameters": {
        "v": "points",
        "k": "block size",
        "t": "covering strength"
      },
      "human_baseline": "La Jolla Combinatorics Repository (Dan Gordon; frozen 2026) stores tens of thousands of best-known covers and lower bounds; individual construction records identify contributors/methods.",
      "primary_sources": [
        "https://dmgordon.org/ljcr/",
        "https://ljcr.dmgordon.org/cover.html"
      ],
      "verification_cost": "Low-medium for coverage; proving minimum needs lower bound.",
      "risks": "Repository baseline may be best-known rather than optimum; freeze data snapshot and preserve authorship metadata.",
      "recommendation": "MVP候选",
      "reason": "One of the strongest candidates: standardized finite objects, natural scalar, and large human record corpus.",
      "research_origin": "discrete.json",
      "source_id": "covering-design",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "specific_configuration_evidence_located_not_replayed",
      "open_configuration_reviews": [
        {
          "review_id": "R009",
          "task_id": "T060",
          "parameters": {
            "v": 24,
            "k": 14,
            "t": 4
          },
          "scalar": "block count ↓",
          "human_baseline": "historical covering repository construction:23; contributor/blocklist pending",
          "frontier_evidence": "2026 Lean project reports20–23; lower proof AI-assisted; root read source but did not replay",
          "sources": [
            "https://github.com/jamesyc/covering",
            "https://dmgordon.org/covering-designs/"
          ],
          "readiness": "source_located_not_release_ready"
        },
        {
          "review_id": "R010",
          "task_id": "T060",
          "parameters": {
            "v": 25,
            "k": 15,
            "t": 5
          },
          "scalar": "block count ↓",
          "human_baseline": "historical upper bound42; blocklist pending",
          "frontier_evidence": "same project reports34–42; human witness provenance pending",
          "sources": [
            "https://github.com/jamesyc/covering"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "excluded_configuration_groups": [
        {
          "task": "T060",
          "config": "C(8,4,3)=14，C(10,4,3)=30",
          "reason": "Steiner四元系达到计数下界；排除，不能把构造库所有行都当未解。",
          "sources": [
            "https://dmgordon.org/covering-designs/"
          ]
        }
      ],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T061",
      "name": "Covering array CAN(t,k,v)",
      "category": "组合设计",
      "definition": "Minimize rows N of a k-column v-ary array so every t selected columns contain every v^t tuple at least once.",
      "solution_format": "N×k array over v symbols; objective N.",
      "scalar_objective": "number of rows N",
      "direction": "minimize",
      "configuration_parameters": "No admitted v2 configuration. See discovery-only audit; all v1 solved calibration configurations excluded.",
      "human_baseline": "NIST Covering Array Library lists actual arrays for strengths 2–6 and 2–6 levels, plus best-known sizes to 20,000 columns (strength 2) and 10,000 (strengths 3–6); NIST and Colbourn records are human constructions/bounds.",
      "primary_sources": [
        "https://csrc.nist.gov/Projects/Automated-Combinatorial-Testing-for-Software/Covering-Array-Library",
        "https://math.nist.gov/coveringarrays/coveringarray.html"
      ],
      "verification_cost": "Low for explicit array; minimum proof varies.",
      "risks": "Keep uniform alphabet case separate from variable-strength/general mixed-level variants; NIST best-known size tables do not always include arrays.",
      "recommendation": "MVP候选",
      "reason": "Excellent benchmark corpus and easily verifiable scalar optimization.",
      "research_origin": "discrete.json",
      "source_id": "covering-array",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "configuration_parameters_v1": {
        "strength": "t",
        "columns": "k",
        "levels": "v"
      },
      "latest_confirmation_status": "excluded_config"
    },
    {
      "id": "T062",
      "name": "Orthogonal array minimum-run construction",
      "category": "组合设计",
      "definition": "For fixed strength t, levels and columns, construct an orthogonal array with the fewest rows (or maximize columns for fixed rows), each t-column tuple appearing equally often.",
      "solution_format": "Array with explicit index lambda; objective rows or columns, with one direction fixed per instance.",
      "scalar_objective": "number of rows N; λ=N/q^t is variable",
      "direction": "minimize",
      "configuration_parameters": {
        "t": "强度",
        "q": "字母表大小",
        "k": "列数；index λ不固定，随行数N优化"
      },
      "human_baseline": "Neil Sloane's library contains 200+ explicit arrays; Eendebak–Schoen catalogue complete non-isomorphic arrays for selected small parameters. OA( N,k,s,t) must meet divisibility/Rao bounds.",
      "primary_sources": [
        "https://neilsloane.com/oadir/index.html"
      ],
      "verification_cost": "Low for explicit array; minimality moderate/high.",
      "risks": "Do not conflate OA existence, maximum columns, and minimum-run objectives; fix one scalar per instance. Strength-2 binary OAs are essentially Hadamard matrices.",
      "recommendation": "后备候选",
      "reason": "Curated human constructions and simple exact validator; good if objective/configuration are fixed consistently.",
      "research_origin": "discrete.json",
      "source_id": "orthogonal-array",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T063",
      "name": "Packing number D(v,k,t)",
      "category": "组合设计",
      "definition": "Maximize the number of k-subsets on v points such that no t-subset is contained in more than one block.",
      "solution_format": "List of blocks; objective block count.",
      "scalar_objective": "number of blocks",
      "direction": "maximize",
      "configuration_parameters": {
        "v": "points",
        "k": "block size",
        "t": "packing strength"
      },
      "human_baseline": "La Jolla covering repository focuses on coverings, while classical packing bounds and constructions are published; candidate instance-level records require dedicated database/source review.",
      "primary_sources": [
        "https://dmgordon.org/ljcr/"
      ],
      "verification_cost": "Low for packing property.",
      "risks": "No unified current record table confirmed in this pass; may overlap partial Steiner designs.",
      "recommendation": "后备候选",
      "reason": "Good scalar and verification, but human-record baseline needs further curation.",
      "research_origin": "discrete.json",
      "source_id": "packing-design",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T064",
      "name": "Social golfer maximum schedule length",
      "category": "组合设计",
      "definition": "Partition players into groups of fixed size each round, avoiding any pair meeting twice; maximize number of rounds.",
      "solution_format": "Round-by-round partitions; objective number of rounds.",
      "scalar_objective": "number of rounds",
      "direction": "maximize",
      "configuration_parameters": {
        "players": "P",
        "group_size": "g",
        "groups_per_round": "fixed/implied"
      },
      "human_baseline": "CSPLib problem 010 defines the canonical 32 golfers in groups of four and its generalization; published constraint-programming literature reports solved/optimal schedules for small parameter sets, but benchmark records need per-instance capture.",
      "primary_sources": [
        "https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob010/",
        "https://www.csplib.org/Problems/prob010/"
      ],
      "verification_cost": "Low for pair uniqueness; maximality requires a bound/proof.",
      "risks": "Could degenerate into mere feasibility when target rounds fixed; use maximize rounds and instances with documented human optima.",
      "recommendation": "后备候选",
      "reason": "Natural schedule objective and benchmark tradition, but require verified per-instance baseline.",
      "research_origin": "discrete.json",
      "source_id": "social-golfer",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T065",
      "name": "Maximum number of mutually orthogonal Latin squares",
      "category": "组合设计",
      "definition": "For order n, maximize the number of pairwise orthogonal Latin squares (MOLS).",
      "solution_format": "List of Latin squares; objective count.",
      "scalar_objective": "number of MOLS",
      "direction": "maximize",
      "configuration_parameters": {
        "order": "n"
      },
      "human_baseline": "Bruck–Ryser–Chowla gives nonexistence restrictions; complete values are known for several small orders, while the standard MOLS tables record constructions and bounds.",
      "primary_sources": [
        "https://doi.org/10.1016/0012-365X(74)90148-4",
        "https://www.dcs.gla.ac.uk/~pat/cpM/jchoco/latinSquares/papers/10%5B1%5D.1.1.49.7739.pdf"
      ],
      "verification_cost": "Low for square/orthogonality checks; maximality often hard.",
      "risks": "Exact optimum open for some n; source table version and proof status must be frozen.",
      "recommendation": "后备候选",
      "reason": "Canonical extremal design quantity, simple verifier, and substantive human theory.",
      "research_origin": "discrete.json",
      "source_id": "latin-mols",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T066",
      "name": "Best minimum distance of linear codes",
      "category": "编码理论",
      "definition": "For fixed (n,k,q), construct a q-ary linear [n,k] code with maximum minimum Hamming distance d.",
      "solution_format": "Generator matrix over GF(q), with independently checked rank and minimum distance.",
      "scalar_objective": "Minimum Hamming distance d(C)",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "block length",
        "k": "dimension",
        "q": "finite-field order; use distinct benchmark rows, not one task per q/n"
      },
      "human_baseline": "Human-computed database: Markus Grassl, John Cannon and Greg White's Magma BKLC tables; Magma reports 33,152 best-known binary codes, all binary entries through n=31 optimal. Row-wise d and construction need retrieval from the database. This is historical human computation, not AI.",
      "primary_sources": [
        "https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html",
        "https://codetables.de/"
      ],
      "verification_cost": "Medium for small k (enumerate q^k codewords); high beyond that. Restrict benchmark to enumerable dimensions or certificate-backed distance.",
      "risks": "Minimum-distance inner enumeration grows exponentially; restrict k (and n) and verify row construction. Database values are best-known, not all proven optimal. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.",
      "recommendation": "MVP候选",
      "reason": "Canonical construction problem and extensively maintained human table, with one exact scalar and matrix output.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa06",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "specific_configuration_evidence_located_not_replayed",
      "open_configuration_reviews": [
        {
          "review_id": "R011",
          "task_id": "T066",
          "parameters": {
            "n": 68,
            "k": 15,
            "q": 2
          },
          "scalar": "minimum Hamming distance ↑",
          "human_baseline": "Grassl construction [68,15,24]",
          "frontier_evidence": "root read table24–26; explicit construction chain exists, generator not reconstructed",
          "sources": [
            "https://www.codetables.de/BKLC/BKLC.php?k=15&n=68&q=2"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "excluded_configuration_groups": [
        {
          "task": "T066",
          "config": "二元[23,12,7] Golay码，[15,7,5] BCH码",
          "reason": "这些参数最优最小距离已确定；排除。",
          "sources": [
            "https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html"
          ]
        }
      ],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T067",
      "name": "Maximum size of a binary code A(n,d)",
      "category": "编码理论",
      "definition": "Construct a subset C of {0,1}^n with pairwise Hamming distance at least d and maximum cardinality.",
      "solution_format": "List of binary words; verify distinctness and pairwise distances.",
      "scalar_objective": "|C|",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "block length",
        "d": "minimum distance"
      },
      "human_baseline": "A. E. Brouwer's classical tables and ongoing bounds; specific construction/value must be fixed per row. Human literature/database; no AI baseline assumed.",
      "primary_sources": [
        "https://aeb.win.tue.nl/codes/binary.html"
      ],
      "verification_cost": "O(|C|^2 n) for lower-bound witness; proving optimality substantially harder.",
      "risks": "Many instances have only bounds, not exact optimum; select a published construction row and compare witness cardinality, not claim optimality.",
      "recommendation": "后备候选",
      "reason": "Canonical extremal scalar and substantial human research; requires careful row selection and verifiable explicit witnesses.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa09",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "specific_configuration_evidence_located_not_replayed",
      "open_configuration_reviews": [
        {
          "review_id": "R012",
          "task_id": "T067",
          "parameters": {
            "n": 17,
            "distance": 6
          },
          "scalar": "number of codewords ↑",
          "human_baseline": "Milshtein 2019:258",
          "frontier_evidence": "root read Brouwer258–340; archive codeword list and newer-record search pending",
          "sources": [
            "https://aeb.win.tue.nl/codes/binary-1.html"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T068",
      "name": "Constant-weight code A(n,d,w)",
      "category": "编码理论",
      "definition": "Find a largest family of w-subsets of an n-set with pairwise symmetric difference at least d.",
      "solution_format": "List of w-subsets/bitmasks; verify all weights and pairwise Hamming distances.",
      "scalar_objective": "Code size |C|",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "ambient length",
        "d": "minimum Hamming distance",
        "w": "constant word weight"
      },
      "human_baseline": "Brouwer, Shearer, Sloane and Smith (1990) compiled bounds; many later explicit constructions and improved bounds. Pin row and construction before benchmark inclusion; human baseline, no AI assumed.",
      "primary_sources": [
        "https://aeb.win.tue.nl/codes/Andw.html"
      ],
      "verification_cost": "Low/medium: O(|C|^2 n), often under a second for small instances.",
      "risks": "Do not confuse lower-bound construction with known optimum; duplicate of general nonlinear code only if constant-weight constraint is not central. Fixed rows needed. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.",
      "recommendation": "后备候选",
      "reason": "Named classical family, explicit construction tables and a cheap exact scalar verifier.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa10",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T069",
      "name": "Constant-dimension subspace code A_q(n,d;k)",
      "category": "编码理论",
      "definition": "Find the largest set of k-dimensional subspaces of GF(q)^n with pairwise subspace distance at least d.",
      "solution_format": "Basis matrices/RREFs for subspaces; exact rank/intersection verification.",
      "scalar_objective": "Code size |C|",
      "direction": "maximize",
      "configuration_parameters": {
        "q": "field order",
        "n": "ambient dimension",
        "k": "subspace dimension",
        "d": "minimum subspace distance"
      },
      "human_baseline": "Heinlein, Kiermaier, Kurz and Wassermann (2016, updated 2019) maintain Tables of Subspace Codes; the paper explicitly describes best lower/upper bounds and constructions. Fix an exact table row for score/construction.",
      "primary_sources": [
        "https://arxiv.org/abs/1601.02864",
        "https://subspacecodes.uni-bayreuth.de/"
      ],
      "verification_cost": "Medium: pairwise intersection ranks O(|C|^2 n^3) with finite-field linear algebra.",
      "risks": "Many rows are intervals rather than exact optima; select modest dimensions and public construction records. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.",
      "recommendation": "后备候选",
      "reason": "Canonical research objective, maintained human database and exact simple witness verifier.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa11",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T070",
      "name": "Covering code size",
      "category": "编码理论",
      "definition": "For fixed binary length n and covering radius R, construct a smallest set C whose radius-R Hamming balls cover the whole cube.",
      "solution_format": "List of codewords; verify full coverage by exhaustive enumeration for small n.",
      "scalar_objective": "Code size |C|",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "length",
        "R": "covering radius"
      },
      "human_baseline": "Cohen, Honkala, Litsyn and Lobstein (1997) survey and tabulate covering codes; select a small open/nontrivial instance and recover explicit construction.",
      "primary_sources": [
        "https://neilsloane.com/doc/CR.html"
      ],
      "verification_cost": "Low for small n (2^n point coverage), exponential and unsuitable for large n.",
      "risks": "Inner covering check scales exponentially; exact optimum often unknown. Only small finite instances qualify.",
      "recommendation": "后备候选",
      "reason": "Natural one-scalar design task with historical constructions, but verifier cost bounds useful scale.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa18",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T071",
      "name": "Maximum permutation code size",
      "definition": "固定 n,d，输出 S_n 的子集，使任意两排列的 Hamming 距离至少 d。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "number of codewords",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "排列阶数",
        "d": "最小Hamming距离"
      },
      "human_baseline": "Bereg et al. (2019) Partition and Extension 给出显式人类构造与数值表；Ding–Fu–Kløve–Wei (2002)、Gao et al. (2008) 等经典构造可复现。需固定具体表格行。",
      "primary_sources": [
        "https://arxiv.org/abs/1804.08252",
        "https://arxiv.org/abs/0801.3987"
      ],
      "verification_cost": "低至中 O(M²n)。",
      "risks": "大群的生成元不是自动可快速验证的完整码；初期只接受显式小码。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-permutation-code",
      "category": "编码理论",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T072",
      "name": "Maximum deletion-correcting code size",
      "definition": "固定 q,n,t，输出 q 元长度 n 的码，任意不同码字的 t-deletion balls 不相交。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "number of codewords",
      "direction": "maximize",
      "configuration_parameters": {
        "q": "字母表大小",
        "n": "码长",
        "t": "可纠正删除数"
      },
      "human_baseline": "Varshamov–Tenengolts (1965) / Levenshtein (1966) 的二元单删除码有明确同余公式；按给定 n 枚举其码字可以得到可重算历史人类baseline。",
      "primary_sources": [
        "https://arxiv.org/abs/math/0207197",
        "https://neilsloane.com/doc/dijen.pdf"
      ],
      "verification_cost": "中：每码字枚举删除结果或两两 LCS；规模受限。",
      "risks": "VT明确同余构造见Sloane (2002)原稿；固定n后枚举得到人类基线，不能将其当全部有限n都已证最优。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-deletion-code",
      "category": "编码理论",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T073",
      "name": "LABS minimum aperiodic autocorrelation energy",
      "category": "序列与平坦多项式",
      "definition": "For s_i in {±1}, length L, minimize E=Σ_{k=1}^{L−1}(Σ_{i=1}^{L−k}s_i s_{i+k})².",
      "solution_format": "Binary sign sequence.",
      "scalar_objective": "E (equivalently merit factor L²/(2E))",
      "direction": "minimize",
      "configuration_parameters": "No admitted v2 configuration. See discovery-only audit; all v1 solved calibration configurations excluded.",
      "human_baseline": "Packebusch–Mertens (2015/2016) exact optima for lengths<=66 in the cited paper; Militzer author page has explicit historical evolutionary sequences. Do not describe historical records as latest.",
      "primary_sources": [
        "https://arxiv.org/abs/1512.02475",
        "https://militzer.berkeley.edu/sequences.html"
      ],
      "verification_cost": "Low: O(L²) integer arithmetic.",
      "risks": "Energy and merit factor are strictly monotone transforms for fixed L, so they are the same task and must not be counted twice. Best known versus proven optimum must be labeled.",
      "recommendation": "MVP候选",
      "reason": "Canonical researched objective, explicit human sequence tables, extremely cheap exact scalar verifier.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa21",
      "publication_status": "candidate_only",
      "baseline_audit": "example_witness_recomputed_not_full_task_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [
        {
          "task": "T073",
          "config": "LABS能量长度N<=66，包括上一版N=66,E=257",
          "reason": "Packebusch–Mertens给出精确最优结果；排除。更大长度是否近期已解另查。",
          "sources": [
            "https://arxiv.org/abs/1512.02475"
          ]
        }
      ],
      "configuration_parameters_v1": {
        "L": "sequence length; select fixed rows, do not count lengths as separate task families"
      },
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T074",
      "name": "LABS peak sidelobe level (PSL)",
      "category": "序列与平坦多项式",
      "definition": "For binary sign sequence s of length L, minimize max_{1≤k<L}|Σ_{i=1}^{L−k}s_i s_{i+k}|.",
      "solution_format": "Binary sign sequence.",
      "scalar_objective": "PSL=max absolute nonzero aperiodic autocorrelation",
      "direction": "minimize",
      "configuration_parameters": {
        "L": "sequence length"
      },
      "human_baseline": "Dmitriev and Jedwab (2005) studied typical PSL; later Best-Known Peak Sidelobe Level Values (2021) reports constructed sequences and search results. Retrieve row-specific construction before instantiation.",
      "primary_sources": [
        "https://www.sfu.ca/~jed/Research/PSL.html",
        "https://arxiv.org/abs/1212.4930",
        "https://arxiv.org/abs/2104.10477"
      ],
      "verification_cost": "Low O(L²).",
      "risks": "PSL optima can conflict with LABS energy; do not present as interchangeable with merit factor. Current row baseline needed.",
      "recommendation": "后备候选",
      "reason": "Independent standard objective with its own human literature and one exact integer score.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa22",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T075",
      "name": "Periodic binary autocorrelation energy",
      "category": "序列与平坦多项式",
      "definition": "For s∈{±1}^L, minimize the sum of squares of nonzero periodic autocorrelations C(k)=Σ_i s_i s_{i+k mod L}.",
      "solution_format": "Binary sign sequence.",
      "scalar_objective": "Σ_{k=1}^{L−1} C(k)^2",
      "direction": "minimize",
      "configuration_parameters": {
        "L": "period length"
      },
      "human_baseline": "经典Legendre/Paley周期序列，以及Yan–Chen–Li (2014)、Yan–Gong (2014)等显式构造。p≡3(mod4)的Legendre符号序列（0项设1）给每个非零周期自相关−1，可作为已解校准：能量p−1、PSL1。非已解长度须另选行级人类构造。",
      "primary_sources": [
        "https://arxiv.org/abs/1401.2530",
        "https://arxiv.org/abs/1411.4340",
        "https://doi.org/10.1016/j.tcs.2009.02.021"
      ],
      "verification_cost": "Low O(L²).",
      "risks": "Be precise about periodic versus aperiodic correlation and normalization; known perfect sequences may make selected cases trivial.",
      "recommendation": "后备候选",
      "reason": "Natural scalar and mature literature, but needs row-specific open headroom and cited human record.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa24",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [
        {
          "task": "T075/T076",
          "config": "奇素数p≡3 mod4的Legendre周期序列已达到能量p−1或PSL=1的情形",
          "reason": "匹配奇长度非零周期自相关绝对值至少1的下界；排除这些配置。",
          "sources": [
            "https://arxiv.org/abs/1401.2530"
          ]
        }
      ],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T076",
      "name": "Binary sequence maximum out-of-phase autocorrelation (periodic merit)",
      "category": "序列与平坦多项式",
      "definition": "For fixed length L, construct a binary sequence minimizing the maximum absolute nonzero periodic autocorrelation.",
      "solution_format": "Binary sign sequence.",
      "scalar_objective": "max_{k≠0}|Σ_i s_i s_{i+k mod L}|",
      "direction": "minimize",
      "configuration_parameters": {
        "L": "period length"
      },
      "human_baseline": "经典Legendre/Paley周期序列，以及Yan–Chen–Li (2014)、Yan–Gong (2014)等显式构造。p≡3(mod4)的Legendre符号序列（0项设1）给每个非零周期自相关−1，可作为已解校准：能量p−1、PSL1。非已解长度须另选行级人类构造。",
      "primary_sources": [
        "https://arxiv.org/abs/1401.2530",
        "https://arxiv.org/abs/1411.4340",
        "https://doi.org/10.1016/j.tcs.2009.02.021"
      ],
      "verification_cost": "Low O(L²).",
      "risks": "Related but distinct from aperiodic PSL; ensure periodic definition and cited baseline align exactly.",
      "recommendation": "后备候选",
      "reason": "Natural exact scalar and historical research, but needs a fixed, sourced comparison row.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa45",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [
        {
          "task": "T075/T076",
          "config": "奇素数p≡3 mod4的Legendre周期序列已达到能量p−1或PSL=1的情形",
          "reason": "匹配奇长度非零周期自相关绝对值至少1的下界；排除这些配置。",
          "sources": [
            "https://arxiv.org/abs/1401.2530"
          ]
        }
      ],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T077",
      "name": "Littlewood polynomials: minimum supremum modulus",
      "definition": "输出长度 L 的±1系数多项式 P，最小化整个单位圆上的归一化最大模。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "max_{|z|=1}|P(z)|/sqrt(L)",
      "direction": "minimize",
      "configuration_parameters": {
        "L": "系数个数"
      },
      "human_baseline": "Rudin–Shapiro 递推给出人类显式多项式和上界 sqrt(2)（L为2的幂）；Odlyzko (2018) 对有限长度做过大量数值搜索。记录数值需全域认证。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html",
        "https://arxiv.org/abs/1907.09464"
      ],
      "verification_cost": "中至高：三角多项式全域极值；不是只采样。",
      "risks": "核实第二来源与所用构造定义；文献中的网格最优不是严格全域最优。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-littlewood-sup",
      "category": "序列与平坦多项式",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T078",
      "name": "Littlewood polynomials: maximum infimum modulus",
      "definition": "输出长度 L 的±1系数多项式 P，最大化整个单位圆上的归一化最小模。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "min_{|z|=1}|P(z)|/sqrt(L)",
      "direction": "maximize",
      "configuration_parameters": {
        "L": "系数个数；注意奇偶造成的单位根"
      },
      "human_baseline": "Littlewood 的平坦多项式问题、Odlyzko (2018) 数值构造、Balister et al. 的 Flat Littlewood Polynomials 提供人类基线来源；具体 L 的系数和严格最小模尚须定位。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html",
        "https://arxiv.org/abs/1907.09464"
      ],
      "verification_cost": "中至高：全域下界证书。",
      "risks": "并非最小sup的单调改写；当前只有文献入口，不能宣称有限实例humanbaseline已齐。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-littlewood-inf",
      "category": "序列与平坦多项式",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T079",
      "name": "First Autocorrelation Inequality (AC1)",
      "category": "极值分析",
      "definition": "Find nonnegative integrable f supported on [-1/4,1/4], integral 1, minimizing max_{t in [-1/2,1/2]} (f*f)(t).",
      "solution_format": "Exact piecewise-polynomial or rational step function with proof of support, positivity and unit mass.",
      "scalar_objective": "Phi1=max_t(f*f)(t)",
      "direction": "minimize",
      "configuration_parameters": {
        "support": "fixed [-1/4,1/4]",
        "representation": "piecewise polynomial degree and breakpoints; configure separately"
      },
      "human_baseline": "SimpleTES (2026 paper table 11 reports human 1.509730; AI-assisted results separate: AlphaEvolve 1.505300; SimpleTES 1.503871). Human attribution cites prior sources [15,82,147], which should be independently checked before benchmark release.",
      "primary_sources": [
        "https://arxiv.org/abs/0907.1379",
        "https://math.bme.hu/~matolcsi/sch0914.pdf",
        "https://arxiv.org/abs/2604.19341"
      ],
      "verification_cost": "Medium/high: exact convolution per polynomial segment, certify global maximum via roots/interval arithmetic.",
      "risks": "Sampling the continuum maximum is not a proof; enforce exact mass and nonnegativity. Human baseline provenance needs citation-level audit.",
      "recommendation": "MVP候选",
      "reason": "Named established objective, human record and one scalar; strict certificate possible with piecewise-polynomial representation.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa01",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T080",
      "name": "Second Autocorrelation Inequality (AC2)",
      "category": "极值分析",
      "definition": "Find nonnegative integrable f supported on [-1/4,1/4], integral 1, maximizing ||f*f||_2^2/(||f*f||_1 ||f*f||_infinity).",
      "solution_format": "Exact piecewise-polynomial or rational step function with proof of support, positivity and unit mass.",
      "scalar_objective": "Phi2=||f*f||_2^2/(||f*f||_1||f*f||_infinity)",
      "direction": "maximize",
      "configuration_parameters": {
        "support": "fixed [-1/4,1/4]",
        "representation": "piecewise polynomial degree and breakpoints; configure separately"
      },
      "human_baseline": "SimpleTES (2026 table 11) reports best human 0.901500; AI-assisted: AlphaEvolve V2 0.961000; SimpleTES 0.962694.",
      "primary_sources": [
        "https://arxiv.org/abs/0907.1379",
        "https://math.bme.hu/~matolcsi/sch0914.pdf",
        "https://arxiv.org/abs/2604.19341"
      ],
      "verification_cost": "High: exact convolution and certified L2/L1/L-infinity evaluation; maximum requires root isolation/interval methods.",
      "risks": "A sampled supremum gives unsound scores; human record citation chain needs audit. Objective's denominator conventions must be fixed.",
      "recommendation": "MVP候选",
      "reason": "Explicit published extremal objective with named human and AI baselines; admits rigorous certificates using algebraic pieces.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa02",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T081",
      "name": "Third Autocorrelation Inequality (AC3)",
      "category": "极值分析",
      "definition": "Find real integrable f supported on [-1/4,1/4], integral 1, minimizing max_t |(f*f)(t)| over [-1/2,1/2].",
      "solution_format": "Exact piecewise-polynomial or rational step function, with exact integral and certified global supremum.",
      "scalar_objective": "Phi3=max_t |(f*f)(t)|",
      "direction": "minimize",
      "configuration_parameters": {
        "support": "fixed [-1/4,1/4]",
        "representation": "piecewise polynomial degree and breakpoints; configure separately"
      },
      "human_baseline": "SimpleTES (2026 table 11) reports best human 1.458100; AI-assisted results include AlphaEvolve 1.455700 and SimpleTES 1.453675. Paper flags some AI comparisons as using a corrected verifier.",
      "primary_sources": [
        "https://arxiv.org/abs/0907.1379",
        "https://math.bme.hu/~matolcsi/sch0914.pdf",
        "https://arxiv.org/abs/2604.19341"
      ],
      "verification_cost": "High: exact convolution; certify absolute maximum by polynomial critical-point isolation or interval arithmetic.",
      "risks": "Continuum maximum cannot be sampled; verifier versions differed in prior AI comparisons; audit human sources.",
      "recommendation": "MVP候选",
      "reason": "Named objective, scalar and human baseline are directly tabulated; exact semialgebraic witnesses can be certified.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa03",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T082",
      "name": "Erdős Minimum Overlap",
      "category": "极值分析",
      "definition": "Let f:[0,2]→[0,1] be a step function with ∫_0^2 f(x)dx=1. Define g(x)=1−f(x) for x∈[0,2] and g(x)=0 outside [0,2]. Minimize Ψ(f)=sup_{t∈R} ∫_R f(x)g(x+t)dx = sup_{t∈R} ∫_[0,2]∩[-t,2-t] f(x)(1−f(x+t))dx. Both f and g are zero outside [0,2]; this is essential. Include both shift directions and do not use finite M(N) as the same score.",
      "solution_format": "Exact rational step function with breakpoints and values, exact mass, and a rigorous maximization over all shifts s (piecewise polynomial plus root isolation/interval arithmetic).",
      "scalar_objective": "Ψ(f)=sup_{t∈R}∫_R f(x)g(x+t)dx, where f,g are supported on [0,2] and g=1−f on [0,2] (lower is better). Equivalent to the intersection-range integral; both positive and negative shifts are included.",
      "direction": "minimize",
      "configuration_parameters": {
        "step_count": "number of equal-width intervals on [0,2] (e.g. 15 or 51); representation setting, not a separate task"
      },
      "human_baseline": "Haugland (2016) reports human step-function upper-bound witnesses for this continuous normalized objective: 15 steps gives 0.38153155 (rounded upward); 51 steps gives 0.3809268534330870. These are reported construction scores, not independently reproduced here. AI-assisted results are separate.",
      "primary_sources": [
        "https://arxiv.org/abs/1609.08000",
        "https://arxiv.org/abs/2201.05704"
      ],
      "verification_cost": "Finite exact task low/medium; limiting witness high (integral/profile derivation and rigorous discretization error certificate).",
      "risks": "Both f and its complement g must be supported on [0,2], with g=1−f only inside [0,2] and zero outside. If 1−f is incorrectly zero-extended as a function equal to 1 outside, endpoint shifts spuriously score 1. Use sup over all real t, equivalently include both positive and negative shifts; a nonsymmetric candidate cannot be scored using only one shift direction. Certify the piecewise functional over every shift interval, not on a grid. The finite partition M(N)/N is related but not the same candidate score.",
      "recommendation": "MVP候选",
      "reason": "Named limiting extremal problem with Haugland continuous step-function upper-bound constructions and a natural scalar. The support convention for both f and g makes the score well-defined and comparable to the published 0.38 values.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa04",
      "publication_status": "candidate_only",
      "baseline_audit": "example_witness_recomputed_not_full_task_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T083",
      "name": "Autocorrelation lower envelope for difference bases",
      "definition": "构造可积函数 f，最大化位移 t∈[0,1] 上自相关的最小值，经L1质量归一化。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "min_{0<=t<=1} ∫f(x)f(x+t)dx / ||f||_1²",
      "direction": "maximize",
      "configuration_parameters": {
        "representation": "支持区间、分段复杂度需固定；不能改变位移区间的尺度后混比"
      },
      "human_baseline": "Barnard–Steinerberger 文献给出历史构造下界0.37（带边界修正的arcsine分布）；具体有界阶梯函数与0.37的适用参数待核。",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/6.html",
        "https://arxiv.org/html/2511.02864v1#S6.SS2"
      ],
      "verification_cost": "中至高：全位移区间的下包络认证。",
      "risks": "奇异函数、边界点及积分容错曾导致原系统虚高得分，初期不选。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-difference-autocorrelation",
      "category": "极值分析",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T084",
      "name": "Sign uncertainty principle (Fourier sign changes)",
      "category": "极值分析",
      "definition": "For even real f∈L1(R), define A(f)=inf{r>0:f(x)≥0 for |x|≥r}; with f(0), fhat(0)<0, seek constructions making A(f)A(fhat) small, hence an upper bound on the best universal constant C in A(f)A(fhat)≥C.",
      "solution_format": "Explicit even real function with a rigorous Fourier transform/sign certificate and certified sign-change radii; use compactly supported piecewise-polynomial or Gaussian-polynomial forms with analytic transforms.",
      "scalar_objective": "A(f)A(fhat), which is an upper bound on the sharp constant C",
      "direction": "minimize",
      "configuration_parameters": {
        "Fourier_convention": "fix once",
        "function_family": "certifiable analytic family; degree/support settings are representation parameters"
      },
      "human_baseline": "Gonçalves, Oliveira e Silva and Steinerberger (2016): upper bound 0.353 and lower bound 0.2025. Cohn and Gonçalves (2017): upper bound 0.32831. Georgiev et al. (2025) AlphaEvolve-assisted construction: 0.321591. Cohn–de Laat–Gonçalves announced unpublished 0.3102 in 2025; distinguish this human result from AI-assisted AlphaEvolve.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/11.html",
        "https://arxiv.org/abs/1712.04438"
      ],
      "verification_cost": "High: certify signs of f and Fourier transform on unbounded domains, plus exact/rigorous threshold radii.",
      "risks": "A finite sample grid cannot certify eventual sign. Human 0.3102 is reported as unpublished in the AlphaEvolve problem page; use the published 0.32831 as baseline unless the unpublished artifact is publicly reproducible.",
      "recommendation": "后备候选",
      "reason": "Named sharp-constant problem, natural one-number witness objective, and documented human published bounds; only include with rigorous Fourier-tail/sign certification.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa46",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [
        {
          "task": "T084",
          "config": "正号sign uncertainty维数12的已知sharp配置",
          "reason": "已达精确常数；不能把另一符号、不同维数或不同平方约定的值混用。",
          "sources": [
            "https://arxiv.org/abs/1712.04438",
            "https://arxiv.org/abs/2608.15415"
          ]
        }
      ],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T085",
      "name": "Cohn–Elkies linear-programming bound for sphere packing",
      "category": "极值分析",
      "definition": "For a fixed dimension d, construct an admissible radial function f with f(0)>0, Fourier transform nonnegative and f(x)≤0 outside a specified radius, minimizing the normalized Cohn–Elkies upper bound on packing density.",
      "solution_format": "Exact polynomial-times-Gaussian or rigorously certified radial function with Fourier positivity and sign constraints, plus computed bound.",
      "scalar_objective": "Normalized linear-programming upper bound C(d)",
      "direction": "minimize",
      "configuration_parameters": {
        "d": "Euclidean dimension",
        "function_family": "radial basis / polynomial-Gaussian representation; exact certificate settings separate"
      },
      "human_baseline": "Cohn and Elkies (2003) introduced the LP bound; Viazovska (2017) proved its sharpness for E8, and Cohn, Kumar, Miller, Radchenko and Viazovska (2017) for Leech lattice dimension 24. For other dimensions, use published human LP bounds; choose an explicit row before acceptance.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/13.html",
        "https://arxiv.org/abs/math/0110009",
        "https://arxiv.org/abs/1603.04246",
        "https://arxiv.org/abs/1603.06518"
      ],
      "verification_cost": "High: global Fourier positivity and sign verification on continuous domains; interval/analytic certificates required.",
      "risks": "Do not score sampled radial values. Dimensions 8 and 24 have solved packing optima; select open dimensions and compare only a certified bound.",
      "recommendation": "后备候选",
      "reason": "Canonical scalar optimization with exceptional human constructions and rich public research, but the continuous certificate is demanding.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa52",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [
        {
          "task": "T090/T085",
          "config": "维数8、24的最优球装填/匹配Cohn–Elkies上界",
          "reason": "E8、Leech格已达最优；排除这些配置。",
          "sources": [
            "https://arxiv.org/abs/1603.04246",
            "https://arxiv.org/abs/1603.06518"
          ]
        }
      ],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T086",
      "name": "General one-dimensional Gagliardo–Nirenberg sharp constant",
      "category": "极值分析",
      "definition": "For fixed admissible (j,p,q,r,m,θ), maximize ||D^j u||_p/(||D^m u||_r^θ ||u||_q^(1−θ)) over nonzero test functions u on R, with the scale relation in the AlphaEvolve problem statement.",
      "solution_format": "Explicit analytic or piecewise-polynomial function with rigorous norm and derivative-integral evaluation; certificate for a lower bound on C.",
      "scalar_objective": "||D^j u||_p / (||D^m u||_r^θ ||u||_q^(1−θ)) for the submitted u",
      "direction": "maximize",
      "configuration_parameters": {
        "j": "derivative order",
        "m": "higher derivative order",
        "p,q,r,theta": "admissible exponents; select one fixed row"
      },
      "human_baseline": "Classical Gagliardo (1958) and Nirenberg (1959) inequalities establish finiteness for the stated admissible regime. The AlphaEvolve paper states that the tested constants are known theoretically; it supplies the explicit solved special case aa49 but does not identify a single general-parameter human score. A fixed row and its sharp-constant reference remain待核实.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/15.html",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "High: improper integrals and derivative norms require certified tails; upper-bound proof of the sharp constant is harder than a witness score.",
      "risks": "General family is too broad as written; configure a single parameter tuple and distinguish a rigorous lower-bound witness from the unknown sharp constant.",
      "recommendation": "后备候选",
      "reason": "Natural one-number extremal objective and rich research, but benchmark needs a concrete row with an explicit human sharp value and certified witness evaluator.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa48",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T087",
      "name": "Rudin spherical harmonic Lp extremizer",
      "category": "极值分析",
      "definition": "For fixed d≥2, degree D and p∈{4,∞}, maximize ||u||_Lp(S^d)/||u||_L2(S^d) over real degree-D spherical harmonics, with sphere measure normalized to one.",
      "solution_format": "Harmonic coefficient vector in an exact orthonormal basis; certify norm ratio, using exact polynomial integration for p=4 or global optimization on sphere for p=∞.",
      "scalar_objective": "||u||_p/||u||_2 for the submitted spherical harmonic",
      "direction": "maximize",
      "configuration_parameters": {
        "d": "sphere dimension",
        "D": "harmonic degree",
        "p": "4 or infinity"
      },
      "human_baseline": "AlphaEvolve repository problem 57 and Georgiev et al. (2025) identify the finite-dimensional extremal problem, but the exact row-level human record/value was not retrieved in this pass; mark score待核实 before inclusion.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/57.html",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "Medium for p=4 (finite algebraic integral); high for p=∞ (continuous sphere supremum).",
      "risks": "Need a published human construction/value for a specific (d,D,p); continuum maximization for p=∞ cannot be sampled as proof.",
      "recommendation": "后备候选",
      "reason": "Clean single scalar and finite-dimensional search space; baseline evidence and strict p=∞ verifier remain incomplete.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa53",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T088",
      "name": "Ovals curvature Schrödinger eigenvalue",
      "category": "极值分析",
      "definition": "Minimize the lowest periodic eigenvalue λ0 of Hγ=−d²/ds²+κ(s)² over simple closed convex plane curves of length 2π.",
      "solution_format": "Certified convex curve (e.g. rational Fourier curvature/tangent data satisfying closure and total turning) and rigorous eigenvalue upper bound; lower-bound claims need proof.",
      "scalar_objective": "λ0(Hγ)",
      "direction": "minimize",
      "configuration_parameters": {
        "length": "fixed 2π",
        "curve_representation": "Fourier coefficients/breakpoints and exact closure constraints"
      },
      "human_baseline": "Benguria and Loss (2004) identified the circle/equality family with value 1, giving C≤1; Linde's 2015 work gives a global lower bound C>0.81 and numerical evaluation C>0.8246 (as summarized in later research). AlphaEvolve (2025) recovered the circle but not the noncircular equality family. Human constructions are explicit.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/19.html",
        "https://doi.org/10.1007/s00023-004-0186-8",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "High: certify convexity/closure and periodic Schrödinger ground-state eigenvalue; use validated spectral bounds.",
      "risks": "Circle immediately attains the known upper value 1; to create a useful benchmark, target a different construction such as recovery of noncircular equality family, but that is structural and not a scalar improvement.",
      "recommendation": "后备候选",
      "reason": "A named spectral variational problem with explicit human extremizers, but the scalar is already attained by the circle and meaningful discovery headroom is limited.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa54",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T089",
      "name": "Maximum determinant of sign matrices",
      "category": "矩阵、格与代数极值",
      "definition": "Find A in {−1,+1}^{29x29} maximizing |det A|.",
      "solution_format": "29x29 sign matrix; exact determinant certificate; optionally a proving upper-bound certificate if optimality is claimed.",
      "scalar_objective": "|det A| (equivalently the normalized determinant in the cited benchmark)",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "阶数；原论文实例29，新配置例如31"
      },
      "human_baseline": "Orrick and Solomon's classical record, as reported by Ye et al. (2026): |det|=320·7^12·2^28 (normalized 0.935673). SimpleTES recovers it; this is AI-assisted and is not the human baseline.",
      "primary_sources": [
        "https://maths-people.anu.edu.au/~brent/maxdet/order29/",
        "https://arxiv.org/abs/math/0304410"
      ],
      "verification_cost": "Low: Bareiss exact determinant; optimality verification is separate and harder.",
      "risks": "Do not score only existence of Hadamard; exact determinant is the natural scalar. Published value is a best-known lower bound, not necessarily proved global maximum.",
      "recommendation": "MVP候选",
      "reason": "Explicit known scalar record, human construction, exact cheap evaluator; fixed order is configuration.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa05",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "specific_configuration_evidence_located_not_replayed",
      "open_configuration_reviews": [
        {
          "review_id": "R013",
          "task_id": "T089",
          "parameters": {
            "n": 29
          },
          "scalar": "absolute determinant ↑",
          "human_baseline": "Orrick et al.:2^28·7^12·320",
          "frontier_evidence": "Brent conjectures optimality; historicalupper329·7^12·2^28; high risk incumbent already optimal",
          "sources": [
            "https://maths-people.anu.edu.au/~brent/maxdet/order29/",
            "https://maths-people.anu.edu.au/~brent/pd/Brent-maxdet-RMIT.pdf"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T090",
      "name": "Minkowski lattice packing density",
      "category": "矩阵、格与代数极值",
      "definition": "For a fixed dimension and specified lattice class, construct a lattice packing maximizing sphere-packing density.",
      "solution_format": "Basis matrix plus rigorous determinant/minimum-vector-length certificate.",
      "scalar_objective": "Packing density (equivalently inverse covolume at fixed minimum distance)",
      "direction": "maximize",
      "configuration_parameters": {
        "dimension": "d",
        "lattice_class": "all lattices or specified symmetry"
      },
      "human_baseline": "Minkowski (1896) introduced the problem; human constructions include root lattices, with exact densest lattice results known in some low dimensions (e.g. dimension 8 and 24 via Viazovska and collaborators for all packings). Row-specific lattice optima vary.",
      "primary_sources": [
        "https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/",
        "https://arxiv.org/abs/1603.04246",
        "https://arxiv.org/abs/1603.06518"
      ],
      "verification_cost": "High: shortest-vector and determinant certification; dimension-dependent.",
      "risks": "May be closed in famous dimensions or difficult to verify in open dimensions; source domain is geometric construction, suitable only with exact finite certificates.",
      "recommendation": "后备候选",
      "reason": "A single meaningful continuous scalar and extensive human constructions, but certificates and open-instance screening are demanding.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa39",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [
        {
          "task": "T090/T085",
          "config": "维数8、24的最优球装填/匹配Cohn–Elkies上界",
          "reason": "E8、Leech格已达最优；排除这些配置。",
          "sources": [
            "https://arxiv.org/abs/1603.04246",
            "https://arxiv.org/abs/1603.06518"
          ]
        }
      ],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T092",
      "name": "Schmeisser polynomial critical-point barycenter constant",
      "category": "矩阵、格与代数极值",
      "definition": "For fixed n, determine the least C(n) such that for each degree-n polynomial with roots in the unit disk and every convex combination of its roots, some critical point lies within distance C(n) of that combination.",
      "solution_format": "Explicit polynomial roots and convex weights for lower-bound witness; exact derivative roots and certified distances.",
      "scalar_objective": "min_j |Σ_k l_k z_k−w_j| for the submitted polynomial and weights",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "degree n≥2",
        "weights": "simplex weights; part of optimization variables"
      },
      "human_baseline": "Schmeisser conjectured C(n)=1; the AlphaEvolve repository states the conjectured value but no numeric human construction or row-specific best lower bound was verified in this scan. Treat numerical baseline as待核实.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/21.html",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "Medium/high: polynomial root certification and optimization over a continuum of convex weights.",
      "risks": "Human construction/record not verified; worst-case optimization includes a continuous simplex and polynomial family. Need a finite witness protocol.",
      "recommendation": "后备候选",
      "reason": "Natural scalar extremal constant and cited human conjecture, but presently lacks a verified numeric construction baseline.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa56",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T093",
      "name": "Borcea p-moment critical-point distance constant",
      "category": "矩阵、格与代数极值",
      "definition": "For fixed (p,n), maximize the worst root-to-nearest-critical-point distance over degree-n polynomials whose roots satisfy n^−1Σ|z_i|^p≤1; this defines C(p,n).",
      "solution_format": "Polynomial roots and derivative roots with exact/interval algebraic data; verify moment constraint and distances.",
      "scalar_objective": "max_{root ζ} min_{critical ξ}|ξ−ζ| for the submitted normalized polynomial",
      "direction": "maximize",
      "configuration_parameters": {
        "p": "moment exponent, 1≤p<∞",
        "n": "degree n≥2"
      },
      "human_baseline": "Borcea (1996) proved Sendov's conjecture for polynomials with at most seven distinct zeros. Khavinson, Pereira, Putinar, Saff and Shimorin (2011) formulated Borcea's variance conjectures; AlphaEvolve paper notes Borcea's conjecture C(p,n)=1 and verifies special cases (p,n)=(1,3),(2,4) in the cited literature. No general numeric row baseline retrieved.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/22.html",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "High: root and derivative root enclosures plus moment constraint; global sharpness unverified.",
      "risks": "Related to Sendov but genuinely adds a p-moment condition; parameter p=∞ recovers Sendov-like behavior. Need a concrete open row and numeric human lower construction.",
      "recommendation": "后备候选",
      "reason": "A distinct published strengthening with a single scalar; current baseline data are insufficient for a frozen benchmark row.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa57",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T094",
      "name": "Noncommutative matrix AM–GM ratio",
      "category": "矩阵、格与代数极值",
      "definition": "固定n,m,d和一个明确的酉不变范数，提交n个d×d半正定矩阵A_i，最小化有放回与无放回的长度m乘积范数平均值之比。",
      "solution_format": "Finite PSD matrices with rational/algebraic entries; exact products, norms, and ratio or certified eigenvalue bounds.",
      "scalar_objective": "[n^(−m) Σ_{j1,…,jm} ||A_j1⋯A_jm||] / [((n−m)!/n!) Σ_{distinct j1,…,jm} ||A_j1⋯A_jm||]",
      "direction": "minimize",
      "configuration_parameters": {
        "n,m,d": "固定，小n和m限制枚举成本",
        "norm": "例如operator norm，必须固定"
      },
      "human_baseline": "Duchi (2012) posed noncommutative AM–GM conjectures; Recht and Ré (2012) gave commentary/counterexample context. De Sa (2020) constructed counterexamples to a related matrix inequality. Exact parameter-row record and theorem status need primary-source audit.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/47.html",
        "https://proceedings.mlr.press/v23/recht12.html"
      ],
      "verification_cost": "Medium/high: exact matrix products and spectral norms; PSD/eigenvalue constraints need certification.",
      "risks": "分母必须严格正；PSD和所选范数都需验证。原代理未抄明确方向，本表按官方47题取inf修正。乘积枚举n^m，仅小配置适合快速验证。",
      "recommendation": "后备候选",
      "reason": "Published matrix inequality family offers a natural scalar ratio, but objective direction and row-level baseline need exact primary-source reconstruction.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa61",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "T095",
      "name": "Minimum Mahler measure of noncyclotomic integer polynomials",
      "category": "矩阵、格与代数极值",
      "definition": "For fixed degree bound d, find a noncyclotomic monic integer polynomial minimizing Mahler measure M(P)=∏ max(1,|root|).",
      "solution_format": "Integer polynomial with irreducibility/noncyclotomic proof and certified roots/Mahler measure.",
      "scalar_objective": "Mahler measure M(P)",
      "direction": "minimize",
      "configuration_parameters": {
        "degree_bound": "d",
        "class": "monic integer, irreducible, noncyclotomic"
      },
      "human_baseline": "Lehmer (1933)给出degree10多项式 x^10+x^9−x^7−x^6−x^5−x^4−x^3+x+1，Mahler measure约1.176280818。这是经典历史人类构造；不就2026最新状态作未经核实断言。",
      "primary_sources": [
        "https://doi.org/10.2307/1968172",
        "https://www.research.ed.ac.uk/files/1874954/Smyth240707.pdf"
      ],
      "verification_cost": "Medium/high: irreducibility and roots/Mahler measure require exact algebraic certification.",
      "risks": "For degree bounded and broad coefficient sizes the search space is ill-defined; specify coefficient/degree constraints and distinguish known lower bound from conjectured minimum.",
      "recommendation": "后备候选",
      "reason": "Famous named scalar challenge and human construction, but parameterization and exact certification need careful design.",
      "research_origin": "algebra_analysis.json",
      "source_id": "aa34",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T096",
      "name": "Integer Chebyshev polynomial construction",
      "definition": "给定区间 E 与次数上限 n，构造非零整数系数多项式 P，最小化其在 E 上的sup范数。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "||P||_E^(1/n)",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "固定次数上限，归一化指数固定为该n",
        "E": "例如[0,1]"
      },
      "human_baseline": "Pritsker (2001/2005)、Habsieger–Salvy、Flammang 等提供显式因子构造。Pritsker原稿有历史界；近年声称新界的预印本不自动作为已核人类纪录。",
      "primary_sources": [
        "https://arxiv.org/abs/math/0101166",
        "https://math.okstate.edu/people/igor/intcheb.pdf"
      ],
      "verification_cost": "中：整数多项式临界点隔离和区间端点求值。",
      "risks": "区别于实系数Chebyshev闭式问题；需要具体次数和因子指数表，不能用渐近常数当有限分数。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-integer-chebyshev",
      "category": "矩阵、格与代数极值",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T097",
      "name": "Shortest addition chain",
      "definition": "固定目标整数 n，输出从1出发的加法链，每项为之前两项之和，末项n。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "number of additions",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "目标整数；大小与位数为配置"
      },
      "human_baseline": "Flammenkamp、Clift 有精确长度数据库；Wilson/Resta 公开 n<=1024 的实际最短链。大数记录须区分历史人与近期可能AI参与的更新。",
      "primary_sources": [
        "https://wwwhomes.uni-bielefeld.de/achim/addition_chain.html",
        "https://webhost.services.iit.cnr.it/staff/giovanni.resta/ac/"
      ],
      "verification_cost": "低：逐步验证等式和长度。",
      "risks": "小数多数已知最优，适合校准；单目标最优加法链NP-hard性不能从多目标版本直接推断。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-addition-chain",
      "category": "数论与算术构造",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T098",
      "name": "Integer complexity",
      "definition": "固定正整数 n，输出只由常数1、+、×、括号组成且值为n的表达式，最小化1的个数。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "number of ones",
      "direction": "minimize",
      "configuration_parameters": {
        "n": "目标整数；表达式按树计数，不允许共享子表达式免费复用"
      },
      "human_baseline": "Arias de Reyna–van de Lune (2014) 及 Fuller 的算法给出人类精确结果；Iraids等研究展示截至10^12的历史计算范围。具体表达式尚须从构造算法重建。",
      "primary_sources": [
        "https://arxiv.org/abs/1404.2183",
        "https://cs.uwaterloo.ca/~shallit/DC2015/iraids2.pdf"
      ],
      "verification_cost": "低至中：大整数表达式求值。",
      "risks": "已知最优值表不等于已下载表达式；与允许共享中间量的加法链不同。",
      "recommendation": "后备候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-integer-complexity",
      "category": "数论与算术构造",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T099",
      "name": "Narrow admissible prime k-tuples",
      "definition": "固定 k，输出 k 个不同整数 H，使每个素数 p 下 H 不覆盖所有剩余类，最小化直径。",
      "solution_format": "见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。",
      "scalar_objective": "max(H)-min(H)",
      "direction": "minimize",
      "configuration_parameters": "No admitted v2 configuration. See discovery-only audit; all v1 solved calibration configurations excluded.",
      "human_baseline": "Engelsma–Sutherland/Polymath8 2013数据库有k=2..5000的元组、日期和贡献者；本次已下载并精确验证 k50直径246、k100直径558。",
      "primary_sources": [
        "https://math.mit.edu/~primegaps/",
        "https://math.mit.edu/~drew/PrimeGapsOberwolfach3.pdf"
      ],
      "verification_cost": "低：只需检验 p<=k 的素数，p>k自动成立。",
      "risks": "不是直接搜索素数；最窄admissible tuple与是否产生无穷素数簇分开。",
      "recommendation": "MVP候选",
      "reason": "主审补充的知名数学问题；候选资格与发布准备度分开。",
      "research_origin": "主审补充",
      "source_id": "root-admissible-tuple",
      "category": "数论与算术构造",
      "publication_status": "candidate_only",
      "baseline_audit": "example_witness_recomputed_not_full_task_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": true,
      "researcher_recommendation": "conditional",
      "uniform_score": "-J",
      "v1_mvp_recommended": true,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [
        {
          "task": "T099",
          "config": "MIT表k<=342标为optimal的配置，特别上一版k=50和100",
          "reason": "公开数据JS的comments明确optimal；不能把已重算见证当作待突破纪录。未标optimal的行另查开放状态。",
          "sources": [
            "https://math.mit.edu/~primegaps/"
          ]
        }
      ],
      "configuration_parameters_v1": {
        "k": "元组大小"
      },
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "T100",
      "name": "Factoring N! into N balanced factors",
      "category": "数论与算术构造",
      "definition": "For a fixed integer N, partition prime factors of N! among N integer factors and maximize the smallest factor; C(N) is the largest c for which N! can be factored into N factors all at least c.",
      "solution_format": "N positive integers with product exactly N!; verify exact product and minimum factor.",
      "scalar_objective": "min_i a_i, with the task maximizing this minimum (lower bound on C(N))",
      "direction": "maximize",
      "configuration_parameters": {
        "N": "positive integer; choose a fixed table row"
      },
      "human_baseline": "Guy and Selfridge studied the problem; the AlphaEvolve paper cites asymptotic C(N)/N=1/e−c0/log N+O(1/log^(1+c)N). Andrew Sutherland's public GuySelfridge.m implements a human search, and exact values C(N) for N≤10^4 are listed in the cited erdos-guy-selfridge repository/OEIS A034258. Retrieve a fixed row/value before freeze; not AI baseline.",
      "primary_sources": [
        "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/38.html",
        "https://github.com/teorth/erdos-guy-selfridge",
        "https://math.mit.edu/~drew/GuySelfridge.m",
        "https://oeis.org/A034258",
        "https://arxiv.org/abs/2511.02864"
      ],
      "verification_cost": "Low for witnesses (big integer product); exact optimum is a bin-covering problem and may be expensive.",
      "risks": "Product factorization means integer factors, not arbitrary reals; fixed N and exact table baseline are mandatory. Optimality verification can be NP-hard.",
      "recommendation": "后备候选",
      "reason": "Natural discrete construction score, exact cheap witness verification, and a public human algorithm plus extensive value table.",
      "research_origin": "algebra_analysis_round2.json",
      "source_id": "aa62",
      "publication_status": "candidate_only",
      "baseline_audit": "pending_configuration_and_witness_audit",
      "main_review": "自然标量任务候选；来源材料已定位不等于构造已复现。",
      "discovery_potential": "按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。",
      "mvp_recommended": false,
      "researcher_recommendation": "accept",
      "uniform_score": "J",
      "v1_mvp_recommended": false,
      "discovery_only_revision": "已证最优配置全部排除；开放配置须见v2审计，不沿用v1校准配置。",
      "discovery_entry_status": "pending_open_configuration_audit",
      "open_configuration_reviews": [],
      "excluded_configuration_groups": [],
      "latest_confirmation_status": "pending"
    },
    {
      "id": "N001",
      "name": "Shannon capacity: independent sets in strong powers of odd cycles",
      "category": "极值图与超图",
      "definition": "固定奇环C_q与幂d，构造其强积幂C_q^{⊠d}的独立集。提交Z_q^d中的互异词，每两词至少有一个坐标差不属于{0,1,−1}。",
      "solution_format": "显式词集合；不接受只声明极限容量或数量。",
      "scalar_objective": "number of independent words",
      "direction": "maximize",
      "configuration_parameters": {
        "q": 7,
        "d": 5
      },
      "human_baseline": "Polak–Schrijver (2018/2019)给出367词，原论文附录显式列出；不是2026全局Shannon容量现纪录。",
      "open_configuration": {
        "q": 7,
        "d": 5,
        "historical_lower_bound": 367,
        "published_upper_bound": 401,
        "record_to_attempt": "368词；截至本次核查一手材料未见第五幂更大构造",
        "status": "published_gap_located_witness_not_recomputed"
      },
      "primary_sources": [
        "https://arxiv.org/abs/1808.07438",
        "https://arxiv.org/html/1808.07438",
        "https://arxiv.org/html/2607.21517v1",
        "https://arxiv.org/abs/2608.30273"
      ],
      "verification_cost": "低：O(M²d)精确模整数运算；M约367。",
      "risks": "2018论文的367是人类基线；2026容量改进来自第10/200/500幂，不可移作第五幂分数。没有全局证明367非最优，gap不保证368存在。",
      "discovery_status": "open_configuration_evidence",
      "baseline_audit": "explicit_appendix_located_not_recomputed",
      "novelty": "原100项没有固定图强积幂的Shannon容量构造；不等于任意图最大独立数任务。",
      "mvp_recommended": true,
      "research_origin": "open_root_additions.json",
      "source_id_v2": "N001",
      "discovery_entry_status": "open_configuration_evidence",
      "publication_status": "candidate_only",
      "uniform_score": "J",
      "open_configuration_reviews": [
        {
          "review_id": "R014",
          "task_id": "N001",
          "parameters": {
            "q": 7,
            "power": 5
          },
          "scalar": "number of independent words ↑",
          "human_baseline": "Polak–Schrijver 2018/2019:367",
          "frontier_evidence": "published367–401;2026 capacity gains at other powers do not close this configuration",
          "sources": [
            "https://arxiv.org/html/1808.07438",
            "https://arxiv.org/html/2607.21517v1"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "N002",
      "name": "Smale mean value extremal constant",
      "category": "矩阵、格与代数极值",
      "definition": "固定degree n、复多项式p和非临界点a，对所有临界点ζ取|p(ζ)−p(a)|/(|p′(a)|·|ζ−a|)的最小值，再对提交对象最大化。",
      "solution_format": "精确多项式与点a，所有临界点距离/函数值的区间证书。",
      "scalar_objective": "min_{p′(ζ)=0} |p(ζ)−p(a)|/(|p′(a)| |ζ−a|)",
      "direction": "maximize",
      "configuration_parameters": {
        "n": "须再选未解次数，不能把小已解次数当open"
      },
      "human_baseline": "经典p(z)=z^n−z,a=0达到1−1/n；Smale猜想其最优。2026年Tao讨论Sendov后仍列该问题及现有上界。",
      "primary_sources": [
        "https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/"
      ],
      "verification_cost": "中至高：代数/区间计算认证临界点与最小比值。",
      "risks": "经典极难且现baseline被猜测已最优。没有证据说明能突破；仅补充研究池，不列MVP；具体未解次数未锁定。",
      "discovery_status": "high_risk_conjectured_optimal_pending_configuration",
      "baseline_audit": "formula_witness_available_configuration_pending",
      "novelty": "与Sendov的根到临界点距离目标不同。",
      "mvp_recommended": false,
      "research_origin": "open_root_additions.json",
      "source_id_v2": "N002",
      "discovery_entry_status": "high_risk_conjectured_optimal_pending_configuration",
      "publication_status": "candidate_only",
      "uniform_score": "J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "name": "Spherical cap covering / minimizing covering radius",
      "novelty": "Distinct from Tammes: minimize worst-case distance to nearest center rather than maximize nearest-neighbor separation.",
      "configurations": [
        {
          "dimension": 3,
          "n": 26,
          "human_baseline": "Hardin, Sloane and Smith (1994), covering radius 25.8449223 degrees"
        },
        {
          "dimension": 3,
          "n": 27,
          "human_baseline": "Hardin, Sloane and Smith (1994), covering radius 25.2509549 degrees"
        }
      ],
      "scalar": "minimize maximum angular distance from any sphere point to its nearest selected center",
      "open_status": "Maintained source calls entries putatively optimal, not proved globally optimal; exact optimum remains unverified/open.",
      "sources": [
        "https://neilsloane.com/coverings/index.html",
        "https://cohn.mit.edu/sloane/"
      ],
      "recommendation": "conditional; strong new task family",
      "next_check": "Download coordinates and find source-backed lower bounds for chosen N.",
      "source_id_v2": null,
      "id": "N003",
      "category": "球面与极值点集",
      "research_origin": "open_geometry_revision.json",
      "primary_sources": [
        "https://neilsloane.com/coverings/index.html",
        "https://cohn.mit.edu/sloane/"
      ],
      "scalar_objective": "minimize maximum angular distance from any sphere point to its nearest selected center",
      "direction": "minimize",
      "human_baseline": [
        {
          "dimension": 3,
          "n": 26,
          "human_baseline": "Hardin, Sloane and Smith (1994), covering radius 25.8449223 degrees"
        },
        {
          "dimension": 3,
          "n": 27,
          "human_baseline": "Hardin, Sloane and Smith (1994), covering radius 25.2509549 degrees"
        }
      ],
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "-J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "name": "Lattice sphere covering density",
      "novelty": "New task family absent from T001-T034; periodic lattice covering objective differs from point-set spherical covering and finite-container packing.",
      "configurations": [
        {
          "dimension": 6,
          "human_baseline": "Schürmann and Vallentin best-known lattice covering density 2.900024; exact optimum not known, since exact lattice covering values are reported through dimension 5"
        }
      ],
      "scalar": "minimize covering density among lattice coverings of R^d by congruent Euclidean balls",
      "open_status": "Dimension 6 is explicitly unresolved; source table provides an incumbent. A rigorous lower bound/gap and exact generator matrix were not checked here.",
      "sources": [
        "https://app.icerm.brown.edu/materials/Slides/sp-s18-w3/Lattice_Coverings_%5D_Mathieu_Dutour_Sikiric%2C_Institut_Rudjer_Boskovic.pdf",
        "https://arxiv.org/abs/2508.06446"
      ],
      "recommendation": "conditional; exact config evidence and human upper value exist, but not ready until lower bound and matrix are verified",
      "next_check": "Retrieve lattice basis and locate current rigorous lower bound.",
      "source_id_v2": null,
      "id": "N004",
      "category": "矩阵、格与代数极值",
      "research_origin": "open_geometry_revision.json",
      "primary_sources": [
        "https://app.icerm.brown.edu/materials/Slides/sp-s18-w3/Lattice_Coverings_%5D_Mathieu_Dutour_Sikiric%2C_Institut_Rudjer_Boskovic.pdf",
        "https://arxiv.org/abs/2508.06446"
      ],
      "scalar_objective": "minimize covering density among lattice coverings of R^d by congruent Euclidean balls",
      "direction": "minimize",
      "human_baseline": [
        {
          "dimension": 6,
          "human_baseline": "Schürmann and Vallentin best-known lattice covering density 2.900024; exact optimum not known, since exact lattice covering values are reported through dimension 5"
        }
      ],
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "-J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "name": "Lattice quantizer normalized second moment",
      "novelty": "New task family absent from T001-T034; optimizes Voronoi-cell second moment, not packing or covering density.",
      "configurations": [
        {
          "dimension": 13,
          "human_baseline": "Agrell and Allen (2023), K12 tensor Z product lattice NSM 0.071034583; previous reported record 0.074873919; conjectured lower bound 0.068721956"
        },
        {
          "dimension": 14,
          "human_baseline": "Agrell and Allen (2023), K12 tensor A2 product lattice NSM 0.071455542; conjectured lower bound 0.068308096"
        }
      ],
      "scalar": "minimize normalized second moment G = (1/(d Vol(V)^(1+2/d))) integral_V ||x||^2 dx over full-rank d-dimensional lattices and their Voronoi cells",
      "open_status": "Paper says optimality proofs only known through d=3. Lower bounds in table are conjectural, not certificates; incumbent lattice constructions and numerical NSM values are explicit.",
      "sources": [
        "https://arxiv.org/abs/2202.09605"
      ],
      "recommendation": "conditional candidate, strong math-structure fit",
      "next_check": "Check current table for post-2023 records and develop certified Voronoi moment evaluation; never represent conjectured bounds as proven.",
      "source_id_v2": null,
      "id": "N005",
      "category": "矩阵、格与代数极值",
      "research_origin": "open_geometry_revision.json",
      "primary_sources": [
        "https://arxiv.org/abs/2202.09605"
      ],
      "scalar_objective": "minimize normalized second moment G = (1/(d Vol(V)^(1+2/d))) integral_V ||x||^2 dx over full-rank d-dimensional lattices and their Voronoi cells",
      "direction": "minimize",
      "human_baseline": [
        {
          "dimension": 13,
          "human_baseline": "Agrell and Allen (2023), K12 tensor Z product lattice NSM 0.071034583; previous reported record 0.074873919; conjectured lower bound 0.068721956"
        },
        {
          "dimension": 14,
          "human_baseline": "Agrell and Allen (2023), K12 tensor A2 product lattice NSM 0.071455542; conjectured lower bound 0.068308096"
        }
      ],
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "-J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "N006",
      "name": "Exact tensor rank of 3x3 matrix multiplication over Q",
      "category": "矩阵、格与代数极值",
      "definition": "For the fixed matrix multiplication tensor M3 over Q, find a decomposition into r rank-one simple tensors minimizing r.",
      "solution_format": "Exact rational tensor factors whose outer-product sum equals M3 coefficientwise.",
      "scalar_objective": "number r of rank-one terms in the submitted exact decomposition",
      "direction": "minimize",
      "configuration_parameters": {
        "field": "Q fixed; do not transfer finite-field results to Q"
      },
      "human_baseline": {
        "status": "historical human construction plus later AI-assisted formal lower bound",
        "value": "Laderman 1976 gives rank ≤23 over every field; Bläser 2003 classical human lower bound ≥19. A 2026 Lean formalization by Andrey Ivanov, explicitly disclosing substantial ChatGPT/Codex assistance, reports ≥21 over every field; this lower-bound proof has not yet been independently re-audited by the parent reviewer. Current reported Q interval [21,23]. Tomar 2026 proves rank 23 over F2 and integer-coefficient algorithms, but not rank 23 over Q."
      },
      "primary_sources": [
        "https://www.ams.org/journals/bull/1976-82-01/S0002-9904-1976-13988-2/S0002-9904-1976-13988-2.pdf",
        "https://doi.org/10.1016/S0885-064X(02)00007-9",
        "https://github.com/AIV5/mmrank21",
        "https://arxiv.org/abs/2610.11823"
      ],
      "verification_cost": "High for finding; low exact identity check once factors submitted.",
      "risks": "Separate historical-human bounds from the AI-assisted reported all-fields lower bound; root has not yet independently re-audited it. The F2/integer rank-23 theorem does not settle Q rank.",
      "recommendation": "conditional",
      "reason": "Natural scalar and reported [21,23] Q interval, but the all-fields lower bound remains conditional on proof audit.",
      "source_id_v2": "NEW-ALG-01",
      "research_origin": "open_algebra_revision.json",
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "-J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "N007",
      "name": "Border rank of 3x3 matrix multiplication over C",
      "category": "矩阵、格与代数极值",
      "definition": "Minimize r such that M3 lies in the Zariski closure of rank-r tensors over C.",
      "solution_format": "Exact algebraic degeneration certificate giving a border-rank upper bound; lower-bound proofs are not scored as solutions in this construction track.",
      "scalar_objective": "number r of terms in the submitted valid algebraic degeneration",
      "direction": "minimize",
      "configuration_parameters": {
        "field": "C"
      },
      "human_baseline": {
        "status": "historical human bounds",
        "value": "Conner, Harper & Landsberg (2019) lower bound 17; Smirnov construction gives upper bound 20 (the upper bound is explicitly cited in Landsberg–Ottaviani 2015). Current sourced interval [17,20]."
      },
      "primary_sources": [
        "https://theoryofcomputing.org/articles/v011a011/v011a011.pdf",
        "https://arxiv.org/abs/1911.07981"
      ],
      "verification_cost": "High; degeneration algebraic details required.",
      "risks": "Do not confuse exact tensor rank 23 baseline with border rank 21; certificate format needs research review.",
      "recommendation": "conditional",
      "reason": "Distinct natural scalar from exact rank; existing human interval and constructions.",
      "source_id_v2": "NEW-ALG-02",
      "research_origin": "open_algebra_revision.json",
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "-J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "N008",
      "name": "Addition count for rank-23 3x3 matrix multiplication schemes",
      "category": "矩阵、格与代数极值",
      "definition": "Among exact noncommutative bilinear schemes of rank exactly 23, minimize scalar additions/subtractions under a fixed literature counting convention.",
      "solution_format": "Exact scheme plus explicit linear forms/output assembly and operation-count certificate.",
      "scalar_objective": "number of scalar additions/subtractions",
      "direction": "minimize",
      "configuration_parameters": {
        "multiplication_rank": "23 fixed",
        "counting_convention": "Must freeze treatment of signs, scalar multiples, and output combinations"
      },
      "human_baseline": {
        "status": "historical published schemes; AI provenance unknown unless explicitly disclosed",
        "value": "Nielsen 2026 reports 52 additions with Karstadt–Schwartz-style basis change (AI provenance undisclosed); Stapleton–Perminov report a 51-addition alternative-basis kernel plus five conversion additions =56 ordinary coordinates. Sidebottom 2026 reports 55 without basis change via human-directed AI-assisted search. Sun 2026 had 56. Sun cites older 60→59→58 progression. Scores use distinct basis/count conventions."
      },
      "primary_sources": [
        "https://arxiv.org/abs/2609.06588",
        "https://arxiv.org/abs/2609.32388",
        "https://arxiv.org/abs/2610.27451",
        "https://arxiv.org/abs/2604.27645"
      ],
      "verification_cost": "Low/medium; exact Brent identities and count once convention frozen.",
      "risks": "Must freeze whether basis conversions are counted. The 51 kernel is not a 51-addition ordinary-coordinate multiplication; it is 56 after conversions. Nielsen provenance unknown. Sidebottom 55 explicitly AI-assisted.",
      "recommendation": "conditional",
      "reason": "Natural scalar and exact published schemes, but score convention and human/AI provenance must be separated.",
      "source_id_v2": "NEW-ALG-03",
      "research_origin": "open_algebra_revision.json",
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "-J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "id": "N009",
      "name": "Waring rank of generic 4x4 determinant",
      "category": "矩阵、格与代数极值",
      "definition": "Find the least r for an exact identity det(X)=sum_{i=1}^r lambda_i L_i(X)^4 over C, where X is a generic 4x4 matrix and each L_i is linear in its 16 entries.",
      "solution_format": "Exact coefficients of linear forms and scalars; coefficientwise polynomial identity.",
      "scalar_objective": "number r of fourth-power terms in the submitted exact identity",
      "direction": "minimize",
      "configuration_parameters": {
        "field": "C",
        "matrix_size": "4 fixed",
        "power": "4 fixed (degree)"
      },
      "human_baseline": {
        "status": "historical human bounds",
        "value": "Derksen-Teitler 2015 lower bound 50. Johns-Teitler 2020 explicit d·d! construction gives upper bound 96 for d=4; interval [50,96]."
      },
      "primary_sources": [
        "https://doi.org/10.1016/j.jpaa.2015.03.001",
        "https://arxiv.org/abs/2004.06158"
      ],
      "verification_cost": "Medium; exact expansion of a 16-variable quartic identity.",
      "risks": "Do not confuse Waring rank with determinant tensor rank or border rank. Check for later improved upper bounds before freeze.",
      "recommendation": "conditional",
      "reason": "Strong natural scalar interval with exact witness verification; current-record search still needed.",
      "source_id_v2": "NEW-ALG-04",
      "research_origin": "open_algebra_revision.json",
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "-J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "name": "Minimum order n_6(4) of a 4-chromatic girth-at-least-6 graph",
      "definition": "最小化4色数且无长度小于6圈的简单图顶点数。",
      "configuration_parameters": {
        "chromatic_number": 4,
        "girth_at_least": 6
      },
      "human_baseline": "Exoo–Goedgebeur 2019给出66顶点显式见证；2026新文给64顶点见证，不能将新64说成人类baseline。",
      "best_known_interval": {
        "lower": 29,
        "upper": 64,
        "historical_human_upper": 66,
        "gap": 35
      },
      "primary_sources": [
        "https://arxiv.org/abs/1901.04881",
        "https://arxiv.org/abs/2608.23652"
      ],
      "verification_cost": "高；64图证书在2026论文中Lean核验，旧图需取得数据；证明最优仍需下界。",
      "recommendation": "conditional",
      "reason": "这是确有新标量目标且与regular cage不同的开放配置；只用旧人类上界时有66-29 gap。",
      "source_id_v2": null,
      "id": "N010",
      "category": "极值图与超图",
      "research_origin": "open_discrete_revision.json",
      "scalar_objective": "number of vertices",
      "direction": "minimize",
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "-J",
      "open_configuration_reviews": [
        {
          "review_id": "R015",
          "task_id": "N010",
          "parameters": {
            "chromatic_number": 4,
            "girth_at_least": 6
          },
          "scalar": "vertex count ↓",
          "human_baseline": "Exoo–Goedgebeur 2019:66",
          "frontier_evidence": "2026 paper29–64; latest64 provenance must be separately recorded; non3-colourability requires certificate",
          "sources": [
            "https://arxiv.org/abs/1901.04881",
            "https://arxiv.org/abs/2608.23652"
          ],
          "readiness": "source_located_not_release_ready"
        }
      ],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "name": "Perfect hash families PHF(N;k,v,t)",
      "definition": "An N-by-k array over v symbols such that for every t-column subset, at least one row assigns pairwise distinct symbols to those t entries. For fixed k,v,t, minimize N; equivalently maximize k at fixed N,v,t.",
      "configuration_parameters": {
        "N": 5,
        "k": 10,
        "v": 3,
        "t": 3
      },
      "human_baseline": "Walker II and Colbourn (2007) give an explicit PHF(5;10,3,3) construction (their figure/table and online PHF tables), with tabu-search and recursive/direct constructions reported. Their article describes the tables as best-known upper bounds and notes exact PHF numbers are generally unknown.",
      "best_known_interval": {
        "upper_rows_for_k10": 5,
        "lower_rows": null,
        "gap": null,
        "status": "concrete human witness verified in primary paper; exact minimum N for this row not verified"
      },
      "primary_sources": [
        "https://doi.org/10.1515/jmc.2007.008",
        "https://www.phftables.com/",
        "https://www.degruyterbrill.com/document/doi/10.1515/JMC.2007.008/html"
      ],
      "verification_cost": "Low; enumerate all 120 triples of columns and confirm at least one rainbow row for each.",
      "risks": "The public table is from 2007 and is an upper-bound catalogue; no current row-specific best lower bound or full downloadable witness was captured in this audit. PHF is a construction/optimization family, not a Boolean existence task if scoring maximum columns or minimum rows.",
      "recommendation": "research_pool_pending_open_gap",
      "reason": "Named, natural scalar and explicit human instance, but current open gap and witness artifact need row-level verification before use.",
      "source_id_v2": null,
      "id": "N011",
      "category": "组合设计",
      "research_origin": "open_discrete_revision.json",
      "scalar_objective": "number of rows N",
      "direction": "minimize",
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "-J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "pending"
    },
    {
      "name": "d-disjunct / d-cover-free binary matrices",
      "definition": "For fixed defective-item count d and number of columns n, minimize the number m of rows in a binary matrix such that no column is contained in the Boolean OR of any d other columns. This is the d-disjunct / superimposed-code / d-cover-free-family construction problem.",
      "configuration_parameters": {
        "d": 4,
        "n": 400,
        "alternative_configuration": {
          "d": 2,
          "n": 1600
        }
      },
      "human_baseline": "Van den Berg, Candès, Chinn, Levin, Olcott and Sing-Long (PNAS 2013) table a 4-disjunct 64-by-400 construction, obtained by shortening a covering-design-derived code; they also table a 2-disjunct 44-by-1600 construction from a standard code. The article gives explicit constructions/references and matching table context.",
      "best_known_interval": {
        "upper_rows_for_d4_n400": 64,
        "lower_rows": null,
        "gap": null,
        "status": "row-matched current lower bound not verified; 2013 paper reports general bounds and says constructions can be within factor two of lower bounds"
      },
      "primary_sources": [
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC3725070/",
        "https://doi.org/10.1073/pnas.1216318110",
        "https://arxiv.org/abs/1507.07368"
      ],
      "verification_cost": "Medium/high; for all columns, check each target column against every d-subset of other columns, O(n^(d+1) m) naively; optimized bitset certificate checks are possible.",
      "risks": "2013 record table is application-motivated and may be stale; no exact contemporary best/lower interval or archived matrix artifact was confirmed for the chosen rows. Distinguish disjunct from the weaker separable property and from error-tolerant variants.",
      "recommendation": "research_pool_pending_open_gap",
      "reason": "Has a natural numerical rows objective and concrete historical constructions; pending newer row-specific records and lower bounds.",
      "source_id_v2": null,
      "id": "N012",
      "category": "组合设计",
      "research_origin": "open_discrete_revision.json",
      "scalar_objective": "number of rows (tests)",
      "direction": "minimize",
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "-J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "confirmed_suitable"
    },
    {
      "name": "Global postage-stamp problem / extremal additive h-basis",
      "definition": "Given k positive stamp denominations and a limit s stamps per envelope, maximize the consecutive range n_s(A) such that every integer from 1 through that range is expressible as a sum of at most s denominations (equivalently add zero and use exactly s summands). The classical unrestricted two-stamp task is n_2(k).",
      "configuration_parameters": {
        "recommended_open_configuration": {
          "k": 25,
          "s": 2,
          "domain": "unrestricted nonnegative denomination set; do not impose restricted-basis condition"
        },
        "closed_general_range": {
          "k": "at most 24",
          "s": 2
        },
        "restricted_data_range": {
          "k": "up to 47",
          "s": 2,
          "this_is_a_different_restricted_objective": true
        }
      },
      "human_baseline": "Kohonen (2015), arXiv:1503.03416, states unrestricted n_2(k) is known only through k=24; Sloane's OEIS A001212 records n_2(24)=212 and authorship/history. Kohonen separately enumerates all extremal restricted bases through k=47, with n*_2(47)=734 and explicit bases. Do not treat 734 as a baseline for unrestricted n_2(47). The GStamps public library (Colisson Palais, Dumas, Galan, Grenet, Maignan, Roche; 2026) implements local/global search and basis construction but this audit did not extract a verified best unrestricted k=25 witness/value from its benchmark files.",
      "best_known_interval": {
        "k25_lower": null,
        "upper": null,
        "gap": null,
        "status": "open by sequence cutoff in 2015 source, but current human best-known numeric k=25 witness and bound need verification; no benchmark row yet"
      },
      "primary_sources": [
        "https://arxiv.org/abs/1503.03416",
        "https://oeis.org/A001212",
        "https://arxiv.org/abs/2601.21423",
        "https://github.com/jgdumas/GStamps"
      ],
      "verification_cost": "Low for validating one basis range by enumerating all sums, but exact global maximality requires a substantial combinatorial search/proof; performance depends on k,s.",
      "risks": "Unrestricted n_2(k) and restricted n*_2(k) are different. General values through 24 are solved; restricted values through 47 do not imply unrestricted values. New 2026 GStamps algorithms are useful but their reported constructed basis is not automatically an optimality result. This is distinct from T049's difference-basis objective.",
      "recommendation": "research_pool_pending_open_gap",
      "reason": "A well-defined open named optimization problem and public human computation record; k=25 is the natural next general configuration, but freeze only after extracting a specific current human basis and numeric range from a primary artifact.",
      "source_id_v2": null,
      "id": "N013",
      "category": "加法组合与离散构造",
      "research_origin": "open_discrete_revision.json",
      "scalar_objective": "largest R such that all integers 0..R are sums of at most h submitted denominations",
      "direction": "maximize",
      "discovery_entry_status": "candidate_pending_configuration_and_current_record_audit",
      "mvp_recommended": false,
      "publication_status": "candidate_only",
      "uniform_score": "J",
      "open_configuration_reviews": [],
      "latest_confirmation_status": "confirmed_suitable"
    }
  ],
  "configuration_reviews": [
    {
      "review_id": "R001",
      "task_id": "T001",
      "parameters": {
        "n": 26,
        "container": "unit square"
      },
      "scalar": "common radius ↑",
      "human_baseline": "Nurmela–Östergård 1999: 0.096362339010",
      "frontier_evidence": "record row not marked proved optimal; no matching numerical upper bound frozen",
      "sources": [
        "https://packomania.com/csq/"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R002",
      "task_id": "T001",
      "parameters": {
        "n": 32,
        "container": "unit square"
      },
      "scalar": "common radius ↑",
      "human_baseline": "Boll et al. 2000: 0.087858157088",
      "frontier_evidence": "same caveat",
      "sources": [
        "https://packomania.com/csq/"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R003",
      "task_id": "T002",
      "parameters": {
        "n": 26
      },
      "scalar": "unit-square container side ↓",
      "human_baseline": "Friedman 1997: (7+3sqrt(2))/2 ≈5.62132034356",
      "frontier_evidence": "maintained project reports verified interval [5.545,5.62132034356]; lower proof replay not repeated here",
      "sources": [
        "https://squaremath.org/cases/26.html"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R004",
      "task_id": "T014",
      "parameters": {
        "n": 11,
        "domain": "unit square"
      },
      "scalar": "minimum triangle area ↑",
      "human_baseline": "Goldberg 1972: 1/27",
      "frontier_evidence": "record construction; unrestricted optimum not established by checked page",
      "sources": [
        "https://math.tejstead.com/heilbronn/square/"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R005",
      "task_id": "T014",
      "parameters": {
        "n": 12,
        "domain": "unit square"
      },
      "scalar": "minimum triangle area ↑",
      "human_baseline": "Comellas–Yebra 2001: 0.0325988586918196…",
      "frontier_evidence": "record construction; unrestricted optimum not established by checked page",
      "sources": [
        "https://math.tejstead.com/heilbronn/square/"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R006",
      "task_id": "T029",
      "parameters": {
        "n": 25
      },
      "scalar": "number of unit-distance pairs ↑",
      "human_baseline": "Engel et al. human construction:72",
      "frontier_evidence": "agent reports current interval72–73; current certificate ledger needs root replay and provenance freeze",
      "sources": [
        "https://arxiv.org/abs/2406.15317",
        "https://artwaste.land/strata/every-edge-but-one/"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R007",
      "task_id": "T032",
      "parameters": {
        "order": 55
      },
      "scalar": "primitive outer side ↓",
      "human_baseline": "Bernard Moss 2020:740",
      "frontier_evidence": "smallest known, not proved minimum; Bouwkamp file located not replayed",
      "sources": [
        "https://www.squaring.net/sq/ss/spss/o55/spsso55.html"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R008",
      "task_id": "T035",
      "parameters": {
        "degree": 4,
        "girth": 10
      },
      "scalar": "vertex count ↓",
      "human_baseline": "Exoo et al. 2025/2026:320",
      "frontier_evidence": "paper interval243–320; obtain320-vertex graph before admitting",
      "sources": [
        "https://arxiv.org/abs/2511.07247"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R009",
      "task_id": "T060",
      "parameters": {
        "v": 24,
        "k": 14,
        "t": 4
      },
      "scalar": "block count ↓",
      "human_baseline": "historical covering repository construction:23; contributor/blocklist pending",
      "frontier_evidence": "2026 Lean project reports20–23; lower proof AI-assisted; root read source but did not replay",
      "sources": [
        "https://github.com/jamesyc/covering",
        "https://dmgordon.org/covering-designs/"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R010",
      "task_id": "T060",
      "parameters": {
        "v": 25,
        "k": 15,
        "t": 5
      },
      "scalar": "block count ↓",
      "human_baseline": "historical upper bound42; blocklist pending",
      "frontier_evidence": "same project reports34–42; human witness provenance pending",
      "sources": [
        "https://github.com/jamesyc/covering"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R011",
      "task_id": "T066",
      "parameters": {
        "n": 68,
        "k": 15,
        "q": 2
      },
      "scalar": "minimum Hamming distance ↑",
      "human_baseline": "Grassl construction [68,15,24]",
      "frontier_evidence": "root read table24–26; explicit construction chain exists, generator not reconstructed",
      "sources": [
        "https://www.codetables.de/BKLC/BKLC.php?k=15&n=68&q=2"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R012",
      "task_id": "T067",
      "parameters": {
        "n": 17,
        "distance": 6
      },
      "scalar": "number of codewords ↑",
      "human_baseline": "Milshtein 2019:258",
      "frontier_evidence": "root read Brouwer258–340; archive codeword list and newer-record search pending",
      "sources": [
        "https://aeb.win.tue.nl/codes/binary-1.html"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R013",
      "task_id": "T089",
      "parameters": {
        "n": 29
      },
      "scalar": "absolute determinant ↑",
      "human_baseline": "Orrick et al.:2^28·7^12·320",
      "frontier_evidence": "Brent conjectures optimality; historicalupper329·7^12·2^28; high risk incumbent already optimal",
      "sources": [
        "https://maths-people.anu.edu.au/~brent/maxdet/order29/",
        "https://maths-people.anu.edu.au/~brent/pd/Brent-maxdet-RMIT.pdf"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R014",
      "task_id": "N001",
      "parameters": {
        "q": 7,
        "power": 5
      },
      "scalar": "number of independent words ↑",
      "human_baseline": "Polak–Schrijver 2018/2019:367",
      "frontier_evidence": "published367–401;2026 capacity gains at other powers do not close this configuration",
      "sources": [
        "https://arxiv.org/html/1808.07438",
        "https://arxiv.org/html/2607.21517v1"
      ],
      "readiness": "source_located_not_release_ready"
    },
    {
      "review_id": "R015",
      "task_id": "N010",
      "parameters": {
        "chromatic_number": 4,
        "girth_at_least": 6
      },
      "scalar": "vertex count ↓",
      "human_baseline": "Exoo–Goedgebeur 2019:66",
      "frontier_evidence": "2026 paper29–64; latest64 provenance must be separately recorded; non3-colourability requires certificate",
      "sources": [
        "https://arxiv.org/abs/1901.04881",
        "https://arxiv.org/abs/2608.23652"
      ],
      "readiness": "source_located_not_release_ready"
    }
  ],
  "latest_confirmation_report": "confirmation_summary.json",
  "confirmed_suitable_families": 91,
  "confirmed_configuration_records": 94,
  "admission_scope": "research selection under relaxed baseline standard; not solver/evaluator release"
}
```

</details>

### 准入与排除规则

<details>
<summary>准入与排除规则：完整记录</summary>

迁入来源：`discovery_only_policy.json`；原文件SHA-256：`710d27172be87ac0cd78d3dbf4521a666d45248b2ceddb11c2c33dcfe870b905`。

```json
{
  "date": "2026-11-03",
  "scope": "仅发现轨；不保留已解校准配置",
  "rules": [
    "已证明最优、匹配通用上/下界、或由简单构造达到理论极值的配置，全部排除。",
    "整个任务的所有参数已有最优值定理，则整题排除；只有部分参数已解时保留家族、替换参数。",
    "未证明最优仅说明尚未闭合，不保证能超过当前纪录；长期猜测已最优者标高风险。",
    "入选具体配置必须有实际人类构造、同一数学定义下的单一标量、公开开放状态证据；待核项不得计入正式发现任务数。",
    "human历史基线与截至检索时可能包含AI的现纪录分开；超过历史基线不等于新纪录。",
    "不通过改变已解任务定义、任意罚函数、加大已解参数等方式凑数。"
  ],
  "excluded_tasks": [
    {
      "id": "T018",
      "reason": "最大无空凸六边形点集=29；h(6)=30已在2024证明并形式验证。旧表误将精确30归于Gerken/Nicolas；两人2006证明的是存在有限阈值。",
      "sources": [
        "https://arxiv.org/abs/2403.00737",
        "https://arxiv.org/abs/2403.17370"
      ]
    },
    {
      "id": "T050",
      "reason": "当前定义为有限阿贝尔群；Green–Ruzsa已确定每个有限阿贝尔群的最大sum-free子集大小。",
      "sources": [
        "https://arxiv.org/abs/math/0307142"
      ]
    },
    {
      "id": "T091",
      "reason": "2026年Sendov证明使当前标量C(n)=1；z^n−1已取等号。该定义下所有次数无纪录提升空间。",
      "sources": [
        "https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/",
        "https://github.com/teorth/sendov"
      ]
    }
  ],
  "excluded_configurations": [
    {
      "task": "T044",
      "config": "Golomb标记数m<=28，包括上一版m=10,12",
      "reason": "已证明最优，排除。m>28仅作替代候选，需逐项定位现纪录。",
      "sources": [
        "https://blogs.distributed.net/2022/11/"
      ]
    },
    {
      "task": "T073",
      "config": "LABS能量长度N<=66，包括上一版N=66,E=257",
      "reason": "Packebusch–Mertens给出精确最优结果；排除。更大长度是否近期已解另查。",
      "sources": [
        "https://arxiv.org/abs/1512.02475"
      ]
    },
    {
      "task": "T009",
      "config": "Tammes球面S²点数N=8、12",
      "reason": "已证明最优；排除。",
      "sources": [
        "https://cohn.mit.edu/spherical-codes/"
      ]
    },
    {
      "task": "T060",
      "config": "C(8,4,3)=14，C(10,4,3)=30",
      "reason": "Steiner四元系达到计数下界；排除，不能把构造库所有行都当未解。",
      "sources": [
        "https://dmgordon.org/covering-designs/"
      ]
    },
    {
      "task": "T066",
      "config": "二元[23,12,7] Golay码，[15,7,5] BCH码",
      "reason": "这些参数最优最小距离已确定；排除。",
      "sources": [
        "https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html"
      ]
    },
    {
      "task": "T014",
      "config": "上一版Heilbronn正方形n=7、8",
      "reason": "已知最优，排除。较新n=9状态需核查，不自动当open。",
      "sources": [
        "https://math.tejstead.com/heilbronn/square/"
      ]
    },
    {
      "task": "T090/T085",
      "config": "维数8、24的最优球装填/匹配Cohn–Elkies上界",
      "reason": "E8、Leech格已达最优；排除这些配置。",
      "sources": [
        "https://arxiv.org/abs/1603.04246",
        "https://arxiv.org/abs/1603.06518"
      ]
    },
    {
      "task": "T075/T076",
      "config": "奇素数p≡3 mod4的Legendre周期序列已达到能量p−1或PSL=1的情形",
      "reason": "匹配奇长度非零周期自相关绝对值至少1的下界；排除这些配置。",
      "sources": [
        "https://arxiv.org/abs/1401.2530"
      ]
    },
    {
      "task": "T099",
      "config": "MIT表k<=342标为optimal的配置，特别上一版k=50和100",
      "reason": "公开数据JS的comments明确optimal；不能把已重算见证当作待突破纪录。未标optimal的行另查开放状态。",
      "sources": [
        "https://math.mit.edu/~primegaps/"
      ]
    },
    {
      "task": "T032",
      "config": "order=21, primitive side=112",
      "reason": "唯一最小阶简单完美平方分割；移除这一配置，order55另审。",
      "sources": [
        "https://www.squaring.net/sq/ss/spss/o21/spsso21.html"
      ]
    },
    {
      "task": "T038",
      "config": "n=30,F={C4}边85；n=30,F={C3,C4}边76",
      "reason": "Afzaly–McKay对应项标为精确极值，并非仅构造下界；移除这些小配置。",
      "sources": [
        "https://users.cecs.anu.edu.au/~bdm/data/extremal.html"
      ]
    },
    {
      "task": "T084",
      "config": "正号sign uncertainty维数12的已知sharp配置",
      "reason": "已达精确常数；不能把另一符号、不同维数或不同平方约定的值混用。",
      "sources": [
        "https://arxiv.org/abs/1712.04438",
        "https://arxiv.org/abs/2608.15415"
      ]
    }
  ],
  "additional_exclusion_warning": {
    "task": "矩阵乘法张量秩新候选",
    "config": "F2与整数上的3×3 rank<23",
    "reason": "2026年10月预印本声称形式化计算证明rank=23。保守移出可尝试配置，结论限该域及整数；不据此排除有理/实/复系数或其他形状。",
    "sources": [
      "https://arxiv.org/abs/2610.11823"
    ]
  },
  "high_risk_configurations": [
    {
      "task": "T002",
      "config": "n=17",
      "reason": "2026维护项目仍标verified open，但已记录全局等号证明候选与Lean形式化声称。先暂停选入，优先n=26。",
      "sources": [
        "https://squaremath.org/cases/17.html",
        "https://squaremath.org/cases/26.html"
      ]
    },
    {
      "task": "T014",
      "config": "n=9,10",
      "reason": "全局浮点求解报告已数值认证现构造在容差内最优；不是严格数学证明，也不宜优先期待突破。改用n>=11。",
      "sources": [
        "https://math.tejstead.com/heilbronn/square/"
      ]
    }
  ]
}
```

</details>

### 首批任务配置选型

<details>
<summary>首批任务配置选型：完整记录</summary>

迁入来源：`configuration_selection.json`；原文件SHA-256：`4971a268e40fa7b4ccc66d62b4121362298b87b1fa846d1f2564e6b2bf223d8a`。

```json
{
  "version": "configuration-selection-v1",
  "date": "2026-11-04",
  "scope": "20个任务、35个配置均已实现并通过Sol逐配置验收。",
  "category_count": 10,
  "task_count": 20,
  "selected_configuration_count": 35,
  "implemented_accepted_configuration_count": 35,
  "additional_selected_configuration_count": 0,
  "maximum_configurations_per_task": 5,
  "status_legend": {
    "accepted_by_sol": "已实现、已逐配置验收，可正式运行",
    "selected_pending_implementation": "新增选型，已定位来源，尚未完成基线复现和实现验收，不可计入完成数"
  },
  "rules": [
    "每题1至5个配置，不凑满；同参数重复运行不增加配置数",
    "仅发现轨：已证最优配置排除",
    "公开人类基线可以弱于纪录，但正式发布前须有已重算见证",
    "本次公开配置未划为隐藏测试集",
    "正式总分按任务等权；具体汇总公式尚未冻结",
    "保留现有配置ID；T009-C01退役，不复用",
    "T002-C02(n17)因公开最优性证明重建记录退役，替换为T002-C04(n38)，不复用旧ID"
  ],
  "tasks": [
    {
      "task_id": "T001",
      "name": "等圆装入正方形",
      "category": "几何装填与覆盖",
      "direction": "maximize",
      "selection_reason": "26、32、50个圆覆盖三个规模；32圆可复用已保存的等圆对照资产。避免只取相邻数量。",
      "configuration_count": 3,
      "configurations": [
        {
          "id": "T001-C01",
          "parameters": {
            "n": 26,
            "container": "unit square"
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": "96362339/1000000000",
          "primary_sources": [
            "https://packomania.com/csq/csq26.html",
            "https://packomania.com/csq/",
            "https://packomania.com/csq/txt/csq26.txt"
          ],
          "record_archive": "tasks/t001/records.json",
          "witness": "reports/witnesses/T001/T001-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        },
        {
          "id": "T001-C02",
          "parameters": {
            "n": 32,
            "container": "unit square"
          },
          "parameter_label": "n=32",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "Packomania table; exact publication attribution not independently resolved.",
          "source_reported_metric": "表中共同半径0.087858157088，未冻结为正式分数。",
          "baseline_verified_objective": "10982269511/125000000000",
          "primary_sources": [
            "https://packomania.com/csq/",
            "https://packomania.com/csq/csq32.html"
          ],
          "witness_source": "https://packomania.com/csq/txt/csq32.txt",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "来源以最佳已知构造列出。表格用粗体表示已证最优；发布前须保存该行原始标记并再次核查。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "精确有理数检查边界及496对距离；圆半径可保守缩小。",
          "record_archive": "tasks/t001/records.json",
          "witness": "reports/witnesses/T001/T001-C02/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Packomania 的32等圆坐标；也可复用T005-C02的人类等圆见证，重新按共同半径目标评分。"
        },
        {
          "id": "T001-C03",
          "parameters": {
            "n": 50,
            "container": "unit square"
          },
          "parameter_label": "n=50",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "Packomania table; table's reference [14] author and year were not resolved.",
          "source_reported_metric": "表中共同半径0.071377103865，未冻结为正式分数。",
          "baseline_verified_objective": "14275420753/200000000000",
          "primary_sources": [
            "https://packomania.com/csq/",
            "https://packomania.com/csq/csq50.html"
          ],
          "witness_source": "https://packomania.com/csq/txt/csq50.txt",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "最佳已知表包含该实例；未发现最优性证明。原始粗体标记与作者归属尚须归档。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "精确边界及1225对距离检查。本次坐标链接抓取失败，须重新取得见证。",
          "record_archive": "tasks/t001/records.json",
          "witness": "reports/witnesses/T001/T001-C03/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Packomania 的50等圆坐标及参考文献[14]；获取时记录具体作者和年份。"
        }
      ]
    },
    {
      "task_id": "T002",
      "name": "单位正方形装入正方形",
      "category": "几何装填与覆盖",
      "direction": "minimize",
      "selection_reason": "26、29、38个正方形覆盖不同构造；17个配置因公开最优性证明及重建记录退役。38个采用Göbel公开斜带构造。",
      "configuration_count": 3,
      "configurations": [
        {
          "id": "T002-C01",
          "parameters": {
            "n": 26
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": "7/2+3/2*sqrt2",
          "primary_sources": [
            "https://erich-friedman.github.io/papers/squares/squares.html",
            "https://squaremath.org/cases/26.html"
          ],
          "record_archive": "tasks/t002/records.json",
          "witness": "reports/witnesses/T002/T002-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        },
        {
          "id": "T002-C03",
          "parameters": {
            "n": 29
          },
          "parameter_label": "n=29",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "Thomas Schadt (2025) found this packing by simulated annealing. The source repository provides 105-decimal center/angle coordinates. The saved benchmark witness was reconstructed from the exact rational corners retained by jlevy/squares and converted to center plus rational half-angle form. This is Schadt, not the earlier Gensane–Ryckelynck packing.",
          "source_reported_metric": "历史综述给s(29)<5.9344；不将其当作当前纪录。",
          "baseline_verified_objective": "2966942899906512939318226046481160904289990651293931822604648091421/500000000000000000000000000000000000000000000000000000000000000000",
          "primary_sources": [
            "https://erich-friedman.github.io/papers/squares/squares.html",
            "https://squaremath.org/cases/29.html",
            "https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record"
          ],
          "witness_source": "https://squaremath.org/cases/29.html",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "当前实例页明确标记open，并分别给上下界。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "允许任意旋转；对406对正方形使用严格分离轴检查，包含条件使用精确数或保守区间。",
          "record_archive": "tasks/t002/records.json",
          "witness": "reports/witnesses/T002/T002-C03/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Gensane–Ryckelynck传统计算构造，2005论文及Friedman图12。近期改进另列，不覆盖历史人类来源。"
        },
        {
          "id": "T002-C04",
          "parameters": {
            "n": 38
          },
          "parameter_label": "n=38",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "Friedman DS7 Figure 1 presents Göbel’s diagonal-strip construction, side 6+1/sqrt(2), and n=38.",
          "source_reported_metric": "边长6+sqrt(2)/2，尚未由本项目重算。",
          "baseline_verified_objective": "6+1/2*sqrt2",
          "primary_sources": [
            "https://erich-friedman.github.io/papers/squares/squares.html",
            "https://squaremath.org/cases/38.html"
          ],
          "witness_source": "https://squaremath.org/cases/38.html",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "当前38点实例页明确标记open，所列上下界有差距。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "重建斜带公式或取得坐标，用Q(sqrt2)或有理数精确检查703对正方形及边界。",
          "record_archive": "tasks/t002/records.json",
          "witness": "reports/witnesses/T002/T002-C04/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Göbel 1979斜带构造；Friedman综述图1给边长6+sqrt(2)/2。"
        }
      ]
    },
    {
      "task_id": "T005",
      "name": "变半径圆装填",
      "category": "几何装填与覆盖",
      "direction": "maximize",
      "selection_reason": "保留26和32两个已验收配置。先补强变半径公开纪录见证，不再扩数量。",
      "configuration_count": 2,
      "configurations": [
        {
          "id": "T005-C01",
          "parameters": {
            "n": 26,
            "container": "unit square",
            "radii": "variable"
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": "125271039413/50000000000",
          "primary_sources": [
            "https://packomania.com/csq/txt/csq26.txt",
            "https://www.packomania.com/csqv/csqv.html"
          ],
          "record_archive": "tasks/t005/records.json",
          "witness": "reports/witnesses/T005/T005-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "等圆人类构造转用于变半径任务。公开变半径纪录坐标未复现。"
          ]
        },
        {
          "id": "T005-C02",
          "parameters": {
            "n": 32,
            "container": "unit square",
            "radii": "variable"
          },
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": "10982269511/3906250000",
          "primary_sources": [
            "https://packomania.com/csq/txt/csq26.txt",
            "https://www.packomania.com/csqv/csqv.html"
          ],
          "record_archive": "tasks/t005/records.json",
          "witness": "reports/witnesses/T005/T005-C02/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "等圆人类构造转用于变半径任务。公开变半径纪录坐标未复现。"
          ]
        }
      ]
    },
    {
      "task_id": "T009",
      "name": "Tammes 球面码",
      "category": "球面与极值点集",
      "direction": "maximize",
      "selection_reason": "16、17、19点均有传统文献与坐标。15点及24点带最优性证明标记，排除。",
      "configuration_count": 3,
      "configurations": [
        {
          "id": "T009-C02",
          "parameters": {
            "n": 16,
            "space": "S2",
            "objective": "minimum pairwise angular separation in radians"
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 0.9118367215999161,
          "primary_sources": [
            "https://spherical-codes.org/"
          ],
          "record_archive": "tasks/t009/records.json",
          "witness": "reports/witnesses/T009/T009-C02/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "采用开放的16点配置，替换已获最优性证明的15点配置。正式成绩使用角度区间下界。"
          ]
        },
        {
          "id": "T009-C03",
          "parameters": {
            "n": 17,
            "space": "S2",
            "objective": "minimum pairwise angular separation in radians"
          },
          "parameter_label": "n=17",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "Public coordinates at spherical-codes.org; the n=17 source row cites Danzer (1986).",
          "source_reported_metric": "表列余弦0.628094415071；正式目标仍为最小角度。",
          "baseline_verified_objective": 0.8916944491515696,
          "primary_sources": [
            "https://spherical-codes.org/",
            "https://doi.org/10.1016/0012-365X(86)90002-6",
            "https://spherical-codes.org/data/3/17"
          ],
          "witness_source": "https://spherical-codes.org/data/3/17",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "表中3维17点未带最优标记*；这是来源证据，不构成穷尽全部证明的声明。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "136对归一化点积和角度下界，用精确比值及向外舍入区间认证。",
          "record_archive": "tasks/t009/records.json",
          "witness": "reports/witnesses/T009/T009-C03/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Danzer 1986构造；Cohn表提供坐标与参考文献。"
        },
        {
          "id": "T009-C04",
          "parameters": {
            "n": 19,
            "space": "S2",
            "objective": "minimum pairwise angular separation in radians"
          },
          "parameter_label": "n=19",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "Public coordinates at spherical-codes.org; the n=19 source row cites Lazić, Šenk and Šeškar (1987).",
          "source_reported_metric": "表列余弦0.673116887561；正式目标仍为最小角度。",
          "baseline_verified_objective": 0.8323809277763071,
          "primary_sources": [
            "https://spherical-codes.org/",
            "https://spherical-codes.org/data/3/19"
          ],
          "witness_source": "https://spherical-codes.org/data/3/19",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "表中3维19点未带最优标记*；发布前再次核查。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "171对归一化点积和角度下界，沿用严格区间方法。",
          "record_archive": "tasks/t009/records.json",
          "witness": "reports/witnesses/T009/T009-C04/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Lazić、Šenk、Šeškar 1987构造；Cohn表提供坐标与参考文献。"
        }
      ]
    },
    {
      "task_id": "T014",
      "name": "正方形中的 Heilbronn 问题",
      "category": "球面与极值点集",
      "direction": "maximize",
      "selection_reason": "11、12、16点有不同公开构造，三角形枚举仍很小。不选已证最优的小规模。",
      "configuration_count": 3,
      "configurations": [
        {
          "id": "T014-C01",
          "parameters": {
            "n": 11
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": "1/27",
          "primary_sources": [
            "https://math.tejstead.com/heilbronn/square/11/points.txt"
          ],
          "record_archive": "tasks/t014/records.json",
          "witness": "reports/witnesses/T014/T014-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        },
        {
          "id": "T014-C02",
          "parameters": {
            "n": 12
          },
          "parameter_label": "n=12",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "F. Comellas and J. Yebra, December 2001",
          "source_reported_metric": "最小面积约0.0325988586918196。",
          "baseline_verified_objective": "101871433411936556933637520697548102056943915772631725289/3125000000000000000000000000000000000000000000000000000000",
          "primary_sources": [
            "https://math.tejstead.com/heilbronn/square/",
            "https://math.tejstead.com/heilbronn/square/12/points.txt"
          ],
          "witness_source": "https://math.tejstead.com/heilbronn/square/12/points.txt",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "来源将n≥11列为最佳已知构造，未宣称最优。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "精确枚举220个三角形；有限小数坐标按有理数处理并重算保守面积。",
          "record_archive": "tasks/t014/records.json",
          "witness": "reports/witnesses/T014/T014-C02/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Comellas–Yebra 2001构造，公开坐标。"
        },
        {
          "id": "T014-C03",
          "parameters": {
            "n": 16
          },
          "parameter_label": "n=16",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "Mark Beyleveld, August 2006",
          "source_reported_metric": "最小面积7/341，待本项目重算。",
          "baseline_verified_objective": "7/341",
          "primary_sources": [
            "https://math.tejstead.com/heilbronn/square/",
            "https://math.tejstead.com/heilbronn/square/16/points.txt"
          ],
          "witness_source": "https://math.tejstead.com/heilbronn/square/16/points.txt",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "来源将该实例标记为record，未宣称最优。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "精确枚举560个三角形；重建精确坐标时才可采用7/341，否则使用实际坐标的保守成绩。",
          "record_archive": "tasks/t014/records.json",
          "witness": "reports/witnesses/T014/T014-C03/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Beyleveld 2006构造，公开坐标；来源给面积7/341。"
        }
      ]
    },
    {
      "task_id": "T035",
      "name": "最小笼图",
      "category": "极值图与超图",
      "direction": "minimize",
      "selection_reason": "保留(4,10)。初始图已较大，先改善起点和搜索；其他参数须另查开放性与见证。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T035-C01",
          "parameters": {
            "degree": 4,
            "girth": 10
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 320,
          "primary_sources": [
            "https://arxiv.org/abs/2511.07247v2",
            "https://houseofgraphs.org/meta-directory/cages",
            "https://github.com/AGT-Kulak/smallRegGirthGraphs/blob/main/genLifts/data/graphs/cage/n320_k4_g10.g6"
          ],
          "record_archive": "tasks/t035/records.json",
          "witness": "reports/witnesses/T035/T035-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        }
      ]
    },
    {
      "task_id": "T044",
      "name": "最短 Golomb ruler",
      "category": "加法组合与离散构造",
      "direction": "minimize",
      "selection_reason": "29、30、32刻度具有公开代数构造，可精确验证。避免已证最优的较小刻度数。",
      "configuration_count": 3,
      "configurations": [
        {
          "id": "T044-C01",
          "parameters": {
            "marks": 29
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 623,
          "primary_sources": [
            "https://cube20.org/golomb/"
          ],
          "record_archive": "tasks/t044/records.json",
          "witness": "reports/witnesses/T044/T044-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        },
        {
          "id": "T044-C02",
          "parameters": {
            "marks": 30
          },
          "parameter_label": "30个刻度",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "Reconstructed from the public rulers-all-00 row; checked against public metadata and then rechecked exactly in the task checker.",
          "source_reported_metric": null,
          "baseline_verified_objective": 680,
          "primary_sources": [
            "https://cube20.org/golomb/"
          ],
          "witness_source": "https://cube20.org/golomb/rulers-all-00.zip",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "来源将较大规模称为possibly optimal，未提供30刻度的全局最优证明。旧页面的OGR-28进度已过时，不用作当前证明状态。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "重建30个刻度，精确检查435个正差互异。压缩档链接已定位，尚未下载重算。",
          "record_archive": "tasks/t044/records.json",
          "witness": "reports/witnesses/T044/T044-C02/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Rokicki–Dogon公开模尺数据与Singer/Bose–Chowla构造；见证在rulers-all-00压缩档。"
        },
        {
          "id": "T044-C03",
          "parameters": {
            "marks": 32
          },
          "parameter_label": "32个刻度",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "Reconstructed from the public rulers-all-00 row; checked against public metadata and then rechecked exactly in the task checker.",
          "source_reported_metric": null,
          "baseline_verified_objective": 784,
          "primary_sources": [
            "https://cube20.org/golomb/"
          ],
          "witness_source": "https://cube20.org/golomb/rulers-all-00.zip",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "来源未对32刻度证明最优；发布前核对最新证明状态。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "精确检查496个正差互异；最短长度直接由最大刻度重算。",
          "record_archive": "tasks/t044/records.json",
          "witness": "reports/witnesses/T044/T044-C03/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "同一公开数据档中的32刻度构造；记录该行方法、素数幂、乘子及作者。"
        }
      ]
    },
    {
      "task_id": "T060",
      "name": "覆盖设计",
      "category": "组合设计",
      "direction": "minimize",
      "selection_reason": "仅C(24,14,4)。先取得更强的23块公开构造，再考虑增加配置。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T060-C01",
          "parameters": {
            "v": 24,
            "k": 14,
            "t": 4
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 62,
          "primary_sources": [
            "https://arxiv.org/html/math/9502238",
            "https://ljcr.dmgordon.org/cover.html"
          ],
          "record_archive": "tasks/t060/records.json",
          "witness": "reports/witnesses/T060/T060-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开方法对照62块，本地传统搜索40块。公开23块纪录见证未取到。"
          ]
        }
      ]
    },
    {
      "task_id": "T066",
      "name": "线性码最小距离",
      "category": "编码理论",
      "direction": "maximize",
      "selection_reason": "仅二元[68,15]。先取得距离24矩阵；维数改变会使最小距离验证呈指数增长。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T066-C01",
          "parameters": {
            "n": 68,
            "k": 15,
            "q": 2
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 8,
          "primary_sources": [
            "https://www.codetables.de/BKLC/BKLC.php?k=15&n=68&q=2",
            "https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/bb895c1dee9ce0b39d6846e0aa984981_MIT6_451S05_FullLecNotes.pdf"
          ],
          "record_archive": "tasks/t066/records.json",
          "witness": "reports/witnesses/T066/T066-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开方法对照距离8，本地传统搜索距离19。公开距离24矩阵未取到。"
          ]
        }
      ]
    },
    {
      "task_id": "T067",
      "name": "二元码最大规模",
      "category": "编码理论",
      "direction": "maximize",
      "selection_reason": "仅A(17,6)。先取得258码字见证，不再增加尚未复现的纪录缺口。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T067-C01",
          "parameters": {
            "n": 17,
            "distance": 6
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 128,
          "primary_sources": [
            "https://aeb.win.tue.nl/codes/binary-1.html",
            "https://www.encyclopediaofmath.org/wiki/BCH_code"
          ],
          "record_archive": "tasks/t067/records.json",
          "witness": "reports/witnesses/T067/T067-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开方法对照128码字。公开258码字见证未取到。"
          ]
        }
      ]
    },
    {
      "task_id": "N001",
      "name": "奇环强积独立集",
      "category": "极值图与超图",
      "direction": "maximize",
      "selection_reason": "仅C7强积5次。367点构造来源清楚；其他幂可能已解决或大幅增加搜索成本。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "N001-C01",
          "parameters": {
            "q": 7,
            "power": 5
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 367,
          "primary_sources": [
            "https://arxiv.org/abs/1808.07438"
          ],
          "record_archive": "tasks/n001/records.json",
          "witness": "reports/witnesses/N001/N001-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        }
      ]
    },
    {
      "task_id": "T057",
      "name": "和差问题 I",
      "category": "加法组合与离散构造",
      "direction": "maximize",
      "selection_reason": "保持集合大小上限512和整数范围。任意改上限可能只转移同一个见证，未必增加结构差异。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T057-C01",
          "parameters": {
            "max_cardinality": 512,
            "integer_interval": [
              -1000000,
              1000000
            ]
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": "1.059793094547245377600002106026027810995517075670792756303442005379263930059059337409",
          "primary_sources": [
            "https://arxiv.org/abs/math/0608131"
          ],
          "record_archive": "tasks/t057/records.json",
          "witness": "reports/witnesses/T057/T057-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        }
      ]
    },
    {
      "task_id": "T073",
      "name": "低自相关二元序列（LABS）",
      "category": "序列与平坦多项式",
      "direction": "minimize",
      "selection_reason": "80、100、120项有可展开的公开序列，覆盖规模变化，精确验证为二次成本。",
      "configuration_count": 3,
      "configurations": [
        {
          "id": "T073-C01",
          "parameters": {
            "L": 100
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 578,
          "primary_sources": [
            "https://www2.chemistry.msu.edu/faculty/dantus/merit_factor_records.htm",
            "https://militzer.berkeley.edu/sequences.html"
          ],
          "record_archive": "tasks/t073/records.json",
          "witness": "reports/witnesses/T073/T073-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        },
        {
          "id": "T073-C02",
          "parameters": {
            "L": 80
          },
          "parameter_label": "L=80",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "The public table does not identify an individual discoverer for this row; attribution is unknown.",
          "source_reported_metric": "历史表能量E=352；不声称当前最佳。",
          "baseline_verified_objective": 352,
          "primary_sources": [
            "https://www2.chemistry.msu.edu/faculty/dantus/merit_factor_records.htm"
          ],
          "witness_source": "https://www2.chemistry.msu.edu/faculty/dantus/merit_factor_records.htm",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "来源将80标*，说明该记录未通过穷举确定最优。旧表的状态须在发布前更新。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "将游程编码展开为80个±1；精确重算79个非周期自相关及平方和。",
          "record_archive": "tasks/t073/records.json",
          "witness": "reports/witnesses/T073/T073-C02/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Dantus公开Merit Factor Records表给出游程编码。该行没有明确个人作者，保留unknown。"
        },
        {
          "id": "T073-C03",
          "parameters": {
            "L": 120
          },
          "parameter_label": "L=120",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "The public table does not identify an individual discoverer for this row; attribution is unknown.",
          "source_reported_metric": "历史表能量E=872；不声称当前最佳。",
          "baseline_verified_objective": 872,
          "primary_sources": [
            "https://www2.chemistry.msu.edu/faculty/dantus/merit_factor_records.htm"
          ],
          "witness_source": "https://www2.chemistry.msu.edu/faculty/dantus/merit_factor_records.htm",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "来源将120标*，未声称全局最优。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "精确重算119个非周期自相关及平方和。",
          "record_archive": "tasks/t073/records.json",
          "witness": "reports/witnesses/T073/T073-C03/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "同一公开表的120项序列游程编码；个人作者未明确时保留unknown。"
        }
      ]
    },
    {
      "task_id": "T079",
      "name": "自卷积不等式 AC1",
      "category": "极值分析",
      "direction": "minimize",
      "selection_reason": "仅208分段。加倍网格可以复制同一函数，不能据此虚增独立数学实例。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T079-C01",
          "parameters": {
            "steps": 208,
            "support": [
              "-1/4",
              "1/4"
            ],
            "nonnegative": true
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": "6280435861361744576/4160000022692211721",
          "primary_sources": [
            "https://arxiv.org/abs/0907.1379"
          ],
          "record_archive": "tasks/t079/records.json",
          "witness": "reports/witnesses/T079/T079-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        }
      ]
    },
    {
      "task_id": "T080",
      "name": "自卷积不等式 AC2",
      "category": "极值分析",
      "direction": "maximize",
      "selection_reason": "仅20分段。其他网格的文献成绩不可直接混用，先保持同参数可比。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T080-C01",
          "parameters": {
            "steps": 20,
            "support": [
              "-1/4",
              "1/4"
            ],
            "nonnegative": true
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": "108065664771600646574507764702/121527759800529249872686490775",
          "primary_sources": [
            "https://arxiv.org/pdf/0907.1379",
            "https://arxiv.org/abs/2604.19341"
          ],
          "record_archive": "tasks/t080/records.json",
          "witness": "reports/witnesses/T080/T080-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        }
      ]
    },
    {
      "task_id": "T081",
      "name": "允许负值的自卷积 AC3",
      "category": "极值分析",
      "direction": "minimize",
      "selection_reason": "仅208分段。先补强真正有符号的人类对照，不将不同网格或正峰值问题混入。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T081-C02",
          "parameters": {
            "steps": 208,
            "support": [
              "-1/4",
              "1/4"
            ],
            "signed_values_allowed": true,
            "integral": 1
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": "6280435861361744576/4160000022692211721",
          "primary_sources": [
            "https://arxiv.org/abs/0907.1379"
          ],
          "record_archive": "tasks/t081/records.json",
          "witness": "reports/witnesses/T081/T081-C02/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "非负208步人类构造转用于有符号类别。150步正峰值不能作为绝对峰值成绩。"
          ]
        }
      ]
    },
    {
      "task_id": "T082",
      "name": "Erdős 最小重叠",
      "category": "极值分析",
      "direction": "minimize",
      "selection_reason": "仅51分段。该人类构造与参数对应明确，优先保持严格全域验证。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T082-C01",
          "parameters": {
            "steps": 51,
            "support": "[0,2]",
            "range": "0≤f≤1",
            "integral": 1
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": "64757565083624785688821235069923/170000000000000000000000000000000",
          "primary_sources": [
            "https://arxiv.org/abs/1609.08000"
          ],
          "record_archive": "tasks/t082/records.json",
          "witness": "reports/witnesses/T082/T082-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        }
      ]
    },
    {
      "task_id": "T089",
      "name": "符号矩阵最大行列式",
      "category": "矩阵、格与代数极值",
      "direction": "maximize",
      "selection_reason": "仅29阶。许多其他阶数已达到已证上界；未逐项核实前不扩张。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T089-C01",
          "parameters": {
            "n": 29,
            "entries": "±1"
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 1188957517256767569920,
          "primary_sources": [
            "https://arxiv.org/abs/math/0304410",
            "https://maths-people.anu.edu.au/~brent/maxdet/order29/"
          ],
          "record_archive": "tasks/t089/records.json",
          "witness": "reports/witnesses/T089/T089-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        }
      ]
    },
    {
      "task_id": "T099",
      "name": "窄可容许素数元组",
      "category": "数论与算术构造",
      "direction": "minimize",
      "selection_reason": "仅343元组。有完整公开见证；新增规模须逐一核对是否已证明最优。",
      "configuration_count": 1,
      "configurations": [
        {
          "id": "T099-C01",
          "parameters": {
            "k": 343
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 2340,
          "primary_sources": [
            "https://mathbases.org/d/narrow-admissible-tuples",
            "https://math.mit.edu/~primegaps/tuples/admissible_343_2340.txt"
          ],
          "record_archive": "tasks/t099/records.json",
          "witness": "reports/witnesses/T099/T099-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        }
      ]
    },
    {
      "task_id": "T097",
      "name": "最短加法链",
      "category": "数论与算术构造",
      "direction": "minimize",
      "selection_reason": "三个明确大整数覆盖192、221、521位；公开链可精确逐步验证，避免已解小目标。",
      "configuration_count": 3,
      "configurations": [
        {
          "id": "T097-C01",
          "parameters": {
            "target": "2^192-2^64-3"
          },
          "role": "primary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_verified_objective": 202,
          "primary_sources": [
            "https://additionchains.com/LargeChains.html"
          ],
          "record_archive": "tasks/t097/records.json",
          "witness": "reports/witnesses/T097/T097-C01/human/solution.json",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。",
          "limitations": [
            "公开最好值限于已查来源。未声称已证明全局最优。"
          ]
        },
        {
          "id": "T097-C02",
          "parameters": {
            "target": "2^221-5"
          },
          "parameter_label": "目标2^221−5",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "公开人类构造，已复现并由Sol复核；见逐配置档案。",
          "source_reported_metric": "链长230，尚未独立重算。",
          "baseline_verified_objective": 230,
          "primary_sources": [
            "https://additionchains.com/LargeChains.html"
          ],
          "witness_source": "https://additionchains.com/LargeChains/M-221_field_inverse_230.txt",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "表中链长上界与small-step下界有差距，未给最优性证明。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "用大整数验证起点1、严格递增、每项为此前两项之和及准确终点。文本下载本次未成功。",
          "record_archive": "tasks/t097/records.json",
          "witness": "reports/witnesses/T097/T097-C02/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Clift的大指数加法链表：M-221目标，公开230步链；历史McLoughlin链231步单列。"
        },
        {
          "id": "T097-C03",
          "parameters": {
            "target": "2^521-3"
          },
          "parameter_label": "目标2^521−3",
          "role": "supplementary",
          "implementation_status": "accepted_by_sol",
          "baseline_evidence": "H1_witness_recomputed",
          "baseline_description": "公开人类构造，已复现并由Sol复核；见逐配置档案。",
          "source_reported_metric": "链长532，尚未独立重算。",
          "baseline_verified_objective": 532,
          "primary_sources": [
            "https://additionchains.com/LargeChains.html"
          ],
          "witness_source": "https://additionchains.com/LargeChains/P-521_field_inverse_532.txt",
          "source_checked_date": "2026-11-04",
          "open_status_evidence": "表列small-step下界10及所供链12，未给最优性证明。",
          "release_requirements": [
            "核对最新最优性证明与来源归属",
            "取得或重建人类构造并独立重算",
            "实现四类程序并按固定配置运行",
            "通过Sol逐配置验收后接入正式目录"
          ],
          "verification_plan": "验证533项大整数链及532次加法；不允许减法或模意义捷径。文本下载本次未成功。",
          "record_archive": "tasks/t097/records.json",
          "witness": "reports/witnesses/T097/T097-C03/human/solution.json",
          "implementation_review_date": "2026-11-04",
          "source_reported_metric_note": "Historical source claim is retained; the frozen baseline is baseline_verified_objective.",
          "selection_baseline_description": "Clift的大指数加法链表：P-521目标，公开532步链；历史Scott链另列。"
        }
      ]
    }
  ],
  "retired_configurations": [
    {
      "task_id": "T002",
      "id": "T002-C02",
      "parameters": {
        "n": 17
      },
      "parameter_label": "n=17",
      "role": "supplementary",
      "implementation_status": "retired_optimality_proof_reported",
      "baseline_evidence": "H2_source_located_not_recomputed_for_this_configuration",
      "baseline_description": "Bidwell 1998构造，基于Hämäläinen 1980布局；Friedman综述图12及当前实例页定位。",
      "source_reported_metric": "历史综述给s(17)<4.6756；当前页给更精细认证值。两者分开归档。",
      "baseline_verified_objective": null,
      "primary_sources": [
        "https://erich-friedman.github.io/papers/squares/squares.html",
        "https://squaremath.org/cases/17.html"
      ],
      "witness_source": "https://squaremath.org/cases/17.html",
      "source_checked_date": "2026-11-04",
      "open_status_evidence": "当前实例页明确标记open。全局最优性未建立。",
      "release_requirements": [
        "核对最新最优性证明与来源归属",
        "取得或重建人类构造并独立重算",
        "实现四类程序并按固定配置运行",
        "通过Sol逐配置验收后接入正式目录"
      ],
      "verification_plan": "保存坐标或重建布局；以有理数保守外扩或代数区间证明包含与分离。高次代数认证可能增加实现成本。",
      "retired_date": "2026-11-04",
      "retirement_reason": "原始Lean证明仓库现报告全源重建通过及全局最优性。按发现轨规则保守排除；本项目没有重放该完整证明。",
      "proof_source": "https://github.com/ofitzharding/sq17-lean"
    }
  ],
  "last_expansion_configuration_count": 14
}
```

</details>

### 来源纠正

<details>
<summary>来源纠正：完整记录</summary>

迁入来源：`source_corrections.json`；原文件SHA-256：`1ca99e88f7211d417bf264b3d37b135f4ca3866da1dd552a4e4f1e631975cd85`。

```json
[
  {
    "source_id": "geo-unit-squares-square",
    "removed": [
      "https://erich-friedman.github.io/papers/squares/squares.pdf"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "geo2-mrs-perkins",
    "removed": [
      "https://doi.org/10.1017/S0305004100038596"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "geo2-distinct-distances",
    "removed": [
      "https://annals.math.princeton.edu/2015/181-1/p07"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "no-three-in-line",
    "removed": [
      "https://mathworld.wolfram.com/No-Three-in-LineProblem.html"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "happy-ending",
    "removed": [
      "https://doi.org/10.1112/jlms/s1-10.1.14"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa09",
    "removed": [
      "https://doi.org/10.1016/0012-365X(90)90309-4"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa10",
    "removed": [
      "https://doi.org/10.1016/0012-365X(90)90309-4",
      "https://doi.org/10.3934/amc.2016.10.525"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa18",
    "removed": [
      "https://doi.org/10.1017/CBO9780511524919"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa22",
    "removed": [
      "https://doi.org/10.3934/dcds.2005.12.315",
      "https://doi.org/10.1109/TSP.2021.3078834"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa34",
    "removed": [
      "https://doi.org/10.1007/978-3-642-36206-1_6"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa38",
    "removed": [
      "https://doi.org/10.1007/978-3-642-36206-1_6"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa39",
    "removed": [
      "https://doi.org/10.4007/annals.2017.185.3.10"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa40",
    "removed": [
      "https://doi.org/10.4007/annals.2017.185.3.10"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa44",
    "removed": [
      "https://doi.org/10.1109/TSP.2021.3078834"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa46",
    "removed": [
      "https://arxiv.org/abs/1710.09008"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa48",
    "removed": [
      "https://doi.org/10.1007/BF02592041"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa52",
    "removed": [
      "https://doi.org/10.1007/s00454-003-2929-1",
      "https://doi.org/10.4007/annals.2017.185.3.10"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa54",
    "removed": [
      "https://doi.org/10.1007/s00023-005-0005-2"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa55",
    "removed": [
      "https://doi.org/10.1090/S0002-9939-1991-1050035-6",
      "https://doi.org/10.1016/S0022-0396(99)00027-4"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa57",
    "removed": [
      "https://doi.org/10.1007/s00208-005-0660-2",
      "https://doi.org/10.1007/978-3-0348-0105-5_10"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  },
  {
    "source_id": "aa61",
    "removed": [
      "https://doi.org/10.5555/3042573.3042658"
    ],
    "reason": "HTTP 404 or title mismatch in main review; raw agent notes remain unverified research history."
  }
]
```

</details>

### 来源访问核查

<details>
<summary>来源访问核查：完整记录</summary>

迁入来源：`source_access_audit.json`；原文件SHA-256：`1e535a4052d4de67270ce1fee98a6c9eb22098cf768e3749823c56df89bb9ca1`。

```json
{
  "note": "可访问性检查不代表文义、构造、作者或基线数字已验证；403/timeout不代表论文不存在。",
  "sources": [
    {
      "url": "https://annals.math.princeton.edu/2003/157-3/p07",
      "status": 200,
      "final_url": "https://annals.math.princeton.edu/2003/157-3/p07",
      "content_type": "text/html; charset=UTF-8",
      "title": "The Erdős–Szeméredi problem on sum set and product set | Annals of Mathematics",
      "meaning_verified": false
    },
    {
      "url": "https://annals.math.princeton.edu/2015/181-1/p07",
      "status": 200,
      "final_url": "https://annals.math.princeton.edu/2015/181-1/p07",
      "content_type": "text/html; charset=UTF-8",
      "title": "Small gaps between primes | Annals of Mathematics",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/0801.3987",
      "status": 200,
      "final_url": "https://arxiv.org/abs/0801.3987",
      "content_type": "text/html; charset=utf-8",
      "title": "[0801.3987] New Constructions of Permutation Arrays",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/0803.2336",
      "status": 200,
      "final_url": "https://arxiv.org/abs/0803.2336",
      "content_type": "text/html; charset=utf-8",
      "title": "[0803.2336] On the size of Kakeya sets in finite fields",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1103.4456",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1103.4456",
      "content_type": "text/html; charset=utf-8",
      "title": "[1103.4456] Finding largest small polygons with GloptiPoly",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1404.2183",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1404.2183",
      "content_type": "text/html; charset=utf-8",
      "title": "[1404.2183] Algorithms for determining integer complexity",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1407.2510",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1407.2510",
      "content_type": "text/html; charset=utf-8",
      "title": "[1407.2510] On the Erdos Discrepancy Problem",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1503.06639",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1503.06639",
      "content_type": "text/html; charset=utf-8",
      "title": "[1503.06639] A finite version of the Kakeya problem",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1509.05363",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1509.05363",
      "content_type": "text/html; charset=utf-8",
      "title": "[1509.05363] The Erdos discrepancy problem",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1512.02475",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1512.02475",
      "content_type": "text/html; charset=utf-8",
      "title": "[1512.02475] Low Autocorrelation Binary Sequences",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1601.02864",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1601.02864",
      "content_type": "text/html; charset=utf-8",
      "title": "[1601.02864] Tables of subspace codes",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1604.08657",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1604.08657",
      "content_type": "text/html; charset=utf-8",
      "title": "[1604.08657] On the Erdos-Szekeres convex polygon problem",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1605.09223",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1605.09223",
      "content_type": "text/html; charset=utf-8",
      "title": "[1605.09223] On large subsets of $F_q^n$ with no three-term arithmetic progression",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1705.09673",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1710.09008",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1710.09008",
      "content_type": "text/html; charset=utf-8",
      "title": "[1710.09008] The Shape of an Image: A Study of Mapper on Images",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1802.06415",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1802.06415",
      "content_type": "text/html; charset=utf-8",
      "title": "[1802.06415] Solving Large-Scale Minimum-Weight Triangulation Instances to Provable Optimality",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1804.08252",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1804.08252",
      "content_type": "text/html; charset=utf-8",
      "title": "[1804.08252] Constructing Permutation Arrays using Partition and Extension",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/1907.09464",
      "status": 200,
      "final_url": "https://arxiv.org/abs/1907.09464",
      "content_type": "text/html; charset=utf-8",
      "title": "[1907.09464] Flat Littlewood Polynomials Exist",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2005.09352",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2005.09352",
      "content_type": "text/html; charset=utf-8",
      "title": "[2005.09352] Single-Deletion Single-Substitution Correcting Codes",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2012.07939",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2012.07939",
      "content_type": "text/html; charset=utf-8",
      "title": "[2012.07939] An integer programming formulation using convex polygons for the convex partition problem",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2104.12711",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2104.12711",
      "content_type": "text/html; charset=utf-8",
      "title": "[2104.12711] The Bose-Chowla argument for Sidon sets",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2201.05704",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2201.05704",
      "content_type": "text/html; charset=utf-8",
      "title": "[2201.05704] Erdős' minimum overlap problem",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2202.05507",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2202.05507",
      "content_type": "text/html; charset=utf-8",
      "title": "[2202.05507] Exact values for unbalanced Zarankiewicz numbers",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2203.02283",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2203.02283",
      "content_type": "text/html; charset=utf-8",
      "title": "[2203.02283] An attack on Zarankiewicz's problem through SAT solving",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2209.01447",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2209.01447",
      "content_type": "text/html; charset=utf-8",
      "title": "[2209.01447] The extensible No-Three-In-Line problem",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2303.07007",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2303.07007",
      "content_type": "text/html; charset=utf-8",
      "title": "[2303.07007] Minimum Coverage by Convex Polygons: The CG:SHOP Challenge 2023",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2403.00737",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2403.00737",
      "content_type": "text/html; charset=utf-8",
      "title": "[2403.00737] Happy Ending: An Empty Hexagon in Every Set of 30 Points",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2403.16203",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2403.16203",
      "content_type": "text/html; charset=utf-8",
      "title": "[2403.16203] Maximum Polygon Packing: The CG:SHOP Challenge 2024",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2403.17370",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2403.17370",
      "content_type": "text/html; charset=utf-8",
      "title": "[2403.17370] Formal Verification of the Empty Hexagon Number",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2403.20123",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2403.20123",
      "content_type": "text/html; charset=utf-8",
      "title": "[2403.20123] Shadoks Approach to Knapsack Polygonal Packing",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2409.15709",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2409.15709",
      "content_type": "text/html; charset=utf-8",
      "title": "[2409.15709] $R(5,5)\\le 46$",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2411.17448",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2411.17448",
      "content_type": "text/html; charset=utf-8",
      "title": "[2411.17448] New bounds for the Furstenberg-Sárközy theorem",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2412.11914",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2412.11914",
      "content_type": "text/html; charset=utf-8",
      "title": "[2412.11914] The Erdős unit distance problem for small point sets",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2502.18189",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2502.18189",
      "content_type": "text/html; charset=utf-8",
      "title": "[2502.18189] Exact Algorithms for Minimum Dilation Triangulation",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2504.04412",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2504.04412",
      "content_type": "text/html; charset=utf-8",
      "title": "[2504.04412] Minimum Non-Obtuse Triangulations: The CG:SHOP Challenge 2025",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2511.02864",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2511.02864",
      "content_type": "text/html; charset=utf-8",
      "title": "[2511.02864] Mathematical exploration and discovery at scale",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2511.07247",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2511.07247",
      "content_type": "text/html; charset=utf-8",
      "title": "[2511.07247] New small regular graphs of given girth: the cage problem and beyond",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2604.19341",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2604.19341",
      "content_type": "text/html; charset=utf-8",
      "title": "[2604.19341] Structured Scaling of AI Discovery Across Diverse Scientific Domains",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2605.07179",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2605.07179",
      "content_type": "text/html; charset=utf-8",
      "title": "[2605.07179] The saturation number of $K^s_t$",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/2608.04392",
      "status": 200,
      "final_url": "https://arxiv.org/abs/2608.04392",
      "content_type": "text/html; charset=utf-8",
      "title": "[2608.04392] The maximum volume polytope with nine vertices inscribed in the sphere",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/cs/0009023",
      "status": 200,
      "final_url": "https://arxiv.org/abs/cs/0009023",
      "content_type": "text/html; charset=utf-8",
      "title": "[cs/0009023] The Rectilinear Crossing Number of K_10 is 62",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/cs/0601002",
      "status": 200,
      "final_url": "https://arxiv.org/abs/cs/0601002",
      "content_type": "text/html; charset=utf-8",
      "title": "[cs/0601002] Minimum-weight triangulation is NP-hard",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/math/0101166",
      "status": 200,
      "final_url": "https://arxiv.org/abs/math/0101166",
      "content_type": "text/html; charset=utf-8",
      "title": "[math/0101166] Small polynomials with integer coefficients",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/math/0304410",
      "status": 200,
      "final_url": "https://arxiv.org/abs/math/0304410",
      "content_type": "text/html; charset=utf-8",
      "title": "[math/0304410] New lower bounds for the maximal determinant problem",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/abs/math/0402285",
      "status": 200,
      "final_url": "https://arxiv.org/abs/math/0402285",
      "content_type": "text/html; charset=utf-8",
      "title": "[math/0402285] The Erdős-Szemerédi problem on sum set and product set",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/html/2511.02864v1#S6.SS2",
      "status": 200,
      "final_url": "https://arxiv.org/html/2511.02864v1#S6.SS2",
      "content_type": "text/html; charset=utf-8",
      "title": "Mathematical exploration and discovery at scale",
      "meaning_verified": false
    },
    {
      "url": "https://arxiv.org/html/2511.02864v1#S6.SS25",
      "status": 200,
      "final_url": "https://arxiv.org/html/2511.02864v1#S6.SS25",
      "content_type": "text/html; charset=utf-8",
      "title": "Mathematical exploration and discovery at scale",
      "meaning_verified": false
    },
    {
      "url": "https://barc.ku.dk/news/bachelor-project-at-barc-wins-computational-geometry-challenge/",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://cgshop.ibr.cs.tu-bs.de/",
      "status": 200,
      "final_url": "https://cgshop.ibr.cs.tu-bs.de/",
      "content_type": "text/html; charset=utf-8",
      "title": "CG:SHOP SoCG Competition",
      "meaning_verified": false
    },
    {
      "url": "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2019/",
      "status": 200,
      "final_url": "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2019/",
      "content_type": "text/html; charset=utf-8",
      "title": "CG:SHOP SoCG Competition",
      "meaning_verified": false
    },
    {
      "url": "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2022/",
      "status": 200,
      "final_url": "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2022/",
      "content_type": "text/html; charset=utf-8",
      "title": "CG:SHOP SoCG Competition",
      "meaning_verified": false
    },
    {
      "url": "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2023/",
      "status": 200,
      "final_url": "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2023/",
      "content_type": "text/html; charset=utf-8",
      "title": "CG:SHOP SoCG Competition",
      "meaning_verified": false
    },
    {
      "url": "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2024/",
      "status": 200,
      "final_url": "https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2024/",
      "content_type": "text/html; charset=utf-8",
      "title": "CG:SHOP SoCG Competition",
      "meaning_verified": false
    },
    {
      "url": "https://citeseerx.ist.psu.edu/document?doi=40b403e751d8807c5609b9eb571711077489bf45&repid=rep1&type=pdf",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://codetables.de/",
      "status": 200,
      "final_url": "https://codetables.de/",
      "content_type": "text/html",
      "title": "CodeTables.de",
      "meaning_verified": false
    },
    {
      "url": "https://cohn.mit.edu/sloane/",
      "status": 200,
      "final_url": "https://cohn.mit.edu/sloane/",
      "content_type": "text/html; charset=UTF-8",
      "title": "Sloane’s tables of point configurations on spheres – Henry Cohn",
      "meaning_verified": false
    },
    {
      "url": "https://cohn.mit.edu/spherical-codes/",
      "status": 200,
      "final_url": "https://cohn.mit.edu/spherical-codes/",
      "content_type": "text/html; charset=UTF-8",
      "title": "Spherical codes – Henry Cohn",
      "meaning_verified": false
    },
    {
      "url": "https://cs.uwaterloo.ca/~shallit/DC2015/iraids2.pdf",
      "status": 200,
      "final_url": "https://cs.uwaterloo.ca/~shallit/DC2015/iraids2.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://cs.uwaterloo.ca/~vanbeek/Publications/sillito.pdf",
      "status": 200,
      "final_url": "https://cs.uwaterloo.ca/~vanbeek/Publications/sillito.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob006/",
      "status": 200,
      "final_url": "https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob006/",
      "content_type": "text/html; charset=utf-8",
      "title": "006: Golomb rulers",
      "meaning_verified": false
    },
    {
      "url": "https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob010/",
      "status": 200,
      "final_url": "https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob010/",
      "content_type": "text/html; charset=utf-8",
      "title": "010: Social Golfer Problem",
      "meaning_verified": false
    },
    {
      "url": "https://csrc.nist.gov/Projects/Automated-Combinatorial-Testing-for-Software/Covering-Array-Library",
      "status": 200,
      "final_url": "https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/acts-library/covering-array-library",
      "content_type": "text/html; charset=utf-8",
      "title": "Combinatorial Methods for Trust and Assurance | CSRC",
      "meaning_verified": false
    },
    {
      "url": "https://distributed.net/ogr/",
      "status": 200,
      "final_url": "https://www.distributed.net/OGR",
      "content_type": "text/html",
      "title": "distributed.net: Project OGR",
      "meaning_verified": false
    },
    {
      "url": "https://dmgordon.org/ljcr/",
      "status": 200,
      "final_url": "https://dmgordon.org/ljcr/",
      "content_type": "text/html; charset=utf-8",
      "title": "The La Jolla Combinatorics Repository - LJCR",
      "meaning_verified": false
    },
    {
      "url": "https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html",
      "status": 200,
      "final_url": "https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Best Known Linear Codes — Magma Handbook",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/978-3-0348-0105-5_10",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/978-3-642-36206-1_3",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/978-3-642-36206-1_6",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/BF00170806",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/BF02454169",
      "status": 200,
      "final_url": "https://link.springer.com/article/10.1007/BF02454169?error=cookies_not_supported&code=ff47d33b-241f-46f8-ae24-15a57c1a8bc6",
      "content_type": "text/html; charset=utf-8",
      "title": "Difference sets without squares | Periodica Mathematica Hungarica | Springer Nature Link",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/BF02566968",
      "status": 200,
      "final_url": "https://link.springer.com/article/10.1007/BF02566968?error=cookies_not_supported&code=520f628a-69bd-4732-812d-f20760cd216b",
      "content_type": "text/html; charset=utf-8",
      "title": "Theorems in the additive theory of numbers | Commentarii Mathematici Helvetici | Springer Nature Link",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/BF02574074",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/BF02592041",
      "status": 200,
      "final_url": "https://link.springer.com/article/10.1007/BF02592041?error=cookies_not_supported&code=e59e4ac7-223a-4ea9-87a9-1b24b51aba9e",
      "content_type": "text/html; charset=utf-8",
      "title": "Approximation of fractional-order integrals by algebraic polynomials. II | Ukrainian Mathematical Journal | Springer Nature Link",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/BF02711518",
      "status": 200,
      "final_url": "https://link.springer.com/article/10.1007/BF02711518?error=cookies_not_supported&code=c608f9ed-5faa-41e2-8a80-7ece0e179681",
      "content_type": "text/html; charset=utf-8",
      "title": "McLaren’s improved snub cube and other new spherical designs in three dimensions | Discrete & Computational Geometry | Springer Nature Link",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/s00023-004-0186-8",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/s00023-005-0005-2",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/s00208-005-0660-2",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1007/s00454-003-2929-1",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1016/0012-365X(90)90309-4",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1016/S0022-0396(99)00027-4",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1016/j.cor.2004.11.002",
      "status": 200,
      "final_url": "https://linkinghub.elsevier.com/retrieve/pii/S0305054804003028",
      "content_type": "text/html;charset=UTF-8",
      "title": "Redirecting",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1017/CBO9780511524919",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1017/S0305004100038596",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1073/pnas.32.12.331",
      "error": "HTTP Error 403: Forbidden",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1080/00029890.2005.11920180",
      "error": "HTTP Error 403: Forbidden",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1090/S0002-9939-1991-1050035-6",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1109/ICASSP.1990.115796",
      "status": 202,
      "final_url": "https://ieeexplore.ieee.org/document/115796/",
      "content_type": "text/html; charset=UTF-8",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1109/JRPROC.1949.232969",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1109/TIT.1965.1053768",
      "status": 202,
      "final_url": "https://ieeexplore.ieee.org/document/1053768/",
      "content_type": "text/html; charset=UTF-8",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1109/TSP.2021.3078834",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1112/jlms/s1-10.1.14",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1112/jlms/s1-44.1.131",
      "error": "HTTP Error 403: Forbidden",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1112/jlms/s1-8.4.242",
      "error": "HTTP Error 403: Forbidden",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.1145/3504000",
      "error": "HTTP Error 403: Forbidden",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.17632/d75dzbjd4k.3",
      "status": 200,
      "final_url": "https://data.mendeley.com/datasets/d75dzbjd4k/3",
      "content_type": "text/html; charset=utf-8",
      "title": "Table of Large Degree/Diameter Graphs - Mendeley Data",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.3792/pja/1195520891",
      "status": 200,
      "final_url": "https://projecteuclid.org/journals/proceedings-of-the-japan-academy-series-a-mathematical-sciences/volume-45/issue-1/Maximal-sum-free-sets-of-elements-of-finite-groups/10.3792/pja/1195520891.full",
      "content_type": "text/html",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.3934/amc.2016.10.525",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.3934/dcds.2005.12.315",
      "status": 200,
      "final_url": "https://www.aimsciences.org//article/doi/10.3934/dcds.2005.12.315",
      "content_type": "text/html;charset=UTF-8",
      "title": "Strong instability of standing waves for nonlinear Klein-Gordon equations",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.4007/annals.2017.185.1.8",
      "status": 200,
      "final_url": "https://annals.math.princeton.edu/2017/185-1/p08",
      "content_type": "text/html; charset=UTF-8",
      "title": "On large subsets of $\\mathbb{F}_q^n$ with no  three-term arithmetic progression | Annals of Mathematics",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.4007/annals.2017.185.3.10",
      "status": 200,
      "final_url": "https://annals.math.princeton.edu/2017/185-3/p10",
      "content_type": "text/html; charset=UTF-8",
      "title": "Monochromatic sums and products in $\\mathbb N$ | Annals of Mathematics",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.4007/annals.2017.185.3.8",
      "status": 200,
      "final_url": "https://annals.math.princeton.edu/2017/185-3/p08",
      "content_type": "text/html; charset=UTF-8",
      "title": "The sphere packing problem in dimension $24$ | Annals of Mathematics",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.4153/CJM-1949-009-2",
      "status": 200,
      "final_url": "https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/nonexistence-of-certain-finite-projective-planes/2A2E0D91C8E872232A01C7519F14D705",
      "content_type": "text/html; charset=utf-8",
      "title": "The Nonexistence of Certain Finite Projective Planes | Canadian Journal of Mathematics | Cambridge Core",
      "meaning_verified": false
    },
    {
      "url": "https://doi.org/10.5555/3042573.3042658",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2018.44",
      "status": 200,
      "final_url": "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2018.44",
      "content_type": "text/html; charset=utf-8",
      "title": "Solving Large-Scale Minimum-Weight Triangulation Instances to Provable Optimality",
      "meaning_verified": false
    },
    {
      "url": "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.48",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://erich-friedman.github.io/packing/",
      "status": 200,
      "final_url": "https://erich-friedman.github.io/packing/",
      "content_type": "text/html; charset=utf-8",
      "title": "Erich's Packing Center",
      "meaning_verified": false
    },
    {
      "url": "https://erich-friedman.github.io/packing/circovcir/",
      "status": 200,
      "final_url": "https://erich-friedman.github.io/packing/circovcir/",
      "content_type": "text/html; charset=utf-8",
      "title": "Circles Covering Circles",
      "meaning_verified": false
    },
    {
      "url": "https://erich-friedman.github.io/packing/maxmin/",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://erich-friedman.github.io/packing/triinsqu/",
      "status": 200,
      "final_url": "https://erich-friedman.github.io/packing/triinsqu/",
      "content_type": "text/html; charset=utf-8",
      "title": "Triangles in Squares",
      "meaning_verified": false
    },
    {
      "url": "https://erich-friedman.github.io/papers/covering.pdf",
      "status": 200,
      "final_url": "https://erich-friedman.github.io/papers/covering.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://erich-friedman.github.io/papers/covering/covering.html",
      "status": 200,
      "final_url": "https://erich-friedman.github.io/papers/covering/covering.html",
      "content_type": "text/html; charset=utf-8",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://erich-friedman.github.io/papers/squares/squares.html",
      "status": 200,
      "final_url": "https://erich-friedman.github.io/papers/squares/squares.html",
      "content_type": "text/html; charset=utf-8",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://erich-friedman.github.io/papers/squares/squares.pdf",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://github.com/teorth/erdos-guy-selfridge",
      "status": 200,
      "final_url": "https://github.com/teorth/erdos-guy-selfridge",
      "content_type": "text/html; charset=utf-8",
      "title": "GitHub - teorth/erdos-guy-selfridge: Project to verify the Guy-Selfridge conjectures · GitHub",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/11.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/11.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/13.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/13.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/15.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/15.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/19.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/19.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/20.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/20.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/21.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/21.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/22.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/22.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/38.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/38.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/42.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/42.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/43.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/43.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/44.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/44.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/46.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/46.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/47.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/47.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/55.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/55.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/57.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/57.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/6.html",
      "status": 200,
      "final_url": "https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/6.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Math Problem Template",
      "meaning_verified": false
    },
    {
      "url": "https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf",
      "status": 200,
      "final_url": "https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://link.springer.com/article/10.1007/s00454-023-00556-3",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://ljcr.dmgordon.org/cover.html",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://math.mit.edu/~drew/GuySelfridge.m",
      "status": 200,
      "final_url": "https://math.mit.edu/~drew/GuySelfridge.m",
      "content_type": "application/vnd.wolfram.mathematica.package",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://math.mit.edu/~drew/PrimeGapsOberwolfach3.pdf",
      "status": 200,
      "final_url": "https://math.mit.edu/~drew/PrimeGapsOberwolfach3.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://math.mit.edu/~primegaps/",
      "status": 200,
      "final_url": "https://math.mit.edu/~primegaps/",
      "content_type": "text/html; charset=UTF-8",
      "title": "Narrow admissible tuples",
      "meaning_verified": false
    },
    {
      "url": "https://math.nist.gov/coveringarrays/coveringarray.html",
      "status": 200,
      "final_url": "https://math.nist.gov/coveringarrays/coveringarray.html",
      "content_type": "text/html",
      "title": "NIST Covering Array Tables - What is a covering array?",
      "meaning_verified": false
    },
    {
      "url": "https://math.okstate.edu/people/igor/intcheb.pdf",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://math.tejstead.com/heilbronn/",
      "status": 200,
      "final_url": "https://math.tejstead.com/heilbronn/",
      "content_type": "text/html; charset=utf-8",
      "title": "The Heilbronn Problem",
      "meaning_verified": false
    },
    {
      "url": "https://math.tejstead.com/heilbronn/convex/",
      "status": 200,
      "final_url": "https://math.tejstead.com/heilbronn/convex/",
      "content_type": "text/html; charset=utf-8",
      "title": "Heilbronn — The Heilbronn Problem for Convex Regions",
      "meaning_verified": false
    },
    {
      "url": "https://maths-people.anu.edu.au/~brent/maxdet/order29/",
      "status": 200,
      "final_url": "https://maths-people.anu.edu.au/~brent/maxdet/order29/",
      "content_type": "text/html",
      "title": "Order 29",
      "meaning_verified": false
    },
    {
      "url": "https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/ExactHypergraphTuranT3n4.html",
      "error": "<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://mathworld.wolfram.com/ErdosDistinctDistancesProblem.html",
      "status": 200,
      "final_url": "https://mathworld.wolfram.com/ErdosDistinctDistancesProblem.html",
      "content_type": "text/html; charset=UTF-8",
      "title": "Erdős Distinct Distances Problem -- from Wolfram MathWorld",
      "meaning_verified": false
    },
    {
      "url": "https://mathworld.wolfram.com/MrsPerkinssQuilt.html",
      "status": 200,
      "final_url": "https://mathworld.wolfram.com/MrsPerkinssQuilt.html",
      "content_type": "text/html; charset=UTF-8",
      "title": "Mrs. Perkins's Quilt -- from Wolfram MathWorld",
      "meaning_verified": false
    },
    {
      "url": "https://mathworld.wolfram.com/No-Three-in-LineProblem.html",
      "error": "HTTP Error 404: Not Found",
      "meaning_verified": false
    },
    {
      "url": "https://militzer.berkeley.edu/sequences.html",
      "status": 200,
      "final_url": "https://militzer.berkeley.edu/sequences.html",
      "content_type": "text/html",
      "title": "Low autocorrelated binary sequences",
      "meaning_verified": false
    },
    {
      "url": "https://neilsloane.com/doc/dijen.pdf",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://neilsloane.com/oadir/index.html",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://neilsloane.com/packings/",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://neilsloane.com/sphdesigns/",
      "status": 200,
      "final_url": "https://neilsloane.com/sphdesigns/",
      "content_type": "text/html",
      "title": "Spherical Designs",
      "meaning_verified": false
    },
    {
      "url": "https://oeis.org/A003035",
      "status": 200,
      "final_url": "https://oeis.org/A003035",
      "content_type": "text/html; charset=utf-8",
      "title": "A003035 - OEIS",
      "meaning_verified": false
    },
    {
      "url": "https://oeis.org/A034258",
      "status": 200,
      "final_url": "https://oeis.org/A034258",
      "content_type": "text/html; charset=utf-8",
      "title": "A034258 - OEIS",
      "meaning_verified": false
    },
    {
      "url": "https://ojs.aaai.org/index.php/AAAI/article/download/12209/12068",
      "status": 200,
      "final_url": "https://ojs.aaai.org/index.php/AAAI/article/download/12209/12068",
      "content_type": "text/html; charset=utf-8",
      "title": "Making sure you're not a bot!",
      "meaning_verified": false
    },
    {
      "url": "https://optimization-online.org/wp-content/uploads/2020/09/8019.pdf",
      "status": 200,
      "final_url": "https://optimization-online.org/wp-content/uploads/2020/09/8019.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://packomania.com/",
      "status": 200,
      "final_url": "https://packomania.com/",
      "content_type": "text/html",
      "title": "Packomania (52C17)",
      "meaning_verified": false
    },
    {
      "url": "https://packomania.com/csq/",
      "status": 200,
      "final_url": "https://packomania.com/csq/",
      "content_type": "text/html",
      "title": "The best known packings of equal circles in a square",
      "meaning_verified": false
    },
    {
      "url": "https://pageperso.lis-lab.fr/guilherme.fonseca/CGSHOP22slides.pdf",
      "status": 200,
      "final_url": "https://pageperso.lis-lab.fr/guilherme.fonseca/CGSHOP22slides.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://people.cs.uchicago.edu/~razborov/files/triangles.pdf",
      "error": "<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://people.maths.ox.ac.uk/keevash/papers/turan-survey.pdf",
      "status": 200,
      "final_url": "https://people.maths.ox.ac.uk/keevash/papers/turan-survey.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://personal.math.ubc.ca/~gerg/papers/downloads/MSHMSTD.pdf",
      "status": 200,
      "final_url": "https://personal.math.ubc.ca/~gerg/papers/downloads/MSHMSTD.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://polyominoes.org/data/5P",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://proceedings.mlr.press/v23/recht12.html",
      "status": 200,
      "final_url": "https://proceedings.mlr.press/v23/recht12.html",
      "content_type": "text/html; charset=utf-8",
      "title": "Toward a Noncommutative Arithmetic-geometric Mean Inequality: Conjectures, Case-studies, and Consequences",
      "meaning_verified": false
    },
    {
      "url": "https://research.ibm.com/publications/some-new-optimum-golomb-rulers",
      "status": 200,
      "final_url": "https://research.ibm.com/publications/some-new-optimum-golomb-rulers",
      "content_type": "text/html; charset=utf-8",
      "title": "Some New Optimum Golomb Rulers for IEEE Trans. Inf. Theory - IBM Research",
      "meaning_verified": false
    },
    {
      "url": "https://sicherman.net/mikereid/p5_rect.html",
      "status": 200,
      "final_url": "https://sicherman.net/mikereid/p5_rect.html",
      "content_type": "text/html",
      "title": "Primes of the  P  pentomino",
      "meaning_verified": false
    },
    {
      "url": "https://subspacecodes.uni-bayreuth.de/",
      "error": "<urlopen error EOF occurred in violation of protocol (_ssl.c:1131)>",
      "meaning_verified": false
    },
    {
      "url": "https://users.cecs.anu.edu.au/~bdm/data/extremal.html",
      "status": 200,
      "final_url": "https://users.cecs.anu.edu.au/~bdm/data/extremal.html",
      "content_type": "text/html",
      "title": "Combinatorial Data",
      "meaning_verified": false
    },
    {
      "url": "https://users.cecs.anu.edu.au/~bdm/data/ramsey.html",
      "status": 200,
      "final_url": "https://users.cecs.anu.edu.au/~bdm/data/ramsey.html",
      "content_type": "text/html",
      "title": "Combinatorial Data",
      "meaning_verified": false
    },
    {
      "url": "https://webhost.services.iit.cnr.it/staff/giovanni.resta/ac/",
      "status": 200,
      "final_url": "https://webhost.services.iit.cnr.it/staff/giovanni.resta/ac/",
      "content_type": "text/html",
      "title": "Addition Chains' Database",
      "meaning_verified": false
    },
    {
      "url": "https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/index.html",
      "status": 200,
      "final_url": "https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/index.html",
      "content_type": "text/html",
      "title": "Riesz energy database",
      "meaning_verified": false
    },
    {
      "url": "https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html",
      "status": 200,
      "final_url": "https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html",
      "content_type": "text/html",
      "title": "Riesz energy database: s = 1",
      "meaning_verified": false
    },
    {
      "url": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0EC7876789232266D60439A4C00D86D9/S144618110000300Xa.pdf/computer_solution_to_the_17point_erdosszekeres_problem.pdf",
      "status": 200,
      "final_url": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0EC7876789232266D60439A4C00D86D9/S144618110000300Xa.pdf/computer_solution_to_the_17point_erdosszekeres_problem.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS16",
      "status": 200,
      "final_url": "https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS16",
      "content_type": "text/html; charset=utf-8",
      "title": "Dynamic Cage Survey\n\t\t\t\t\t\t\t| The Electronic Journal of Combinatorics",
      "meaning_verified": false
    },
    {
      "url": "https://www.combinatorics.org/ojs/index.php/eljc/article/view/v18i1p64",
      "status": 200,
      "final_url": "https://www.combinatorics.org/ojs/index.php/eljc/article/view/v18i1p64",
      "content_type": "text/html; charset=utf-8",
      "title": "Lower Bounds on van der Waerden Numbers: Randomized- and Deterministic-Constructive\n\t\t\t\t\t\t\t| The Electronic Journal of Combinatorics",
      "meaning_verified": false
    },
    {
      "url": "https://www.crossingnumbers.org/projects/crossingconstants/rectilinear.php",
      "status": 200,
      "final_url": "https://www.crossingnumbers.org/projects/crossingconstants/rectilinear.php",
      "content_type": "text/html; charset=UTF-8",
      "title": "Crossing Numbers",
      "meaning_verified": false
    },
    {
      "url": "https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf",
      "status": 200,
      "final_url": "https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://www.cs.utexas.edu/~marijn/Schur/",
      "status": 200,
      "final_url": "https://www.cs.utexas.edu/~marijn/Schur/",
      "content_type": "text/html",
      "title": "Schur Number Five",
      "meaning_verified": false
    },
    {
      "url": "https://www.cs.utexas.edu/~marijn/publications/waerden.pdf",
      "status": 200,
      "final_url": "https://www.cs.utexas.edu/~marijn/publications/waerden.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://www.csplib.org/Problems/prob010/",
      "status": 200,
      "final_url": "https://www.csplib.org/Problems/prob010/",
      "content_type": "text/html; charset=utf-8",
      "title": "010: Social Golfers Problem",
      "meaning_verified": false
    },
    {
      "url": "https://www.csun.edu/~ctoth/Handbook/chap14.pdf",
      "status": 200,
      "final_url": "https://www.csun.edu/~ctoth/Handbook/chap14.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://www.csun.edu/~sf70713/publications/survey.pdf",
      "status": 200,
      "final_url": "https://www.csun.edu/~sf70713/publications/survey.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Poly/",
      "status": 200,
      "final_url": "https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Poly/",
      "content_type": "text/html",
      "title": "Area-Optimal Simple Polygonization Problems - Benchmark Instances",
      "meaning_verified": false
    },
    {
      "url": "https://www.ic.unicamp.br/~cid/Problem-instances/Dilation/MDTP/index.html",
      "status": 200,
      "final_url": "https://www.ic.unicamp.br/~cid/Problem-instances/Dilation/MDTP/index.html",
      "content_type": "text/html",
      "title": "IC - UNICAMP - Dilation Instances Library",
      "meaning_verified": false
    },
    {
      "url": "https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/BGKRSW96/bgkrsw96.pdf",
      "status": 200,
      "final_url": "https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/BGKRSW96/bgkrsw96.pdf",
      "content_type": "application/pdf",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://www.mcs.anl.gov/~more/cops/bcops/polygon.html",
      "error": "HTTP Error 403: Forbidden",
      "meaning_verified": false
    },
    {
      "url": "https://www.squaring.net/downloads/downloads.html~",
      "status": 200,
      "final_url": "https://www.squaring.net/downloads/downloads.html~",
      "content_type": "",
      "title": null,
      "meaning_verified": false
    },
    {
      "url": "https://www.squaring.net/sq/ss/quilts/mrs-perkins-quilts.html",
      "status": 200,
      "final_url": "https://www.squaring.net/sq/ss/quilts/mrs-perkins-quilts.html",
      "content_type": "text/html",
      "title": "Mrs Perkins's Quilt",
      "meaning_verified": false
    },
    {
      "url": "https://www.squaring.net/sq/ss/spss/o21/spsso21.html",
      "status": 200,
      "final_url": "https://www.squaring.net/sq/ss/spss/o21/spsso21.html",
      "content_type": "text/html",
      "title": "Simple Perfect Squared Squares Order 21",
      "meaning_verified": false
    },
    {
      "url": "https://www.squaring.net/sq/ss/spss/o55/spsso55.html",
      "status": 200,
      "final_url": "https://www.squaring.net/sq/ss/spss/o55/spsso55.html",
      "content_type": "text/html",
      "title": "Simple Perfect Squared Squares Order 55",
      "meaning_verified": false
    },
    {
      "url": "https://www.win.tue.nl/~aeb/codes/",
      "status": 200,
      "final_url": "https://aeb.win.tue.nl/codes/",
      "content_type": "text/html;charset=ISO-8859-1",
      "title": "Index of /codes",
      "meaning_verified": false
    },
    {
      "url": "https://wwwhomes.uni-bielefeld.de/achim/addition_chain.html",
      "status": 200,
      "final_url": "https://wwwhomes.uni-bielefeld.de/achim/addition_chain.html",
      "content_type": "text/html",
      "title": "Shortest Addition Chains",
      "meaning_verified": false
    }
  ]
}
```

</details>
