> 2026-11-04 实现修订：T009 的15点配置已有最优性证明，已换成16点 T009-C02。任务数与首批配置数不变。正式参数与复现状态见任务包。

# 数学构造 benchmark：逐项核查结果

日期：2026-11-03。Luna 分方向核查，主代理复核配置、分数方向和近期已解结果。

候选池为 **12 类、110 个任务家族**。其中 **91 个家族已确认适合选型**，17 个待补证，2 个目前只核到了须排除的配置。没有把候选池计作100个已就绪任务。

共有 115 条配置核查记录。其中 94 条通过选型筛查，11 条保留了独立重算的基线见证。配置记录和任务家族分开计数。

## 选型标准

公开可验证的人类构造基线、明确单标量、所选配置没有已知最优性证明。历史基线可用；独立重算与选型确认分开。

最小化任务统一排名分数为 −J，最大化任务为 J。无效构造不参与有效解排名。理论下界不能作为最小化任务的可行构造分数。

## 首批 20 个任务

建议从 10 类、20 个任务、21 个配置开始。变半径圆装填包含26和32两个配置，以对应系统论文中的两组实例。AC3首批使用208步转移基线；150步旧见证单独保留。

|任务|配置|人类基线|选择理由|
|---|---|---|---|
|T001 等圆装入正方形|n=26, unit square|Nurmela–Östergård circle packing, common radius 0.096362339010|公开坐标与传统研究历史清楚；用两两距离和边界距离验证。|
|T002 单位正方形装入正方形|n=26 unit squares in a square|Friedman unit-square packing, side (7+3√2)/2 = 5.62132034355964|用户重点方向；26 个方块有开放界与具名人类构造。|
|T005 变半径圆装填|n=26 variable-radius circles in unit square|0.096362339010 radius for each of 26 equal circles; total sum 2.505420814260, a feasible human baseline.|覆盖 SimpleTES 与 DREAM-RSI；先比较人类可行构造，再冻结现代纪录。|
|T005 变半径圆装填|{"n": 32, "container": "unit square", "radii": "variable; human baseline uses equal radii"}|2.811461026816|覆盖 SimpleTES 与 DREAM-RSI；先比较人类可行构造，再冻结现代纪录。|
|T009 Tammes 球面码|16 points on S², T009-C02|认证最小角下界0.9118367215999161弧度|15点已解，改用16点开放配置。|
|T014 正方形中的 Heilbronn 问题|n=11 points in unit square|minimum triangle area 1/27 for 11 points|公开点集；枚举三点可检查最小三角形面积。|
|T035 最小笼图|{"degree": 4, "girth": 10}|320|经典极值图；顶点数为标量，正则性和围长可直接检查。|
|T044 最短 Golomb ruler|{"marks": 29}|623|经典离散构造；29 标记避免已解的较小配置。|
|T060 覆盖设计|{"v": 24, "k": 14, "t": 4}|23|公开设计表；块数为标量，逐个检查目标子集是否被覆盖。|
|T066 线性码最小距离|{"n": 68, "k": 15, "q": 2}|24|有明确距离区间；15 维二元线性码可枚举全部 32768 个码字。|
|T067 二元码最大规模|{"n": 17, "distance": 6}|258|已发表人类基线；两两汉明距离可直接检查。|
|N001 奇环强积独立集|{"q": 7, "power": 5}|367|367 个词的人类见证已重算；提供组合图方向。|
|T057 和差问题 I|{"max_cardinality": 512, "integer_interval": [-1000000, 1000000]}|1.0597930945472454|覆盖两篇系统论文；人类整数集合与和差计数已核。|
|T073 低自相关二元序列（LABS）|{"L": 100}|638|长度 100 的人类序列已精确重算，目标能量为整数。|
|T079 自卷积不等式 AC1|{"steps": 208, "support": ["-1/4", "1/4"], "nonnegative": true}|1.5097201507458786|覆盖 SimpleTES 与 AlphaEvolve；208 步人类基线已精确重算。|
|T080 自卷积不等式 AC2|{"steps": 20, "support": ["-1/4", "1/4"], "nonnegative": true}|0.8892261730897966|独立的卷积目标；20 步人类基线已精确积分。|
|T081 允许负值的自卷积 AC3|{"steps": 208, "support": ["-1/4", "1/4"], "signed_values_allowed": true, "integral": 1}|1.5097201507458786|覆盖 DREAM-RSI；明确绝对值评分，使用合法的人类转移基线。|
|T082 Erdős 最小重叠|{"steps": 51, "support": "[0,2]", "range": "0≤f≤1", "integral": 1}|Haugland (2016): symmetric 51-step function gives upper bound 0.3809268534330870 for the limiting constant.|覆盖 SimpleTES；51 步基线可用有限个分段端点精确验证。|
|T089 符号矩阵最大行列式|{"n": 29, "entries": "±1"}|Solomon/Orrick construction: \|det A\|=320·7^12·2^28. Brent hosts compressed/full Gram matrix and 4,918 known H-classes.|经典矩阵问题；整数行列式可精确计算。|
|T099 窄可容许素数元组|{"k": 343, "objective": "minimum diameter admissible k-tuple"}|Thomas Engelsma (2013): k=343 admissible tuple of diameter 2340. The supplied local artifact checks 343 distinct entries, the diameter, and residue-class noncoverage for all 68 primes p≤343.|343 个整数见证已重算；有限个素数的剩余类检查即可验证。|
|T097 最短加法链|{"target": "2^192−2^64−3 (NIST P-192 field inversion exponent)"}|A public previous chain of length 203 (McLoughlin) and current public chain of length 202 (Brian Smith); both are explicit finite construction records.|公开人类加法链；链长为整数，每步加法可直接检查。|

## 全量核查目录

|编号|任务|类别|状态|通过配置|
|---|---|---|---|---:|
|T001|Equal-circle packing in fixed containers|几何装填与覆盖|已确认适合|1|
|T002|Packing unit squares in squares|几何装填与覆盖|已确认适合|1|
|T003|Equilateral-triangle packing in a square|几何装填与覆盖|已确认适合|1|
|T004|Maximum polygon packing (CG:SHOP 2024)|几何装填与覆盖|已确认适合|1|
|T005|Unequal-circle packing: maximum sum of radii|几何装填与覆盖|已确认适合|2|
|T006|Erdős unequal squares: maximum total side length|几何装填与覆盖|已确认适合|1|
|T007|Circles covering circles|几何装填与覆盖|已确认适合|1|
|T008|Covering a square with unit squares|几何装填与覆盖|已确认适合|1|
|T009|Tammes problem / spherical codes|球面与极值点集|已确认适合|1|
|T010|Riesz energy minimization on the sphere (Thomson at s=1)|球面与极值点集|已确认适合|1|
|T011|Minimum-size spherical t-design|球面与极值点集|已确认适合|1|
|T012|Maximum-volume polytope with N vertices on a sphere|球面与极值点集|已确认适合|1|
|T013|Heilbronn problem for a free convex region|球面与极值点集|已确认适合|1|
|T014|Heilbronn triangle problem in a square|球面与极值点集|已确认适合|1|
|T015|Minimum maximum-to-minimum pair-distance ratio|球面与极值点集|已确认适合|1|
|T016|Largest small n-gon|球面与极值点集|已确认适合|1|
|T017|Erdős minimum distinct-distance problem|球面与极值点集|待补证|0|
|T019|Erdős–Szekeres happy-ending number f(k)|球面与极值点集|已确认适合|1|
|T020|Minimum-dilation triangulation|几何图与计算几何|所选配置已排除|0|
|T021|Minimum-weight triangulation|几何图与计算几何|待补证|0|
|T022|Minimum convex partition of a point set|几何图与计算几何|待补证|0|
|T023|Minimum coverage by convex polygons (CG:SHOP 2023)|几何图与计算几何|已确认适合|1|
|T024|Minimum partition into plane subgraphs (CG:SHOP 2022)|几何图与计算几何|已确认适合|1|
|T025|Minimum non-obtuse triangulation (CG:SHOP 2025)|几何图与计算几何|已确认适合|1|
|T026|Minimum-area simple polygonalization|几何图与计算几何|已确认适合|1|
|T027|Maximum-area simple polygonalization|几何图与计算几何|已确认适合|1|
|T028|Rectilinear crossing number of K_n|几何图与计算几何|已确认适合|1|
|T029|Erdős maximum unit distances for n planar points|几何图与计算几何|已确认适合|1|
|T030|Orchard planting / maximum 3-rich lines|几何图与计算几何|已确认适合|1|
|T031|No-three-in-line maximum on an n×n grid|几何图与计算几何|已确认适合|1|
|T032|Simple perfect squared squares: minimum primitive side at fixed order|铺砌与分割|已确认适合|1|
|T033|Mrs. Perkins’s quilt|铺砌与分割|已确认适合|1|
|T034|Klarner order of a polyomino|铺砌与分割|待补证|0|
|T035|(d,g)-cage order|极值图与超图|已确认适合|1|
|T036|Degree–diameter problem|极值图与超图|已确认适合|1|
|T037|Zarankiewicz number Z_{s,t}(m,n)|极值图与超图|已确认适合|1|
|T038|Forbidden-subgraph extremal number ex(n,F)|极值图与超图|已确认适合|1|
|T039|Graph saturation number sat(n,F)|极值图与超图|已确认适合|1|
|T040|Classical Ramsey number lower-bound construction|极值图与超图|已确认适合|1|
|T041|Hypergraph Turán number ex_r(n,F)|极值图与超图|已确认适合|1|
|T042|Erdős–Rogers function f_{s,t}(n)|极值图与超图|已确认适合|1|
|T043|Minimum triangles at fixed edge count|极值图与超图|待补证|0|
|T044|Optimal Golomb ruler length|加法组合与离散构造|已确认适合|1|
|T045|Minimum diameter of a B_h set of integers, h≥3|加法组合与离散构造|待补证|0|
|T046|Difference triangle sets|加法组合与离散构造|待补证|0|
|T047|Maximum cap set in F_3^n|加法组合与离散构造|已确认适合|1|
|T048|Largest 3-term-progression-free subset of [n]|加法组合与离散构造|已确认适合|1|
|T049|Minimum difference basis for [n]|加法组合与离散构造|已确认适合|1|
|T051|Schur number S(k) lower-bound coloring|加法组合与离散构造|已确认适合|1|
|T052|van der Waerden number lower-bound coloring|加法组合与离散构造|已确认适合|1|
|T053|Longest finite sequence with discrepancy at most C|加法组合与离散构造|已确认适合|1|
|T054|Largest square-difference-free subset of [N]|加法组合与离散构造|已确认适合|1|
|T055|Finite-set sum–product growth minimization|加法组合与离散构造|已确认适合|1|
|T056|Minimum finite-field Kakeya set size|加法组合与离散构造|已确认适合|1|
|T057|Sum–difference I: normalized logarithmic ratio|加法组合与离散构造|已确认适合|1|
|T058|Sum–difference II: unnormalized logarithmic ratio|加法组合与离散构造|已确认适合|1|
|T059|Sum–difference III: finite certificate for asymptotic exponent|加法组合与离散构造|已确认适合|1|
|T060|Covering number C(v,k,t)|组合设计|已确认适合|2|
|T061|Covering array CAN(t,k,v)|组合设计|所选配置已排除|0|
|T062|Orthogonal array minimum-run construction|组合设计|待补证|0|
|T063|Packing number D(v,k,t)|组合设计|待补证|0|
|T064|Social golfer maximum schedule length|组合设计|已确认适合|1|
|T065|Maximum number of mutually orthogonal Latin squares|组合设计|已确认适合|1|
|T066|Best minimum distance of linear codes|编码理论|已确认适合|1|
|T067|Maximum size of a binary code A(n,d)|编码理论|已确认适合|1|
|T068|Constant-weight code A(n,d,w)|编码理论|已确认适合|1|
|T069|Constant-dimension subspace code A_q(n,d;k)|编码理论|已确认适合|1|
|T070|Covering code size|编码理论|已确认适合|1|
|T071|Maximum permutation code size|编码理论|已确认适合|1|
|T072|Maximum deletion-correcting code size|编码理论|已确认适合|1|
|T073|LABS minimum aperiodic autocorrelation energy|序列与平坦多项式|已确认适合|1|
|T074|LABS peak sidelobe level (PSL)|序列与平坦多项式|已确认适合|1|
|T075|Periodic binary autocorrelation energy|序列与平坦多项式|待补证|0|
|T076|Binary sequence maximum out-of-phase autocorrelation (periodic merit)|序列与平坦多项式|待补证|0|
|T077|Littlewood polynomials: minimum supremum modulus|序列与平坦多项式|已确认适合|1|
|T078|Littlewood polynomials: maximum infimum modulus|序列与平坦多项式|待补证|0|
|T079|First Autocorrelation Inequality (AC1)|极值分析|已确认适合|1|
|T080|Second Autocorrelation Inequality (AC2)|极值分析|已确认适合|1|
|T081|Third Autocorrelation Inequality (AC3)|极值分析|已确认适合|2|
|T082|Erdős Minimum Overlap|极值分析|已确认适合|1|
|T083|Autocorrelation lower envelope for difference bases|极值分析|已确认适合|1|
|T084|Sign uncertainty principle (Fourier sign changes)|极值分析|已确认适合|1|
|T085|Cohn–Elkies linear-programming bound for sphere packing|极值分析|已确认适合|1|
|T086|General one-dimensional Gagliardo–Nirenberg sharp constant|极值分析|待补证|0|
|T087|Rudin spherical harmonic Lp extremizer|极值分析|待补证|0|
|T088|Ovals curvature Schrödinger eigenvalue|极值分析|已确认适合|1|
|T089|Maximum determinant of sign matrices|矩阵、格与代数极值|已确认适合|1|
|T090|Minkowski lattice packing density|矩阵、格与代数极值|已确认适合|1|
|T092|Schmeisser polynomial critical-point barycenter constant|矩阵、格与代数极值|已确认适合|1|
|T093|Borcea p-moment critical-point distance constant|矩阵、格与代数极值|已确认适合|1|
|T094|Noncommutative matrix AM–GM ratio|矩阵、格与代数极值|待补证|0|
|T095|Minimum Mahler measure of noncyclotomic integer polynomials|矩阵、格与代数极值|已确认适合|1|
|T096|Integer Chebyshev polynomial construction|矩阵、格与代数极值|已确认适合|1|
|T097|Shortest addition chain|数论与算术构造|已确认适合|1|
|T098|Integer complexity|数论与算术构造|已确认适合|1|
|T099|Narrow admissible prime k-tuples|数论与算术构造|已确认适合|1|
|T100|Factoring N! into N balanced factors|数论与算术构造|待补证|0|
|N001|Shannon capacity: independent sets in strong powers of odd cycles|极值图与超图|已确认适合|1|
|N002|Smale mean value extremal constant|矩阵、格与代数极值|已确认适合|1|
|N003|Spherical cap covering / minimizing covering radius|球面与极值点集|已确认适合|1|
|N004|Lattice sphere covering density|矩阵、格与代数极值|已确认适合|1|
|N005|Lattice quantizer normalized second moment|矩阵、格与代数极值|已确认适合|1|
|N006|Exact tensor rank of 3x3 matrix multiplication over Q|矩阵、格与代数极值|已确认适合|1|
|N007|Border rank of 3x3 matrix multiplication over C|矩阵、格与代数极值|已确认适合|1|
|N008|Addition count for rank-23 3x3 matrix multiplication schemes|矩阵、格与代数极值|已确认适合|1|
|N009|Waring rank of generic 4x4 determinant|矩阵、格与代数极值|已确认适合|1|
|N010|Minimum order n_6(4) of a 4-chromatic girth-at-least-6 graph|极值图与超图|已确认适合|1|
|N011|Perfect hash families PHF(N;k,v,t)|组合设计|待补证|0|
|N012|d-disjunct / d-cover-free binary matrices|组合设计|已确认适合|1|
|N013|Global postage-stamp problem / extremal additive h-basis|加法组合与离散构造|已确认适合|1|

## 需要保留的限制

- 全部有核查记录，不表示全部通过。待补证条目尚未满足完整选型要求。
- 确认基于所列来源；不是穷尽全部2026文献后的无遗漏保证。
- 配置记录数包含已固定的公开实例或明确参数。已排除、待补证记录不计入可用配置。
- 历史人类基线不必是当前纪录；超过它不自动构成新的世界纪录。
- 连续任务的文献数值、浮点验证与严格数学证书分开。
- 首批为选型建议；本轮没有实现求解器或通用评分器。
- 仍未达到100个已确认家族，缺口保持可见。

## 数据与证据

逐条参数、基线、作者、来源、核查动作和剩余事项见 [JSON](confirmation_summary.json) 与 [CSV](confirmation_summary.csv)。原始分方向记录见 `confirmation_geometry.*`、`confirmation_discrete.*`、`confirmation_algebra.*`；额外离散核查见 `confirmation_discrete_supplement.*`。汇总表包含主代理修订，以汇总表为当前入口。

SimpleTES与DREAM-RSI的数学核心并集为7个任务家族，首批全部纳入。AlphaEvolve按任务家族映射；已解决、非标量、验证开销大或缺同配置基线的原题不自动准入。完整原题去向见 [覆盖审计](sota_task_coverage.md)。
