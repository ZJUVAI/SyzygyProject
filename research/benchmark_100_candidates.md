> **2026-11-03修订：本文含第一版选型信息；已解校准配置不再准入。现行清单及删除记录见 [发现轨修订](discovery_candidates_v2.md) 和 [仅发现轨规则](discovery_only_policy.json)。

# 数学构造 benchmark：100个任务候选与初期20项建议

这是选型研究稿，不是已发布benchmark。**12个类别、100个任务候选；初期建议20个任务，按每项2个配置规划40个配置。** 已发布/已完整审计的配置数尚未建立，不能将40写成已验证规模。

所有条目都有自然标量目标。原始Luna调研中的重复、纯存在性和目标平凡条目未用来凑数。仍保留有条件候选，尤其尚缺具体人类构造、有限参数或严格认证者；这里没有声称100项human baseline已经复现。

人类传统数学/计算搜索与AI结果分列；引用历史纪录不表示2026最新纪录。五个任务的少量见证已在本次重算：Sum–difference I/III、窄admissible tuple、minimum overlap、LABS，见baseline_examples/recomputed_examples.json。其余任务的引用只表示文献/数据入口已定位。

## 分类概览

| 类别 | 任务数 | 编号 |
|---|---:|---|
|几何装填与覆盖|8|T001–T008|
|球面与极值点集|11|T009–T019|
|几何图与计算几何|12|T020–T031|
|铺砌与分割|3|T032–T034|
|极值图与超图|9|T035–T043|
|加法组合与离散构造|16|T044–T059|
|组合设计|6|T060–T065|
|编码理论|7|T066–T072|
|序列与平坦多项式|6|T073–T078|
|极值分析|10|T079–T088|
|矩阵、格与代数极值|8|T089–T096|
|数论与算术构造|4|T097–T100|

## 初期20项

优先覆盖两篇系统论文的数学核心和用户提出的六个方向；优先是调研/实例化顺序，不表示所有配置已准备发布。几何图与分割保留各一项，编码选小维数以控制验证成本。

|编号|任务|原始标量及方向|
|---|---|---|
|T002|Packing unit squares in squares|minimum enclosing-square side s(n) ↓|
|T001|Equal-circle packing in fixed containers|maximum common radius in unit square (equivalently minimum container side for unit disks) ↑|
|T005|Unequal-circle packing: maximum sum of radii|sum_i r_i ↑|
|T014|Heilbronn triangle problem in a square|minimum area over all point triples ↑|
|T009|Tammes problem / spherical codes|minimum pairwise angular distance ↑|
|T099|Narrow admissible prime k-tuples|max(H)-min(H) ↓|
|T044|Optimal Golomb ruler length|ruler length ↓|
|T038|Forbidden-subgraph extremal number ex(n,F)|number of edges ↑|
|T020|Minimum-dilation triangulation|maximum pairwise stretch (dilation) ↓|
|T032|Simple perfect squared squares: minimum primitive side at fixed order|primitive outer-square side length ↓|
|T060|Covering number C(v,k,t)|number of blocks ↓|
|T061|Covering array CAN(t,k,v)|number of rows N ↓|
|T066|Best minimum distance of linear codes|Minimum Hamming distance d(C) ↑|
|T089|Maximum determinant of sign matrices|\|det A\| (equivalently the normalized determinant in the cited benchmark) ↑|
|T073|LABS minimum aperiodic autocorrelation energy|E (equivalently merit factor L²/(2E)) ↓|
|T079|First Autocorrelation Inequality (AC1)|Phi1=max_t(f*f)(t) ↓|
|T080|Second Autocorrelation Inequality (AC2)|Phi2=\|\|f*f\|\|_2^2/(\|\|f*f\|\|_1\|\|f*f\|\|_infinity) ↑|
|T081|Third Autocorrelation Inequality (AC3)|Phi3=max_t \|(f*f)(t)\| ↓|
|T082|Erdős Minimum Overlap|Ψ(f)=sup_{t∈R}∫_R f(x)g(x+t)dx, where f,g are supported on [0,2] and g=1−f on [0,2] (lower is better). Equivalent to the intersection-range integral; both positive and negative shifts are included. ↓|
|T057|Sum–difference I: normalized logarithmic ratio|log(\|A+A\|/\|A\|)/log(\|A-A\|/\|A\|) ↑|

## 全部100项

配置只是参数实例，未给出行级构造和分数前不计入已发布z。相关家族（如不同编码子类、不同序列范数）应分层汇总，避免视作完全独立证据。

### T001 · Equal-circle packing in fixed containers · MVP

- 类别：几何装填与覆盖。
- 问题：Place n congruent disks without overlap in a square and minimize the square side (equivalently maximize the common disk radius in a unit square).
- 输出：disk centers and radius, or normalized center coordinates
- 单一标量：`maximum common radius in unit square (equivalently minimum container side for unit disks)`；越大越好。统一高分方向 `J`。
- 配置：{"n": "圆数量", "container": "单位正方形为主；圆形/矩形等独立基线容器配置"}
- 人类基线证据：Packomania lists best-known values, coordinates, drawings, contact graphs, and attribution codes for n up to 10000; it marks proven optima. Human attribution in records, AI involvement unknown.
- 验证成本：medium; pairwise distance and wall-clearance checks; upper-bound optimality is generally hard
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Packomania is a changing best-known catalogue, not a proof for most n; choose frozen version/instances and verify contact tolerances.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://packomania.com/csq/)；[来源2](https://packomania.com/)

### T002 · Packing unit squares in squares · MVP

- 类别：几何装填与覆盖。
- 问题：Pack n non-overlapping unit squares, allowing arbitrary rotation, into the smallest enclosing square.
- 输出：square centers and orientations; enclosing side s
- 单一标量：`minimum enclosing-square side s(n)`；越小越好。统一高分方向 `-J`。
- 配置：{"n": "正方形数量", "container": "正方形主轨；其他容器须独立基线"}
- 人类基线证据：Erich Friedman’s 2009 survey gives best-known bounds/packings for n≤100 and historical authors. It proves selected n and reports named constructions by Göbel, Trump, Wainwright, Hämäläinen, Bidwell, Cantrell, and others; computer-search involvement is explicit for some later records. AI involvement unknown.
- 验证成本：medium; non-overlap and enclosure directly checkable; optimality proof hard
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Do not treat upper-bound construction as proven optimum except rows marked/proven in the paper; use exact coordinate reconstruction.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://erich-friedman.github.io/papers/squares/squares.html)；[来源2](https://kingbird.myphotos.cc/packing/squares_in_squares.html)

### T003 · Equilateral-triangle packing in a square

- 类别：几何装填与覆盖。
- 问题：Pack n unit equilateral triangles, arbitrary orientations, inside the smallest square.
- 输出：triangle placements and square side
- 单一标量：`minimum square side`；越小越好。统一高分方向 `-J`。
- 配置：n; unit side triangles; rotations allowed
- 人类基线证据：Friedman’s page gives per-n constructions and named records: Friedman (1996), Maurizio Morandi (2008), with later results; AI involvement unknown.
- 验证成本：medium
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Page updated in 2026; freeze selected historical instance and confirm exact coordinates; many records are upper bounds only.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://erich-friedman.github.io/packing/triinsqu/)

### T004 · Maximum polygon packing (CG:SHOP 2024)

- 类别：几何装填与覆盖。
- 问题：Select a subset of given polygonal items and place them inside a container polygon without overlap, using translations only, maximizing the official weight/area objective.
- 输出：selected polygon IDs and translations
- 单一标量：`total selected item area/weight as defined by challenge`；越大越好。统一高分方向 `J`。
- 配置：official CG:SHOP 2024 item/container instances; no rotation per challenge definition
- 人类基线证据：Official challenge and paper document 2024 competition, data, ranking, and participating solvers; Shadoks paper describes their feasible solutions. AI involvement unknown.
- 验证成本：medium; polygon containment and non-overlap checks
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Confirm official scoring is exactly total area/weight (and all rules); internal optimum NP-hard, so use returned feasible value or valid bound.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2024/)；[来源2](https://arxiv.org/abs/2403.16203)；[来源3](https://arxiv.org/abs/2403.20123)

### T005 · Unequal-circle packing: maximum sum of radii · MVP

- 类别：几何装填与覆盖。
- 问题：Pack n or a source-defined number of circles in a fixed container, maximizing their total perimeter subject to containment and non-overlap.
- 输出：circle centers/radii
- 单一标量：`sum_i r_i`；越大越好。统一高分方向 `J`。
- 配置：fixed container and either fixed n or source-defined permitted counts
- 人类基线证据：Friedman’s catalog lists a ‘Packing Copies to Maximize Total Perimeter’ section, including circles in squares, but specific page outcomes/authors are not verified here; unknown.
- 验证成本：medium
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Variable radii/count may be part of optimization; exact source problem needs reading. Do not define own penalty.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www.packomania.com/csqv/csqv.html)；[来源2](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/36.html)

### T006 · Erdős unequal squares: maximum total side length

- 类别：几何装填与覆盖。
- 问题：在单位正方形中放置 n 个可旋转、大小可不同、内部不重叠的正方形。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`sum_i side_i`；越大越好。统一高分方向 `J`。
- 配置：{"n": "正方形数量", "rotation": "允许任意旋转；平行边子类单列配置"}
- 人类基线证据：Halasz (1984)、Erdős–Soifer (1995)、Campbell–Staton (2005) 有显式构造；例如 n=k²+2 的历史下界 k+1/(k+1)。选定非平方数配置后须重建原文布局。
- 验证成本：中：多边形相交与边界精确谓词。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：不同于等尺寸正方形装填；历史公式的旋转和零边长约定须锁定。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/55.html)；[来源2](https://doi.org/10.1080/00029890.2005.11920180)

### T007 · Circles covering circles

- 类别：几何装填与覆盖。
- 问题：Place n unit disks to cover the largest possible circular target disk.
- 输出：unit-disk centers and target radius
- 单一标量：`maximum target radius covered`；越大越好。统一高分方向 `J`。
- 配置：{"n": "覆盖圆数量", "target": "单位圆/单位正方形等各固定配置"}
- 人类基线证据：Friedman’s table reports named discoveries and proven records (e.g. Bezdek, Fejes Tóth, Melissen, Tan) for n values, along with a 2026 proof attribution for several; AI involvement is unknown, so historical attribution must not be read as AI-free.
- 验证成本：medium; union containment check and radius calculation; optimality proof hard
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Dynamic page has post-cutoff updates; freeze a dated snapshot and select explicit constructions with machine-readable coordinates if possible.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://erich-friedman.github.io/packing/circovcir/)

### T008 · Covering a square with unit squares

- 类别：几何装填与覆盖。
- 问题：Among coverings of a square by n unit squares (overlap allowed), maximize the side of the covered target square.
- 输出：square placements including orientations
- 单一标量：`maximum target-square side s(n)`；越大越好。统一高分方向 `J`。
- 配置：n; covering squares have side 1; overlap allowed
- 人类基线证据：Friedman and Paterson’s paper gives constructions/bounds and named sources; known optimality only for n=2,3,5,10 and square n per the survey. Authors of unattributed examples are given; AI involvement unknown.
- 验证成本：medium; exact coverage of target square requires geometric union check; optimum proofs difficult
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Only keep instances with archived explicit configurations; source says many bounds are not exact optima.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://erich-friedman.github.io/papers/covering/covering.html)；[来源2](https://erich-friedman.github.io/papers/covering.pdf)

### T009 · Tammes problem / spherical codes · MVP

- 类别：球面与极值点集。
- 问题：Place N points on S² to maximize their minimum pairwise angular separation (equivalently chord distance).
- 输出：N unit vectors
- 单一标量：`minimum pairwise angular distance`；越大越好。统一高分方向 `J`。
- 配置：N; dimension 3 for cited tables
- 人类基线证据：Henry Cohn’s table lists constructions through N=32 with nearest-pair inner products and rattler counts; Sloane’s tables include downloadable coordinates. Records are not all proven optima. Historical human attribution; AI use unknown.
- 验证成本：Low for feasibility; global optimality is hard.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Use a frozen N row and report best-known versus proven status; do not count distinct container variants as separate tasks.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://cohn.mit.edu/spherical-codes/)；[来源2](https://neilsloane.com/packings/)；[来源3](https://cohn.mit.edu/sloane/)

### T010 · Riesz energy minimization on the sphere (Thomson at s=1)

- 类别：球面与极值点集。
- 问题：For fixed N points on S², minimize the sum over unordered pairs of distance raised to −s; Thomson is s=1.
- 输出：N unit vectors / coordinate file
- 单一标量：`Σ(i<j) ||xi−xj||^(−s)`；越小越好。统一高分方向 `-J`。
- 配置：N and exponent s; fix s=1 for Thomson
- 人类基线证据：Cambridge Riesz Energy Database, s=1, lists 53 lowest-known minima for N=512–9913, with energy, symmetry, and downloadable coordinates; N=512 energy 124673.9055677. These are lowest located minima, not all certified global minima. AI use unknown.
- 验证成本：Low-medium; evaluate all pair terms with suitable precision.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Freeze N,s and do not call a located minimum globally optimal without proof.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/index.html)；[来源2](https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html)

### T011 · Minimum-size spherical t-design

- 类别：球面与极值点集。
- 问题：For fixed dimension and strength t, find an equal-weight spherical t-design using the fewest points.
- 输出：point coordinates plus moment identities/certificate
- 单一标量：`number of points N`；越小越好。统一高分方向 `-J`。
- 配置：fix dimension d and strength t; S² is the best documented library
- 人类基线证据：Hardin–Sloane library provides putatively optimal designs and coordinates. Their paper reports a 24-point 7-design first found by McLaren (1963), and records existence/minimal-size claims; it explicitly distinguishes analytic proofs from numerical coordinates. AI use unknown.
- 验证成本：Medium-high; check all polynomial moments, with exactness needed for a proof.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Small residual is not proof of exact design or minimum N; choose rows with exact coordinates and lower-bound certificate. Exact moment identities need certificates; approximate designs are a separately named track.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://neilsloane.com/sphdesigns/)；[来源2](https://cohn.mit.edu/sloane/)；[来源3](https://doi.org/10.1007/BF02711518)

### T012 · Maximum-volume polytope with N vertices on a sphere

- 类别：球面与极值点集。
- 问题：Choose at most N vertices on the unit sphere in R³ to maximize convex-hull volume.
- 输出：unit-vector coordinates / named polyhedron
- 单一标量：`convex-hull volume`；越大越好。统一高分方向 `J`。
- 配置：vertex cap N; unit sphere in R³
- 人类基线证据：Sloane tables include maximal-volume arrangements and downloadable coordinates. A 2026 paper resolves N=9 exactly: volume 3√(2√3−3), attained by a triaugmented triangular prism of specified shape. Human theorem and construction; AI use unknown.
- 验证成本：Medium to calculate hull volume; optimum proof depends on N.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Clarify at-most versus exactly N vertices. N=9 is a calibration, not open discovery.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://cohn.mit.edu/sloane/)；[来源2](https://arxiv.org/abs/2608.04392)

### T013 · Heilbronn problem for a free convex region

- 类别：球面与极值点集。
- 问题：Place N points in any unit-area convex region to maximize the smallest triangle area among triples, normalized by the convex hull area.
- 输出：point coordinates
- 单一标量：`minimum triple triangle area divided by convex-hull area`；越大越好。统一高分方向 `J`。
- 配置：N; convex hull is free and normalized to area 1
- 人类基线证据：Tej Stead’s table provides coordinates and a rational-arithmetic verifier. For N=8, A=0.0800001393294664…; David Cantrell found the construction (2007), and Tej Stead proved optimality (2026). The value is the root of 2060x^5−2332x^4+1064x^3−240x^2+26x−1.
- 验证成本：Low for candidate coordinates; upper-bound proof varies by N.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Living page has later AI-assisted records; use N=8 and label provenance explicitly.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://math.tejstead.com/heilbronn/convex/)；[来源2](https://math.tejstead.com/heilbronn/)

### T014 · Heilbronn triangle problem in a square · MVP

- 类别：球面与极值点集。
- 问题：Choose n points in a unit square to maximize the area of the smallest triangle determined by any three chosen points.
- 输出：n point coordinates
- 单一标量：`minimum area over all point triples`；越大越好。统一高分方向 `J`。
- 配置：n; unit square domain
- 人类基线证据：Tej Stead maintains a dedicated Heilbronn-problem page linked by Friedman’s catalog; this audit did not verify specific authors, numeric records, or downloadable data, so baseline is unknown.
- 验证成本：low for a given point set (enumerate triples); optimum determination is hard
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：An instance is n and domain; published records and coordinate data must be verified before admission. Do not use nested optimum as scorer.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://math.tejstead.com/heilbronn/square/)；[来源2](https://github.com/spiralulam/heilbronn)

### T015 · Minimum maximum-to-minimum pair-distance ratio

- 类别：球面与极值点集。
- 问题：Choose N points in R^d to minimize maximum pair distance divided by minimum pair distance; scale and translation are immaterial.
- 输出：N coordinates
- 单一标量：`max pair distance / min pair distance`；越小越好。统一高分方向 `-J`。
- 配置：N,d; choose 2D N=5 or 7 for proved records
- 人类基线证据：Friedman’s records state r²=(3+√5)/2 for N=5 and r²=4 for N=7, proved by Bateman and Erdős (1951); N=8 is proved by Bezdek and Fodor (1999). Diagrams are published. Newer rows include 2026 contributors; AI use there unknown.
- 验证成本：Low for a candidate; global optimum proof hard for larger N.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Do not constrain points to an arbitrary box; avoid recent AI-assisted rows if using a human-only baseline.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://erich-friedman.github.io/packing/maxmin/)；[来源2](https://doi.org/10.1007/BF02574074)

### T016 · Largest small n-gon

- 类别：球面与极值点集。
- 问题：Among convex n-gons of diameter at most 1, maximize area.
- 输出：cyclic vertex coordinates with diameter normalized
- 单一标量：`polygon area`；越大越好。统一高分方向 `J`。
- 配置：n vertices; diameter bound 1; convexity
- 人类基线证据：Reinhardt (1922) proved regular n-gons optimal for every odd n. Exact/global records also exist for n=4,6,8,10,12; Henrion–Messine used GloptiPoly for n=10,12 with global/numerical guarantees, and Audet et al. gave exact algebraic equations for small even cases.
- 验证成本：Low for area/diameter/convexity; global certificate specialized.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Choose a fixed n and distinguish proof from local numerical record.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://optimization-online.org/wp-content/uploads/2020/09/8019.pdf)；[来源2](https://arxiv.org/abs/1103.4456)；[来源3](https://www.mcs.anl.gov/~more/cops/bcops/polygon.html)

### T017 · Erdős minimum distinct-distance problem

- 类别：球面与极值点集。
- 问题：For a fixed N, choose N distinct planar points that determine as few distinct positive pairwise Euclidean distances as possible.
- 输出：N point coordinates; normalize by similarity
- 单一标量：`number of distinct pairwise distances`；越小越好。统一高分方向 `-J`。
- 配置：N; Euclidean plane; arbitrary point coordinates
- 人类基线证据：Erdős (1946) introduced D(N). A square lattice construction gives O(N/sqrt(log N)) distinct distances for square-grid sizes; Guth and Katz (Annals 2015) prove every N-point planar set determines at least cN/log N distances. For N=4 a square gives exactly 2 distances and is a simple exact calibration. AI use unknown for historical constructions.
- 验证成本：Low for a fixed exact/rational coordinate set; global optimum proof is hard.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：A construction yields an upper bound on the minimum, not a proof of optimality. Use exact small-N calibration or compare distinct-distance count only; do not require an uncertified inner optimum.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://annals.math.princeton.edu/wp-content/uploads/annals-v181-n1-p02-p.pdf)

### T018 · Largest point set with no empty convex hexagon

- 类别：球面与极值点集。
- 问题：Find a largest finite point set in general position with no empty convex 6-gon.
- 输出：point coordinates
- 单一标量：`number of points`；越大越好。统一高分方向 `J`。
- 配置：forbidden polygon size 6; no three collinear
- 人类基线证据：Overmars (2003) found 29 points with no empty hexagon. Gerken and Nicolás proved every 30-point set contains one, so optimum is 29. A public paper gives the construction/search; formal verification work supplies a SAT certificate for the upper bound. Human result with computer-assisted search/proof.
- 验证成本：Low for candidate set; global upper proof is high.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Solved calibration; retrieve point coordinates from Overmars paper/data before admitting.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://citeseerx.ist.psu.edu/document?doi=40b403e751d8807c5609b9eb571711077489bf45&repid=rep1&type=pdf)；[来源2](https://arxiv.org/abs/2403.00737)；[来源3](https://arxiv.org/abs/2403.17370)

### T019 · Erdős–Szekeres happy-ending number f(k)

- 类别：球面与极值点集。
- 问题：Find the minimum N such that every N points in general position in the plane contain k points in convex position.
- 输出：For lower-bound witness, coordinates of N−1 points with no convex k-gon; score N−1. Exact f(k) only with matching upper proof.
- 单一标量：`largest point-set size avoiding a convex k-gon`；越大越好。统一高分方向 `J`。
- 配置：{"convex_subset_size": "k"}
- 人类基线证据：Erdős–Szekeres (1935) proved finiteness and conjectured f(k)=2^{k−2}+1; exact f(3)=3 through f(6)=17 are known, with Peters (2006) computer proof for f(6)=17. Suk (2017) gives f(k)=2^{k+o(k)}.
- 验证成本：Geometric general-position and convexity checks are low with exact coordinates; upper proof is difficult.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：A lower-bound point set is finite and checkable but does not prove f(k); coordinates may be algebraic and need exact predicates.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0EC7876789232266D60439A4C00D86D9/S144618110000300Xa.pdf/computer_solution_to_the_17point_erdosszekeres_problem.pdf)；[来源2](https://arxiv.org/abs/1604.08657)

### T020 · Minimum-dilation triangulation · MVP

- 类别：几何图与计算几何。
- 问题：For a fixed point set, triangulate it to minimize the maximum ratio of triangulation shortest-path distance to straight-line distance over all point pairs.
- 输出：triangulation edge list
- 单一标量：`maximum pairwise stretch (dilation)`；越小越好。统一高分方向 `-J`。
- 配置：Point set; 2014 library has 210 instances with 10–70 points
- 人类基线证据：UNICAMP archive provides 210 MDTP instances and results for Brandt, Gaiowski, de Rezende, de Souza (2014). Fekete, Keldenich, Perk (SoCG 2025) give exact algorithms and optimal regular n-gon results through n=100, with methods up to 30,000 points.
- 验证成本：Medium-high; all-pairs paths and accurate sums of radicals.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Do not assume every instance has certified optimum; use published exact instances/results or compare feasible values with bounds.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www.ic.unicamp.br/~cid/Problem-instances/Dilation/MDTP/index.html)；[来源2](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.48)；[来源3](https://arxiv.org/abs/2502.18189)

### T021 · Minimum-weight triangulation

- 类别：几何图与计算几何。
- 问题：Triangulate a fixed planar point set with straight edges minimizing the sum of edge lengths.
- 输出：triangulation edge list
- 单一标量：`sum of Euclidean edge lengths`；越小越好。统一高分方向 `-J`。
- 配置：point set; no Steiner vertices; hull edges included
- 人类基线证据：Haas (SoCG 2018) reports certified optima on public benchmark classes up to 30 million uniform/normal points, TSPLIB up to 85,900, and VLSI up to 744,710; earlier Beirouti–Snoeyink exact uniform cases reached 80,000. Human algorithmic records; AI use unknown.
- 验证成本：Medium to compute edge sum; global optimum is NP-hard in general.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Need match a source instance to its solution/certificate. Never use uncertified inner optimum as answer.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2018.44)；[来源2](https://arxiv.org/abs/1802.06415)；[来源3](https://arxiv.org/abs/cs/0601002)

### T022 · Minimum convex partition of a point set

- 类别：几何图与计算几何。
- 问题：给定平面有限点集，在其凸包内构造无交叉直线图，使每个输入点为顶点且每个有界面凸，不允许Steiner点，最小化有界面数。
- 输出：noncrossing diagonals or convex piece vertex lists
- 单一标量：`number of convex bounded faces`；越小越好。统一高分方向 `-J`。
- 配置：{"point_set": "固定点集实例；退化、共线、允许边界角等遵循CG:SHOP2020规则"}
- 人类基线证据：Published exact and integer-programming formulations exist, but a standardized public instance corpus with per-instance human values was not verified in this audit. Baseline unknown.
- 验证成本：Low for checking a proposed partition; proving minimum is harder.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：原代理将点集与polygon版本混写；此处固定为CG:SHOP2020点集版本。不能把允许Steiner点、简单polygon最优剖分等不同问题的基线移来。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2020/)；[来源2](https://arxiv.org/abs/2012.07939)

### T023 · Minimum coverage by convex polygons (CG:SHOP 2023)

- 类别：几何图与计算几何。
- 问题：Cover a given polygonal region with as few convex polygons as possible under the competition’s exact allowed-piece rules.
- 输出：list of convex polygon pieces
- 单一标量：`number of convex pieces`；越小越好。统一高分方向 `-J`。
- 配置：polygon instance and competition constraints; use official 2023 instances
- 人类基线证据：Official CG:SHOP 2023 challenge archive reports 22 teams and publishes instances/ranking; Copenhagen identifies William Bille Meyling, Mikkel Abrahamsen, André Nusser as first-place team (announced 2023). AI involvement unknown.
- 验证成本：medium; piece validity/coverage and piece-count checking
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Must reproduce challenge’s exact formulation; objective is a computable count but feasible coverage validation should be robust. Do not use count as an inner optimum oracle.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2023/)；[来源2](https://barc.ku.dk/news/bachelor-project-at-barc-wins-computational-geometry-challenge/)；[来源3](https://arxiv.org/abs/2303.07007)

### T024 · Minimum partition into plane subgraphs (CG:SHOP 2022)

- 类别：几何图与计算几何。
- 问题：Partition a geometric graph into the minimum number of planar subgraphs under the official challenge’s edge/vertex rules.
- 输出：color or partition of input edges into planar classes
- 单一标量：`number of parts/colors`；越小越好。统一高分方向 `-J`。
- 配置：official CG:SHOP 2022 graph instances and rule set
- 人类基线证据：Official CG:SHOP archive states this was the 2022 task; teams published algorithm/ranking materials (e.g. Crombez et al. Shadoks approach). AI involvement unknown.
- 验证成本：medium; crossing checks per part
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Exact task formalization and leaderboard records need confirmation; scalar optimum is hard, score feasible partition’s part count only.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2022/)；[来源2](https://pageperso.lis-lab.fr/guilherme.fonseca/CGSHOP22slides.pdf)

### T025 · Minimum non-obtuse triangulation (CG:SHOP 2025)

- 类别：几何图与计算几何。
- 问题：Triangulate an input point set / polygon with all triangles non-obtuse and minimize the competition-defined triangulation size.
- 输出：triangle vertex triples
- 单一标量：`number of triangles or Steiner vertices as specified by challenge`；越小越好。统一高分方向 `-J`。
- 配置：official CG:SHOP 2025 instances and the precise challenge objective
- 人类基线证据：A challenge paper is published as ‘Minimum Non-Obtuse Triangulations: The CG:SHOP Challenge 2025’; official CG:SHOP archive should contain results and instances. Specific winners/scores not verified in this audit; AI involvement unknown.
- 验证成本：medium; angle and triangulation checks
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：The competition objective may include Steiner points or other penalties; not admissible until precise scalar and human ranking are independently checked.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/2504.04412)；[来源2](https://cgshop.ibr.cs.tu-bs.de/)

### T026 · Minimum-area simple polygonalization

- 类别：几何图与计算几何。
- 问题：Given a planar point set, choose a simple polygon whose vertex set is exactly the input and minimize its area.
- 输出：cyclic permutation of point indices
- 单一标量：`polygon area`；越小越好。统一高分方向 `-J`。
- 配置：input point set; source datasets FHKPS and GEN; point count fixed per instance
- 人类基线证据：CG:SHOP 2019 produced a ranking and multiple published teams/algorithms; CG challenge paper (Demaine, Fekete, Keldenich, Krupke, Mitchell, 2022) documents it. Public benchmark site has instance/solution and result files. AI involvement unknown.
- 验证成本：low; simple polygon check and shoelace area exact for rational input
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：NP-hard inner optimum; do not score against purported optimum unless certified. Compare returned polygon’s computable area, or use only benchmark instances with verified optimum values.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2019/)；[来源2](https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Poly/)；[来源3](https://doi.org/10.1145/3504000)

### T027 · Maximum-area simple polygonalization

- 类别：几何图与计算几何。
- 问题：Given a planar point set, choose a simple polygon through every point exactly once that maximizes area.
- 输出：cyclic permutation of point indices
- 单一标量：`polygon area`；越大越好。统一高分方向 `J`。
- 配置：input point set; FHKPS/GEN benchmark instances
- 人类基线证据：CG:SHOP 2019 ranking and papers cover Max-Area; public benchmark data includes results and solution permutations. Human team names are available in challenge papers; AI involvement unknown.
- 验证成本：low; simple polygon validation plus shoelace area
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：NP-hard inner optimum. Use objective value of feasible returned polygon; comparing gap requires a valid upper bound, never an unverified optimum.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2019/)；[来源2](https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Poly/)；[来源3](https://doi.org/10.1145/3504000)

### T028 · Rectilinear crossing number of K_n

- 类别：几何图与计算几何。
- 问题：Place n points in general position in the plane and minimize the number of crossings in the straight-line drawing of K_n.
- 输出：Exact coordinates or order type; objective number of crossing edge pairs.
- 单一标量：`number of crossings`；越小越好。统一高分方向 `-J`。
- 配置：{"vertices": "n"}
- 人类基线证据：Exact values are known through small orders (K_9=36, K_10=62 and published tables extend further); Ábrego–Fernández-Merchant and collaborators maintain best-known bounds and constructions; all exact statuses must be frozen from the survey.
- 验证成本：Medium for exact coordinates/order type; proving minimum hard.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Do not merge with topological crossing number; numerical optimization coordinates need exact orientation tests.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/cs/0009023)；[来源2](https://www.csun.edu/~sf70713/publications/survey.pdf)；[来源3](https://www.crossingnumbers.org/projects/crossingconstants/rectilinear.php)

### T029 · Erdős maximum unit distances for n planar points

- 类别：几何图与计算几何。
- 问题：Maximize the number of unit-distance pairs among n distinct points in the Euclidean plane.
- 输出：Exact-coordinate point set; objective unit-distance pair count.
- 单一标量：`number of unit-distance pairs`；越大越好。统一高分方向 `J`。
- 配置：{"points": "n"}
- 人类基线证据：Alexeev, Mixon & Parshall (2024/2025) report that for n≤21 their upper bounds match best-known lower bounds and fully enumerate densest unit-distance graphs; exact values are thus recorded through 21. No claim about AI-generated or later constructions is used as human baseline.
- 验证成本：Witness edge count is checkable with exact algebraic coordinates; global maximum is hard beyond small n.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Distinguish exact n≤21 values from open larger n and avoid scoring floating-point near-unit distances; freeze the 2024/2025 paper version and accompanying data.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/2412.11914)

### T030 · Orchard planting / maximum 3-rich lines

- 类别：几何图与计算几何。
- 问题：给定N个互异实平面点，最大化恰好包含三个输入点的不同直线数；允许三点共线，不能施加“任意三点不共线”的一般位置条件。
- 输出：point coordinates and counted lines
- 单一标量：`number of distinct lines containing exactly three input points`；越大越好。统一高分方向 `J`。
- 配置：{"N": "输入点数", "coordinates": "整数、有理或精确代数数表示需固定"}
- 人类基线证据：Sloane’s A003035 table gives values (e.g. N=7→6, 11→16, 14→26); cubic-curve constructions by Burr, Grünbaum and Sloane provide explicit examples. 2026 work gives t3(15)=31 and excludes 32 with a certificate. Historical human constructions; newer computational component identified.
- 验证成本：Medium; exact collinearity/incidence checks.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：恰好3点的直线不等于所有至少3点的直线；源数据的共线约定必须一致。相等/共线关系需精确谓词。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/1208.4714)；[来源2](https://oeis.org/A003035)

### T031 · No-three-in-line maximum on an n×n grid

- 类别：几何图与计算几何。
- 问题：Select as many lattice points as possible from [n]×[n] with no three collinear.
- 输出：Grid point list; objective cardinality.
- 单一标量：`number of selected points`；越大越好。统一高分方向 `J`。
- 配置：{"grid_order": "n"}
- 人类基线证据：Dudeney posed the problem; constructions of 2n points are known for many n, but the universal 2n conjecture remains open. Wolfram/House of Graphs style databases list configurations; exact finite maxima are only known for selected small n, so a primary record source must be frozen.
- 验证成本：Low for collinearity checks; optimum proof hard.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Recent preprints and recreational databases may contain construction records without optimality proofs; label upper/lower status carefully.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/2209.01447)

### T032 · Simple perfect squared squares: minimum primitive side at fixed order · MVP

- 类别：铺砌与分割。
- 问题：固定小正方形数量N，将一个整数边长正方形分割为边长互不相同的小正方形，要求simple、所有边长gcd=1，最小化外框边长。
- 输出：Bouwkamp code or exact tile placements
- 单一标量：`primitive outer-square side length`；越小越好。统一高分方向 `-J`。
- 配置：{"N": "固定order，例如21校准、55历史构造轨"}
- 人类基线证据：Duijvestijn (1978)：N21唯一构造primitive side112，已知最优校准。Squaring.net order55页列 Bernard Moss (2020) side740 的历史构造；本次未下载重算。
- 验证成本：Low-medium; exact integer tiling and distinct sizes; global proof is enumeration-based.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：不是把固定目标最低order21当可持续发现任务；须验证Bouwkamp码、simple条件与gcd；side740仅历史baseline。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www.squaring.net/sq/ss/spss/o21/spsso21.html)；[来源2](https://www.squaring.net/sq/ss/spss/o55/spsso55.html)；[来源3](https://www.squaring.net/downloads/downloads.html~)

### T033 · Mrs. Perkins’s quilt

- 类别：铺砌与分割。
- 问题：For fixed n×n square, dissect into the fewest smaller integer-sided squares whose side lengths have gcd 1.
- 输出：integer square tiling / side lengths and positions
- 单一标量：`number of smaller squares`；越小越好。统一高分方向 `-J`。
- 配置：Fix outer side n; integer alignment; tile-side gcd 1
- 人类基线证据：For n=13, the catalogue gives an optimal 11-square dissection with sides 1,1,2,2,2,3,3,4,6,6,7; no fewer than 11 is possible. Squaring.net lists results through n=120, while warning most later rows are best known rather than proven. Conway, Guy, Gay, Pegg and computer searches are documented.
- 验证成本：Low for a proposed tiling/gcd; exact minimality varies by n.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Use proven n=13 calibration; do not claim later best-known values are optimal.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www.squaring.net/sq/ss/quilts/mrs-perkins-quilts.html)；[来源2](https://mathworld.wolfram.com/MrsPerkinssQuilt.html)

### T034 · Klarner order of a polyomino

- 类别：铺砌与分割。
- 问题：For a fixed polyomino P, find the fewest congruent copies (translations, rotations, reflections allowed) that tile any rectangle.
- 输出：rectangle dimensions and copy placements
- 单一标量：`minimum number of copies of P`；越小越好。统一高分方向 `-J`。
- 配置：fixed polyomino shape; allowed orientations stated
- 人类基线证据：polyominoes.org lists P-pentomino order 2 and an explicit 2×5 tiling. The Handbook of Discrete and Computational Geometry defines order and records a Y-pentomino’s 5×10 rectangle (10 copies), with results by Klarner and Reid.
- 验证成本：Low for a placement; proving no smaller order may require exhaustive search.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Shape P is an instance parameter; P-pentomino order 2 is trivial. Use only a nontrivial shape with source-supported minimality.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://polyominoes.org/data/5P)；[来源2](https://www.csun.edu/~ctoth/Handbook/chap14.pdf)；[来源3](https://sicherman.net/mikereid/p5_rect.html)

### T035 · (d,g)-cage order

- 类别：极值图与超图。
- 问题：For fixed degree d and girth g, find the smallest order n of a d-regular graph of girth exactly g.
- 输出：Adjacency list/matrix of a d-regular graph with a verifiable girth certificate; objective is vertex count.
- 单一标量：`number of vertices n`；越小越好。统一高分方向 `-J`。
- 配置：{"degree": "d", "girth": "g"}
- 人类基线证据：Exoo, Jajcay, Goedgebeur et al. (2025 preprint) improved eleven upper bounds; e.g. n(4,10)≤320. Exoo–Jajcay (2013) survey distinguishes known cages from upper-bound constructions; optimality is proved only for some parameter pairs.
- 验证成本：Medium for a supplied graph; high to prove global minimality.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Report incumbent order separately from proven minimum; exact optimality certificates are often absent.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/2511.07247)；[来源2](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS16)

### T036 · Degree–diameter problem

- 类别：极值图与超图。
- 问题：For maximum degree d and diameter k, maximize the order of a simple graph.
- 输出：Graph adjacency list plus proof/check of maximum degree and diameter; objective vertex count.
- 单一标量：`number of vertices n`；越大越好。统一高分方向 `J`。
- 配置：{"maximum_degree": "d", "diameter": "k"}
- 人类基线证据：The large degree/diameter graph table (Miller, Širáň and contributors; updated tables) records best known orders and marks the few proven optimal cases; Moore bound is an upper bound, not an attained baseline.
- 验证成本：Medium for witness; exact optimum usually unknown.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Must label best-known vs proven; table updates and graph conventions (regular vs maximum degree) need freezing.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://doi.org/10.17632/d75dzbjd4k.3)

### T037 · Zarankiewicz number Z_{s,t}(m,n)

- 类别：极值图与超图。
- 问题：固定左右部大小m,n，构造二部图，禁止存在s个左顶点与t个右顶点形成完整二部子图，最大化边数。若同时禁止交换角色的情形，须单列配置。
- 输出：Bipartite adjacency matrix; objective number of 1 entries.
- 单一标量：`number of edges`；越大越好。统一高分方向 `J`。
- 配置：{"part_sizes": "m,n", "forbidden_biclique": "s,t"}
- 人类基线证据：Published exact values and bounds are surveyed in the extremal graph literature; small square cases have SAT-verified tables (Mubayi et al. / 2022 SAT study corrects known table errors). Explicit finite-field constructions give human lower bounds.
- 验证成本：Medium for forbidden biclique and edge count; optimality high.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Older tables contain errors; pin a source version and instance. General asymptotics remain open.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/2203.02283)；[来源2](https://arxiv.org/abs/2202.05507)；[来源3](https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/BGKRSW96/bgkrsw96.pdf)

### T038 · Forbidden-subgraph extremal number ex(n,F) · MVP

- 类别：极值图与超图。
- 问题：固定 n 与有限禁止图族 F，构造 F-free 简单图。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`number of edges`；越大越好。统一高分方向 `J`。
- 配置：{"n": "顶点数", "F": "例如 {C4} 或 {C3,C4}，作为配置"}
- 人类基线证据：Afzaly–McKay 公开 sparse6 构造表：ex(10,C4)=16；禁止 C3,C4 时 n=10 的构造为15条边。较大行区分最优与仅下界。
- 验证成本：低至中；固定小 F 的子图检查。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：高阶 F 或很大 n 会使验证昂贵；Zarankiewicz 的二部限制与此相关，按族分层汇总。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)

### T039 · Graph saturation number sat(n,F)

- 类别：极值图与超图。
- 问题：Minimize edges in an n-vertex F-saturated graph: it is F-free, but adding any missing edge creates F.
- 输出：Graph adjacency list; objective edge count.
- 单一标量：`number of edges`；越小越好。统一高分方向 `-J`。
- 配置：{"vertices": "n", "forbidden_graph": "F"}
- 人类基线证据：Bollobás (1965) initiated the problem; for cliques, classical constructions and recent papers give exact formulas for many ranges. Current papers state the standard definition and bounds.
- 验证成本：Medium for candidate; exact optimum often requires proof.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Newer specific F parameter results must be checked against publication status; easy families have formulaic answers.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/2605.07179)

### T040 · Classical Ramsey number lower-bound construction

- 类别：极值图与超图。
- 问题：For fixed s,t, construct the largest N-vertex graph with neither an s-clique nor an independent t-set, equivalently improve the lower bound R(s,t)≥N+1.
- 输出：Graph adjacency list; independently verify forbidden-clique/independent-set conditions; scalar N.
- 单一标量：`number of vertices N`；越大越好。统一高分方向 `J`。
- 配置：{"s,t": "禁止clique与independent set大小；图Ramsey扩展另作为有关联配置，不重复立项"}
- 人类基线证据：Exoo et al. (1997) catalogued 656 nonisomorphic (5,5,42)-graphs, implying R(5,5)≥43; Radziszowski Dynamic Survey rev. 18 (2026) records 43≤R(5,5)≤46, with the upper bound by Angeltveit–McKay (2024).
- 验证成本：High; exact clique and independence checks scale exponentially, though certificates are finite and reproducible.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：A one-unit increase is meaningful but only if exact validation is performed; do not score heuristic estimates or claim exact Ramsey values from a lower-bound witness.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf)；[来源2](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)；[来源3](https://arxiv.org/abs/2409.15709)

### T041 · Hypergraph Turán number ex_r(n,F)

- 类别：极值图与超图。
- 问题：Maximize edges in an r-uniform n-vertex hypergraph avoiding a fixed forbidden r-graph F.
- 输出：List of r-subsets; objective edge count.
- 单一标量：`number of hyperedges`；越大越好。统一高分方向 `J`。
- 配置：{"uniformity": "r", "vertices": "n", "forbidden_hypergraph": "F"}
- 人类基线证据：Keevash's survey and the Erdős problems archive record open cases and constructions. The 3-uniform K4 problem has Turán's construction at density 5/9, but exact density remains open; finite n entries can have exact/conjectured distinctions.
- 验证成本：High; checking F-freeness is manageable for small n, global optimality is difficult.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Do not blur finite exact values with asymptotic Turán density; choose frozen small n and explicit F.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://people.maths.ox.ac.uk/keevash/papers/turan-survey.pdf)；[来源2](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/ExactHypergraphTuranT3n4.html)

### T042 · Erdős–Rogers function f_{s,t}(n)

- 类别：极值图与超图。
- 问题：固定2≤s<t与n，在n顶点K_t-free图G中，最小化α_s(G)，其中α_s(G)是G中诱导子图不含K_s的最大顶点集大小。s=2时α_2是独立数。
- 输出：图G；有限小规模下由独立精确算法计算α_s，或提交相应可检查证书。
- 单一标量：`α_s(G)=max{|U|:G[U] is K_s-free}`；越小越好。统一高分方向 `-J`。
- 配置：{"vertices": "n", "forbidden_clique": "s", "independent_set_forbidden_size": "t (target alpha < t)"}
- 人类基线证据：Erdős–Rogers introduced the function; extensive probabilistic and explicit bounds are surveyed in recent graph Ramsey literature. Specific finite graph records need source-level validation before use.
- 验证成本：高：内层最大子集问题通常指数复杂；仅限能精确求解的小配置，不进MVP。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：原代理误写为K_s-free图上最大独立数（空图平凡达到n），此处已修为标准Erdős–Rogers最小化问题；须同时验证K_t-free与内层α_s。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf)

### T043 · Minimum triangles at fixed edge count

- 类别：极值图与超图。
- 问题：固定 n,m，输出恰有 m 条边的简单图，使三角形数最少。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`triangle count`；越小越好。统一高分方向 `-J`。
- 配置：{"n": "顶点数", "m": "边数"}
- 人类基线证据：Razborov (2008) 的三角形密度定理及 Lovász–Simonovits 构造提供经典基线；非平凡有限 n,m 的显式构造与可达边数须逐项固定。
- 验证成本：低：精确数三角形。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：渐近最优密度不是每个有限配置的最优值；不得用 asymptotic 数字冒充精确基线。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/46.html)；[来源2](https://people.cs.uchicago.edu/~razborov/files/triangles.pdf)

### T044 · Optimal Golomb ruler length · MVP

- 类别：加法组合与离散构造。
- 问题：For m integer marks, place distinct marks so all positive pairwise differences are distinct and minimize the largest mark.
- 输出：Increasing integer mark list starting at 0; objective final mark.
- 单一标量：`ruler length`；越小越好。统一高分方向 `-J`。
- 配置：{"marks": "m"}
- 人类基线证据：Shearer (1990) exhaustively proved optimal lengths 127,151,177 for m=14,15,16; distributed.net completed proof of optimality through m=28 (2022 records), and CSPLib has the standard benchmark. Distinguish proven optima from larger-m best known rulers.
- 验证成本：Low for ruler; optimality proof high for large m.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Open sizes beyond proven range must be scored as incumbent length, not as proven optimum; preserve provenance and certificate status.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://research.ibm.com/publications/some-new-optimum-golomb-rulers)；[来源2](https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob006/)；[来源3](https://distributed.net/ogr/)

### T045 · Minimum diameter of a B_h set of integers, h≥3

- 类别：加法组合与离散构造。
- 问题：For fixed m and h≥3, choose m integers with all h-term sums (repetition convention fixed) distinct, minimizing the diameter.
- 输出：Sorted integer set; objective maximum minus minimum.
- 单一标量：`diameter`；越小越好。统一高分方向 `-J`。
- 配置：{"set_size": "m", "sum order": "h≥3", "repetitions": "fixed by benchmark"}
- 人类基线证据：Bose–Chowla (1962) give finite-field B_h constructions; modern additive-combinatorics papers provide bounds. The h=2 case is the Golomb/Sidon ruler task and is deliberately excluded here as a duplicate.
- 验证成本：Low for witness; exact optimum difficult.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Must distinguish unordered multisets with repetitions from distinct-element sums and from modular B_h sets; h=2 merges with Golomb rulers.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://doi.org/10.1007/BF02566968)；[来源2](https://arxiv.org/abs/2104.12711)

### T046 · Difference triangle sets

- 类别：加法组合与离散构造。
- 问题：Construct several rows of marks with all within-row positive differences distinct globally; minimize maximum span under fixed row/mark counts.
- 输出：Rows of integer marks; objective maximum row span.
- 单一标量：`maximum span`；越小越好。统一高分方向 `-J`。
- 配置：{"rows": "r", "marks_per_row": "m"}
- 人类基线证据：Published difference-triangle-set constructions and tabu search literature report best-known spans; Golomb rulers are the one-row special case.
- 验证成本：Low for a witness.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Overlaps Golomb ruler at r=1; careful definition variants (all differences vs row-tagged) must be frozen.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://doi.org/10.1016/j.cor.2004.11.002)；[来源2](https://cs.uwaterloo.ca/~vanbeek/Publications/sillito.pdf)

### T047 · Maximum cap set in F_3^n

- 类别：加法组合与离散构造。
- 问题：Find a largest subset of the vector space F_3^n containing no affine line (three distinct points summing to zero).
- 输出：Point list in F_3^n; objective cardinality.
- 单一标量：`number of points`；越大越好。统一高分方向 `J`。
- 配置：{"dimension": "n"}
- 人类基线证据：Pellegrino (1970) proved maximum 20 for n=4. Kleinberg–Sawin–Speyer (2016) gave constructions and Ellenberg–Gijswijt (2017) exponential upper bound; human lower-bound records are published for higher n, with exact values limited.
- 验证成本：Low for witness and no-line property; proving optimality difficult.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Modern record tables may have changed; distinguish exact small dimensions from best-known lower bounds.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://doi.org/10.4007/annals.2017.185.1.8)；[来源2](https://arxiv.org/abs/1605.09223)

### T048 · Largest 3-term-progression-free subset of [n]

- 类别：加法组合与离散构造。
- 问题：Find a largest subset of {1,…,n} containing no nontrivial 3-term arithmetic progression.
- 输出：Integer set; objective cardinality.
- 单一标量：`set cardinality`；越大越好。统一高分方向 `J`。
- 配置：{"interval_length": "n"}
- 人类基线证据：Behrend (1946) gave classical constructions; exact small-n values are known computationally and Roth's theorem gives qualitative upper bounds. Pin exact-value source/version for each n.
- 验证成本：Low for witness, exponential for maximality.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Closely related to cap sets but distinct ambient group; avoid treating parameter variants as different tasks.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://doi.org/10.1073/pnas.32.12.331)

### T049 · Minimum difference basis for [n]

- 类别：加法组合与离散构造。
- 问题：Find a smallest set A of integers such that every integer 1,…,n is a difference of two elements of A.
- 输出：Sorted integer set; objective cardinality (or span if a different canonical version is chosen).
- 单一标量：`number of elements of A`；越小越好。统一高分方向 `-J`。
- 配置：{"target_interval": "n", "ambient_domain": "integer interval, fixed convention"}
- 人类基线证据：Rédei–Rényi and Leech difference-basis constructions; the prior finite witness at n=6166 has128 marks, giving128²/6166≈2.6571. Original128-element list still needs retrieval; not a same-config value for all n.
- 验证成本：Low for coverage; proving minimality difficult.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Several inequivalent definitions (difference set vs difference basis, interval endpoint, signed differences); human baseline source requires additional research.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/7.html)；[来源2](https://arxiv.org/html/2511.02864v1#S6.SS3)

### T050 · Maximum sum-free subset of a finite group

- 类别：加法组合与离散构造。
- 问题：Maximize |A| in a fixed finite abelian group subject to no x,y,z∈A with x+y=z (convention fixed).
- 输出：Element list; objective cardinality.
- 单一标量：`set cardinality`；越大越好。统一高分方向 `J`。
- 配置：{"group": "fixed finite abelian group"}
- 人类基线证据：For integers [n], the maximum is floor((n+1)/2), giving an exact calibration; finite group extremal classifications are known in many cases.
- 验证成本：Low for witness, exact optimum varies.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Integer interval is formulaic; broad finite-group versions need more specific literature and are not one task.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://doi.org/10.3792/pja/1195520891)；[来源2](https://doi.org/10.1112/jlms/s1-44.1.131)

### T051 · Schur number S(k) lower-bound coloring

- 类别：加法组合与离散构造。
- 问题：For fixed k colors, construct a coloring of [N] with no monochromatic x+y=z; maximize N, the certified lower bound for S(k).
- 输出：Color assignment [N]→[k] with exact check of all x+y=z; scalar N.
- 单一标量：`largest colorable N`；越大越好。统一高分方向 `J`。
- 配置：{"colors": "k"}
- 人类基线证据：Heule (AAAI 2018) proved S(5)=160 using a DRAT-certified SAT computation; S(6)≥536 and S(7)≥1680 are cited constructions by Fredricksen–Sweet (2000). Schur numbers S(1..4)=1,4,13,44 are exact.
- 验证成本：Low for lower-bound coloring; proving exact value needs a large SAT/DRAT proof.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Score a coloring's N only, not an exact S(k) claim absent an upper proof; weak Schur numbers are a separate convention and should be excluded/merged only by explicit scope.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://ojs.aaai.org/index.php/AAAI/article/download/12209/12068)；[来源2](https://www.cs.utexas.edu/~marijn/Schur/)

### T052 · van der Waerden number lower-bound coloring

- 类别：加法组合与离散构造。
- 问题：For fixed r colors and AP length k, construct the longest r-coloring of [N] with no monochromatic k-term arithmetic progression.
- 输出：Coloring of [N]; scalar N.
- 单一标量：`largest AP-free coloring order N`；越大越好。统一高分方向 `J`。
- 配置：{"colors": "r", "progression_length": "k"}
- 人类基线证据：Marijn Heule's 2005 EJC survey/paper tables W(2,5)=178, W(2,6)=1132 and many best known lower-bound colorings; Berlekamp (1968) and later recurrence constructions provide explicit records.
- 验证成本：Low for a coloring witness by enumerating arithmetic progressions; upper/exact proof is costly.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Closely related to Ramsey lower-bound construction but a distinct named AP-avoidance family; freeze coloring convention and don't label lower bounds as exact W(r,k).
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)；[来源2](https://arxiv.org/abs/1705.09673)；[来源3](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v18i1p64)

### T053 · Longest finite sequence with discrepancy at most C

- 类别：加法组合与离散构造。
- 问题：For a fixed discrepancy cap C, find the largest prefix length N of a ±1 sequence such that every homogeneous initial segment along every arithmetic progression has absolute sum at most C.
- 输出：Sign sequence of length N; exact scalar N.
- 单一标量：`sequence length N`；越大越好。统一高分方向 `J`。
- 配置：{"discrepancy_cap": "C"}
- 人类基线证据：Konev–Lisitsa (2015) reported a discrepancy-3 sequence of length 127,645, improving 17,000, with inductive construction rules; Tao (2015) proved the infinite Erdős discrepancy conjecture.
- 验证成本：Low for a supplied finite sequence; proving maximality requires exhaustive/combinatorial upper certificates.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：The unbounded infinite theorem itself is not a finite optimization task; freeze exact prefix discrepancy convention and evaluate witness length only.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/1407.2510)；[来源2](https://arxiv.org/abs/1509.05363)

### T054 · Largest square-difference-free subset of [N]

- 类别：加法组合与离散构造。
- 问题：Maximize |A| for A⊂[N] with no distinct a,b∈A such that |a−b| is a perfect square.
- 输出：Integer set; objective cardinality.
- 单一标量：`number of elements`；越大越好。统一高分方向 `J`。
- 配置：{"interval_length": "N"}
- 人类基线证据：Ruzsa (1984) gave an explicit construction of square-difference-free sets; Green–Sawhney (preprint 2024, updated 2025) prove |A|≪N exp(−c√log N). These are asymptotic bounds, not exact finite-N maxima.
- 验证成本：Low for a finite set; proof of maximum difficult.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Asymptotic rather than exact finite record frontier; parameters N give highly correlated instances.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://doi.org/10.1007/BF02454169)；[来源2](https://arxiv.org/abs/2411.17448)

### T055 · Finite-set sum–product growth minimization

- 类别：加法组合与离散构造。
- 问题：固定集合大小m与环境环R（有限域F_p或有坐标界的整数），构造A⊂R、|A|=m，最小化max(|A+A|,|A·A|)。
- 输出：Finite integer set A; objective the larger of sumset/product-set cardinalities.
- 单一标量：`max(|A+A|,|A·A|)`；越小越好。统一高分方向 `-J`。
- 配置：{"m": "集合大小", "R": "F_p及素数p，或整数及坐标上界B"}
- 人类基线证据：Erdős–Szemerédi (1983) established a power-growth theorem for integer sets; later Solymosi and others improve exponents. No canonical exact finite-n construction table for this min-max objective was verified in this pass.
- 验证成本：Low for a finite set and exact integer operations; global optimum hard.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Integer interval bound B affects the problem substantially and may be artificial; no verified human optimum table. Restrict to conditional exploratory instances only.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://annals.math.princeton.edu/2003/157-3/p07)；[来源2](https://arxiv.org/abs/math/0402285)；[来源3](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/45.html)

### T056 · Minimum finite-field Kakeya set size

- 类别：加法组合与离散构造。
- 问题：For fixed finite field F_q and dimension d, minimize |K| over K⊂F_q^d containing a full affine line in every direction.
- 输出：Point list or characteristic function; objective |K|.
- 单一标量：`number of points`；越小越好。统一高分方向 `-J`。
- 配置：{"field_order": "q", "dimension": "d"}
- 人类基线证据：Dvir (2009) proved |K|≥c_d q^d by the polynomial method; explicit constructions are known. An October 2026 exposition reports an exact exhaustive result |K|=13 for F_3^3, but that source is secondary, so require primary-paper confirmation before adopting this numeric record.
- 验证成本：Low for candidate set; exact minimum needs exhaustive or mathematical lower bound.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Small finite cases and field characteristic matter; separate proven minimum from construction upper bound; record 2026 claim as pending primary confirmation.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/0803.2336)；[来源2](https://arxiv.org/abs/1503.06639)

### T057 · Sum–difference I: normalized logarithmic ratio · MVP

- 类别：加法组合与离散构造。
- 问题：输出至少两个不同整数组成的集合 A；计算其和集与差集。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`log(|A+A|/|A|)/log(|A-A|/|A|)`；越大越好。统一高分方向 `J`。
- 配置：{"cardinality": "固定上限，如512；不是把固定17元素改作上限512", "integer_range": "如[-10^6,10^6]"}
- 人类基线证据：Pigarev–Freiman 的17元构造在 Martin–O'Bryant (2006/2007) 中重列；|A+A|=59、|A-A|=55，score=1.0597930945472454；本次已独立重算。
- 验证成本：低：O(|A|²) 整数集合运算。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：该历史人类构造不是2026世界纪录；与II/III分母不同。新的含AI论文另列。
- 研究状态：example_witness_recomputed_not_full_task_audit；当前仅为候选。
- 来源：[来源1](https://personal.math.ubc.ca/~gerg/papers/downloads/MSHMSTD.pdf)；[来源2](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/42.html)

### T058 · Sum–difference II: unnormalized logarithmic ratio

- 类别：加法组合与离散构造。
- 问题：输出有限整数集 A，优化差集大小相对和集大小的指数。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`log(|A-A|)/log(|A+A|)`；越大越好。统一高分方向 `J`。
- 配置：{"size_bound": "有限大小/坐标界需固定"}
- 人类基线证据：人类高维非负整数 simplex 构造给出渐近指数 log(1+sqrt(2))/log(2)≈1.27155；明确有限维实例须用足够大的进制嵌入整数并精确计分。
- 验证成本：低至中：有限输出时计和集差集。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：渐近常数不是任意有限配置的可达baseline；有限实例尚待固定。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/43.html)；[来源2](https://arxiv.org/html/2511.02864v1#S6.SS25)

### T059 · Sum–difference III: finite certificate for asymptotic exponent

- 类别：加法组合与离散构造。
- 问题：输出含0的非负整数集 U，满足 Gyarmati–Hennecart–Ruzsa 有限证书定理的条件，用其证明渐近指数下界。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`1+log(|U-U|/|U+U|)/log(2 max(U)+1)`；越大越好。统一高分方向 `J`。
- 配置：{"integer_bound": "max U 上限", "size_bound": "显式输出规模上限"}
- 人类基线证据：Gyarmati–Hennecart–Ruzsa (2007)：U={0,1,3,6,13,17,21}，和集26、差集39、q=43，score=1.107802056693651；本次已重算有限表达式。
- 验证成本：低：整数集合运算。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：必须验证原证书条件（严格 |U-U|<2maxU+1 等）；后续1.14465等大构造不可直接当小配置baseline。
- 研究状态：example_witness_recomputed_not_full_task_audit；当前仅为候选。
- 来源：[来源1](https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf)；[来源2](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/44.html)

### T060 · Covering number C(v,k,t) · MVP

- 类别：组合设计。
- 问题：Find the fewest k-subsets of a v-set such that every t-subset is included in at least one selected block.
- 输出：List of k-subsets; objective block count.
- 单一标量：`number of blocks`；越小越好。统一高分方向 `-J`。
- 配置：{"v": "points", "k": "block size", "t": "covering strength"}
- 人类基线证据：La Jolla Combinatorics Repository (Dan Gordon; frozen 2026) stores tens of thousands of best-known covers and lower bounds; individual construction records identify contributors/methods.
- 验证成本：Low-medium for coverage; proving minimum needs lower bound.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Repository baseline may be best-known rather than optimum; freeze data snapshot and preserve authorship metadata.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://dmgordon.org/ljcr/)；[来源2](https://ljcr.dmgordon.org/cover.html)

### T061 · Covering array CAN(t,k,v) · MVP

- 类别：组合设计。
- 问题：Minimize rows N of a k-column v-ary array so every t selected columns contain every v^t tuple at least once.
- 输出：N×k array over v symbols; objective N.
- 单一标量：`number of rows N`；越小越好。统一高分方向 `-J`。
- 配置：{"strength": "t", "columns": "k", "levels": "v"}
- 人类基线证据：NIST Covering Array Library lists actual arrays for strengths 2–6 and 2–6 levels, plus best-known sizes to 20,000 columns (strength 2) and 10,000 (strengths 3–6); NIST and Colbourn records are human constructions/bounds.
- 验证成本：Low for explicit array; minimum proof varies.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Keep uniform alphabet case separate from variable-strength/general mixed-level variants; NIST best-known size tables do not always include arrays.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://csrc.nist.gov/Projects/Automated-Combinatorial-Testing-for-Software/Covering-Array-Library)；[来源2](https://math.nist.gov/coveringarrays/coveringarray.html)

### T062 · Orthogonal array minimum-run construction

- 类别：组合设计。
- 问题：For fixed strength t, levels and columns, construct an orthogonal array with the fewest rows (or maximize columns for fixed rows), each t-column tuple appearing equally often.
- 输出：Array with explicit index lambda; objective rows or columns, with one direction fixed per instance.
- 单一标量：`number of rows N; λ=N/q^t is variable`；越小越好。统一高分方向 `-J`。
- 配置：{"t": "强度", "q": "字母表大小", "k": "列数；index λ不固定，随行数N优化"}
- 人类基线证据：Neil Sloane's library contains 200+ explicit arrays; Eendebak–Schoen catalogue complete non-isomorphic arrays for selected small parameters. OA( N,k,s,t) must meet divisibility/Rao bounds.
- 验证成本：Low for explicit array; minimality moderate/high.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Do not conflate OA existence, maximum columns, and minimum-run objectives; fix one scalar per instance. Strength-2 binary OAs are essentially Hadamard matrices.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://neilsloane.com/oadir/index.html)

### T063 · Packing number D(v,k,t)

- 类别：组合设计。
- 问题：Maximize the number of k-subsets on v points such that no t-subset is contained in more than one block.
- 输出：List of blocks; objective block count.
- 单一标量：`number of blocks`；越大越好。统一高分方向 `J`。
- 配置：{"v": "points", "k": "block size", "t": "packing strength"}
- 人类基线证据：La Jolla covering repository focuses on coverings, while classical packing bounds and constructions are published; candidate instance-level records require dedicated database/source review.
- 验证成本：Low for packing property.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：No unified current record table confirmed in this pass; may overlap partial Steiner designs.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://dmgordon.org/ljcr/)

### T064 · Social golfer maximum schedule length

- 类别：组合设计。
- 问题：Partition players into groups of fixed size each round, avoiding any pair meeting twice; maximize number of rounds.
- 输出：Round-by-round partitions; objective number of rounds.
- 单一标量：`number of rounds`；越大越好。统一高分方向 `J`。
- 配置：{"players": "P", "group_size": "g", "groups_per_round": "fixed/implied"}
- 人类基线证据：CSPLib problem 010 defines the canonical 32 golfers in groups of four and its generalization; published constraint-programming literature reports solved/optimal schedules for small parameter sets, but benchmark records need per-instance capture.
- 验证成本：Low for pair uniqueness; maximality requires a bound/proof.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Could degenerate into mere feasibility when target rounds fixed; use maximize rounds and instances with documented human optima.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob010/)；[来源2](https://www.csplib.org/Problems/prob010/)

### T065 · Maximum number of mutually orthogonal Latin squares

- 类别：组合设计。
- 问题：For order n, maximize the number of pairwise orthogonal Latin squares (MOLS).
- 输出：List of Latin squares; objective count.
- 单一标量：`number of MOLS`；越大越好。统一高分方向 `J`。
- 配置：{"order": "n"}
- 人类基线证据：Bruck–Ryser–Chowla gives nonexistence restrictions; complete values are known for several small orders, while the standard MOLS tables record constructions and bounds.
- 验证成本：Low for square/orthogonality checks; maximality often hard.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Exact optimum open for some n; source table version and proof status must be frozen.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://doi.org/10.1016/0012-365X(74)90148-4)；[来源2](https://www.dcs.gla.ac.uk/~pat/cpM/jchoco/latinSquares/papers/10%5B1%5D.1.1.49.7739.pdf)

### T066 · Best minimum distance of linear codes · MVP

- 类别：编码理论。
- 问题：For fixed (n,k,q), construct a q-ary linear [n,k] code with maximum minimum Hamming distance d.
- 输出：Generator matrix over GF(q), with independently checked rank and minimum distance.
- 单一标量：`Minimum Hamming distance d(C)`；越大越好。统一高分方向 `J`。
- 配置：{"n": "block length", "k": "dimension", "q": "finite-field order; use distinct benchmark rows, not one task per q/n"}
- 人类基线证据：Human-computed database: Markus Grassl, John Cannon and Greg White's Magma BKLC tables; Magma reports 33,152 best-known binary codes, all binary entries through n=31 optimal. Row-wise d and construction need retrieval from the database. This is historical human computation, not AI.
- 验证成本：Medium for small k (enumerate q^k codewords); high beyond that. Restrict benchmark to enumerable dimensions or certificate-backed distance.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Minimum-distance inner enumeration grows exponentially; restrict k (and n) and verify row construction. Database values are best-known, not all proven optimal. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html)；[来源2](https://codetables.de/)

### T067 · Maximum size of a binary code A(n,d)

- 类别：编码理论。
- 问题：Construct a subset C of {0,1}^n with pairwise Hamming distance at least d and maximum cardinality.
- 输出：List of binary words; verify distinctness and pairwise distances.
- 单一标量：`|C|`；越大越好。统一高分方向 `J`。
- 配置：{"n": "block length", "d": "minimum distance"}
- 人类基线证据：A. E. Brouwer's classical tables and ongoing bounds; specific construction/value must be fixed per row. Human literature/database; no AI baseline assumed.
- 验证成本：O(|C|^2 n) for lower-bound witness; proving optimality substantially harder.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Many instances have only bounds, not exact optimum; select a published construction row and compare witness cardinality, not claim optimality.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://aeb.win.tue.nl/codes/binary.html)

### T068 · Constant-weight code A(n,d,w)

- 类别：编码理论。
- 问题：Find a largest family of w-subsets of an n-set with pairwise symmetric difference at least d.
- 输出：List of w-subsets/bitmasks; verify all weights and pairwise Hamming distances.
- 单一标量：`Code size |C|`；越大越好。统一高分方向 `J`。
- 配置：{"n": "ambient length", "d": "minimum Hamming distance", "w": "constant word weight"}
- 人类基线证据：Brouwer, Shearer, Sloane and Smith (1990) compiled bounds; many later explicit constructions and improved bounds. Pin row and construction before benchmark inclusion; human baseline, no AI assumed.
- 验证成本：Low/medium: O(|C|^2 n), often under a second for small instances.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Do not confuse lower-bound construction with known optimum; duplicate of general nonlinear code only if constant-weight constraint is not central. Fixed rows needed. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://aeb.win.tue.nl/codes/Andw.html)

### T069 · Constant-dimension subspace code A_q(n,d;k)

- 类别：编码理论。
- 问题：Find the largest set of k-dimensional subspaces of GF(q)^n with pairwise subspace distance at least d.
- 输出：Basis matrices/RREFs for subspaces; exact rank/intersection verification.
- 单一标量：`Code size |C|`；越大越好。统一高分方向 `J`。
- 配置：{"q": "field order", "n": "ambient dimension", "k": "subspace dimension", "d": "minimum subspace distance"}
- 人类基线证据：Heinlein, Kiermaier, Kurz and Wassermann (2016, updated 2019) maintain Tables of Subspace Codes; the paper explicitly describes best lower/upper bounds and constructions. Fix an exact table row for score/construction.
- 验证成本：Medium: pairwise intersection ranks O(|C|^2 n^3) with finite-field linear algebra.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Many rows are intervals rather than exact optima; select modest dimensions and public construction records. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/1601.02864)；[来源2](https://subspacecodes.uni-bayreuth.de/)

### T070 · Covering code size

- 类别：编码理论。
- 问题：For fixed binary length n and covering radius R, construct a smallest set C whose radius-R Hamming balls cover the whole cube.
- 输出：List of codewords; verify full coverage by exhaustive enumeration for small n.
- 单一标量：`Code size |C|`；越小越好。统一高分方向 `-J`。
- 配置：{"n": "length", "R": "covering radius"}
- 人类基线证据：Cohen, Honkala, Litsyn and Lobstein (1997) survey and tabulate covering codes; select a small open/nontrivial instance and recover explicit construction.
- 验证成本：Low for small n (2^n point coverage), exponential and unsuitable for large n.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Inner covering check scales exponentially; exact optimum often unknown. Only small finite instances qualify.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://neilsloane.com/doc/CR.html)

### T071 · Maximum permutation code size

- 类别：编码理论。
- 问题：固定 n,d，输出 S_n 的子集，使任意两排列的 Hamming 距离至少 d。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`number of codewords`；越大越好。统一高分方向 `J`。
- 配置：{"n": "排列阶数", "d": "最小Hamming距离"}
- 人类基线证据：Bereg et al. (2019) Partition and Extension 给出显式人类构造与数值表；Ding–Fu–Kløve–Wei (2002)、Gao et al. (2008) 等经典构造可复现。需固定具体表格行。
- 验证成本：低至中 O(M²n)。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：大群的生成元不是自动可快速验证的完整码；初期只接受显式小码。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/1804.08252)；[来源2](https://arxiv.org/abs/0801.3987)

### T072 · Maximum deletion-correcting code size

- 类别：编码理论。
- 问题：固定 q,n,t，输出 q 元长度 n 的码，任意不同码字的 t-deletion balls 不相交。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`number of codewords`；越大越好。统一高分方向 `J`。
- 配置：{"q": "字母表大小", "n": "码长", "t": "可纠正删除数"}
- 人类基线证据：Varshamov–Tenengolts (1965) / Levenshtein (1966) 的二元单删除码有明确同余公式；按给定 n 枚举其码字可以得到可重算历史人类baseline。
- 验证成本：中：每码字枚举删除结果或两两 LCS；规模受限。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：VT明确同余构造见Sloane (2002)原稿；固定n后枚举得到人类基线，不能将其当全部有限n都已证最优。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/math/0207197)；[来源2](https://neilsloane.com/doc/dijen.pdf)

### T073 · LABS minimum aperiodic autocorrelation energy · MVP

- 类别：序列与平坦多项式。
- 问题：For s_i in {±1}, length L, minimize E=Σ_{k=1}^{L−1}(Σ_{i=1}^{L−k}s_i s_{i+k})².
- 输出：Binary sign sequence.
- 单一标量：`E (equivalently merit factor L²/(2E))`；越小越好。统一高分方向 `-J`。
- 配置：{"L": "sequence length; select fixed rows, do not count lengths as separate task families"}
- 人类基线证据：Packebusch–Mertens (2015/2016) exact optima for lengths<=66 in the cited paper; Militzer author page has explicit historical evolutionary sequences. Do not describe historical records as latest.
- 验证成本：Low: O(L²) integer arithmetic.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Energy and merit factor are strictly monotone transforms for fixed L, so they are the same task and must not be counted twice. Best known versus proven optimum must be labeled.
- 研究状态：example_witness_recomputed_not_full_task_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/1512.02475)；[来源2](https://militzer.berkeley.edu/sequences.html)

### T074 · LABS peak sidelobe level (PSL)

- 类别：序列与平坦多项式。
- 问题：For binary sign sequence s of length L, minimize max_{1≤k<L}|Σ_{i=1}^{L−k}s_i s_{i+k}|.
- 输出：Binary sign sequence.
- 单一标量：`PSL=max absolute nonzero aperiodic autocorrelation`；越小越好。统一高分方向 `-J`。
- 配置：{"L": "sequence length"}
- 人类基线证据：Dmitriev and Jedwab (2005) studied typical PSL; later Best-Known Peak Sidelobe Level Values (2021) reports constructed sequences and search results. Retrieve row-specific construction before instantiation.
- 验证成本：Low O(L²).
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：PSL optima can conflict with LABS energy; do not present as interchangeable with merit factor. Current row baseline needed.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www.sfu.ca/~jed/Research/PSL.html)；[来源2](https://arxiv.org/abs/1212.4930)；[来源3](https://arxiv.org/abs/2104.10477)

### T075 · Periodic binary autocorrelation energy

- 类别：序列与平坦多项式。
- 问题：For s∈{±1}^L, minimize the sum of squares of nonzero periodic autocorrelations C(k)=Σ_i s_i s_{i+k mod L}.
- 输出：Binary sign sequence.
- 单一标量：`Σ_{k=1}^{L−1} C(k)^2`；越小越好。统一高分方向 `-J`。
- 配置：{"L": "period length"}
- 人类基线证据：经典Legendre/Paley周期序列，以及Yan–Chen–Li (2014)、Yan–Gong (2014)等显式构造。p≡3(mod4)的Legendre符号序列（0项设1）给每个非零周期自相关−1，可作为已解校准：能量p−1、PSL1。非已解长度须另选行级人类构造。
- 验证成本：Low O(L²).
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Be precise about periodic versus aperiodic correlation and normalization; known perfect sequences may make selected cases trivial.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/1401.2530)；[来源2](https://arxiv.org/abs/1411.4340)；[来源3](https://doi.org/10.1016/j.tcs.2009.02.021)

### T076 · Binary sequence maximum out-of-phase autocorrelation (periodic merit)

- 类别：序列与平坦多项式。
- 问题：For fixed length L, construct a binary sequence minimizing the maximum absolute nonzero periodic autocorrelation.
- 输出：Binary sign sequence.
- 单一标量：`max_{k≠0}|Σ_i s_i s_{i+k mod L}|`；越小越好。统一高分方向 `-J`。
- 配置：{"L": "period length"}
- 人类基线证据：经典Legendre/Paley周期序列，以及Yan–Chen–Li (2014)、Yan–Gong (2014)等显式构造。p≡3(mod4)的Legendre符号序列（0项设1）给每个非零周期自相关−1，可作为已解校准：能量p−1、PSL1。非已解长度须另选行级人类构造。
- 验证成本：Low O(L²).
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Related but distinct from aperiodic PSL; ensure periodic definition and cited baseline align exactly.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/1401.2530)；[来源2](https://arxiv.org/abs/1411.4340)；[来源3](https://doi.org/10.1016/j.tcs.2009.02.021)

### T077 · Littlewood polynomials: minimum supremum modulus

- 类别：序列与平坦多项式。
- 问题：输出长度 L 的±1系数多项式 P，最小化整个单位圆上的归一化最大模。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`max_{|z|=1}|P(z)|/sqrt(L)`；越小越好。统一高分方向 `-J`。
- 配置：{"L": "系数个数"}
- 人类基线证据：Rudin–Shapiro 递推给出人类显式多项式和上界 sqrt(2)（L为2的幂）；Odlyzko (2018) 对有限长度做过大量数值搜索。记录数值需全域认证。
- 验证成本：中至高：三角多项式全域极值；不是只采样。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：核实第二来源与所用构造定义；文献中的网格最优不是严格全域最优。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html)；[来源2](https://arxiv.org/abs/1907.09464)

### T078 · Littlewood polynomials: maximum infimum modulus

- 类别：序列与平坦多项式。
- 问题：输出长度 L 的±1系数多项式 P，最大化整个单位圆上的归一化最小模。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`min_{|z|=1}|P(z)|/sqrt(L)`；越大越好。统一高分方向 `J`。
- 配置：{"L": "系数个数；注意奇偶造成的单位根"}
- 人类基线证据：Littlewood 的平坦多项式问题、Odlyzko (2018) 数值构造、Balister et al. 的 Flat Littlewood Polynomials 提供人类基线来源；具体 L 的系数和严格最小模尚须定位。
- 验证成本：中至高：全域下界证书。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：并非最小sup的单调改写；当前只有文献入口，不能宣称有限实例humanbaseline已齐。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html)；[来源2](https://arxiv.org/abs/1907.09464)

### T079 · First Autocorrelation Inequality (AC1) · MVP

- 类别：极值分析。
- 问题：Find nonnegative integrable f supported on [-1/4,1/4], integral 1, minimizing max_{t in [-1/2,1/2]} (f*f)(t).
- 输出：Exact piecewise-polynomial or rational step function with proof of support, positivity and unit mass.
- 单一标量：`Phi1=max_t(f*f)(t)`；越小越好。统一高分方向 `-J`。
- 配置：{"support": "fixed [-1/4,1/4]", "representation": "piecewise polynomial degree and breakpoints; configure separately"}
- 人类基线证据：SimpleTES (2026 paper table 11 reports human 1.509730; AI-assisted results separate: AlphaEvolve 1.505300; SimpleTES 1.503871). Human attribution cites prior sources [15,82,147], which should be independently checked before benchmark release.
- 验证成本：Medium/high: exact convolution per polynomial segment, certify global maximum via roots/interval arithmetic.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Sampling the continuum maximum is not a proof; enforce exact mass and nonnegativity. Human baseline provenance needs citation-level audit.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/0907.1379)；[来源2](https://math.bme.hu/~matolcsi/sch0914.pdf)；[来源3](https://arxiv.org/abs/2604.19341)

### T080 · Second Autocorrelation Inequality (AC2) · MVP

- 类别：极值分析。
- 问题：Find nonnegative integrable f supported on [-1/4,1/4], integral 1, maximizing ||f*f||_2^2/(||f*f||_1 ||f*f||_infinity).
- 输出：Exact piecewise-polynomial or rational step function with proof of support, positivity and unit mass.
- 单一标量：`Phi2=||f*f||_2^2/(||f*f||_1||f*f||_infinity)`；越大越好。统一高分方向 `J`。
- 配置：{"support": "fixed [-1/4,1/4]", "representation": "piecewise polynomial degree and breakpoints; configure separately"}
- 人类基线证据：SimpleTES (2026 table 11) reports best human 0.901500; AI-assisted: AlphaEvolve V2 0.961000; SimpleTES 0.962694.
- 验证成本：High: exact convolution and certified L2/L1/L-infinity evaluation; maximum requires root isolation/interval methods.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：A sampled supremum gives unsound scores; human record citation chain needs audit. Objective's denominator conventions must be fixed.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/0907.1379)；[来源2](https://math.bme.hu/~matolcsi/sch0914.pdf)；[来源3](https://arxiv.org/abs/2604.19341)

### T081 · Third Autocorrelation Inequality (AC3) · MVP

- 类别：极值分析。
- 问题：Find real integrable f supported on [-1/4,1/4], integral 1, minimizing max_t |(f*f)(t)| over [-1/2,1/2].
- 输出：Exact piecewise-polynomial or rational step function, with exact integral and certified global supremum.
- 单一标量：`Phi3=max_t |(f*f)(t)|`；越小越好。统一高分方向 `-J`。
- 配置：{"support": "fixed [-1/4,1/4]", "representation": "piecewise polynomial degree and breakpoints; configure separately"}
- 人类基线证据：SimpleTES (2026 table 11) reports best human 1.458100; AI-assisted results include AlphaEvolve 1.455700 and SimpleTES 1.453675. Paper flags some AI comparisons as using a corrected verifier.
- 验证成本：High: exact convolution; certify absolute maximum by polynomial critical-point isolation or interval arithmetic.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Continuum maximum cannot be sampled; verifier versions differed in prior AI comparisons; audit human sources.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/0907.1379)；[来源2](https://math.bme.hu/~matolcsi/sch0914.pdf)；[来源3](https://arxiv.org/abs/2604.19341)

### T082 · Erdős Minimum Overlap · MVP

- 类别：极值分析。
- 问题：Let f:[0,2]→[0,1] be a step function with ∫_0^2 f(x)dx=1. Define g(x)=1−f(x) for x∈[0,2] and g(x)=0 outside [0,2]. Minimize Ψ(f)=sup_{t∈R} ∫_R f(x)g(x+t)dx = sup_{t∈R} ∫_[0,2]∩[-t,2-t] f(x)(1−f(x+t))dx. Both f and g are zero outside [0,2]; this is essential. Include both shift directions and do not use finite M(N) as the same score.
- 输出：Exact rational step function with breakpoints and values, exact mass, and a rigorous maximization over all shifts s (piecewise polynomial plus root isolation/interval arithmetic).
- 单一标量：`Ψ(f)=sup_{t∈R}∫_R f(x)g(x+t)dx, where f,g are supported on [0,2] and g=1−f on [0,2] (lower is better). Equivalent to the intersection-range integral; both positive and negative shifts are included.`；越小越好。统一高分方向 `-J`。
- 配置：{"step_count": "number of equal-width intervals on [0,2] (e.g. 15 or 51); representation setting, not a separate task"}
- 人类基线证据：Haugland (2016) reports human step-function upper-bound witnesses for this continuous normalized objective: 15 steps gives 0.38153155 (rounded upward); 51 steps gives 0.3809268534330870. These are reported construction scores, not independently reproduced here. AI-assisted results are separate.
- 验证成本：Finite exact task low/medium; limiting witness high (integral/profile derivation and rigorous discretization error certificate).
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Both f and its complement g must be supported on [0,2], with g=1−f only inside [0,2] and zero outside. If 1−f is incorrectly zero-extended as a function equal to 1 outside, endpoint shifts spuriously score 1. Use sup over all real t, equivalently include both positive and negative shifts; a nonsymmetric candidate cannot be scored using only one shift direction. Certify the piecewise functional over every shift interval, not on a grid. The finite partition M(N)/N is related but not the same candidate score.
- 研究状态：example_witness_recomputed_not_full_task_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/1609.08000)；[来源2](https://arxiv.org/abs/2201.05704)

### T083 · Autocorrelation lower envelope for difference bases

- 类别：极值分析。
- 问题：构造可积函数 f，最大化位移 t∈[0,1] 上自相关的最小值，经L1质量归一化。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`min_{0<=t<=1} ∫f(x)f(x+t)dx / ||f||_1²`；越大越好。统一高分方向 `J`。
- 配置：{"representation": "支持区间、分段复杂度需固定；不能改变位移区间的尺度后混比"}
- 人类基线证据：Barnard–Steinerberger 文献给出历史构造下界0.37（带边界修正的arcsine分布）；具体有界阶梯函数与0.37的适用参数待核。
- 验证成本：中至高：全位移区间的下包络认证。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：奇异函数、边界点及积分容错曾导致原系统虚高得分，初期不选。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/6.html)；[来源2](https://arxiv.org/html/2511.02864v1#S6.SS2)

### T084 · Sign uncertainty principle (Fourier sign changes)

- 类别：极值分析。
- 问题：For even real f∈L1(R), define A(f)=inf{r>0:f(x)≥0 for |x|≥r}; with f(0), fhat(0)<0, seek constructions making A(f)A(fhat) small, hence an upper bound on the best universal constant C in A(f)A(fhat)≥C.
- 输出：Explicit even real function with a rigorous Fourier transform/sign certificate and certified sign-change radii; use compactly supported piecewise-polynomial or Gaussian-polynomial forms with analytic transforms.
- 单一标量：`A(f)A(fhat), which is an upper bound on the sharp constant C`；越小越好。统一高分方向 `-J`。
- 配置：{"Fourier_convention": "fix once", "function_family": "certifiable analytic family; degree/support settings are representation parameters"}
- 人类基线证据：Gonçalves, Oliveira e Silva and Steinerberger (2016): upper bound 0.353 and lower bound 0.2025. Cohn and Gonçalves (2017): upper bound 0.32831. Georgiev et al. (2025) AlphaEvolve-assisted construction: 0.321591. Cohn–de Laat–Gonçalves announced unpublished 0.3102 in 2025; distinguish this human result from AI-assisted AlphaEvolve.
- 验证成本：High: certify signs of f and Fourier transform on unbounded domains, plus exact/rigorous threshold radii.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：A finite sample grid cannot certify eventual sign. Human 0.3102 is reported as unpublished in the AlphaEvolve problem page; use the published 0.32831 as baseline unless the unpublished artifact is publicly reproducible.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/11.html)；[来源2](https://arxiv.org/abs/1712.04438)

### T085 · Cohn–Elkies linear-programming bound for sphere packing

- 类别：极值分析。
- 问题：For a fixed dimension d, construct an admissible radial function f with f(0)>0, Fourier transform nonnegative and f(x)≤0 outside a specified radius, minimizing the normalized Cohn–Elkies upper bound on packing density.
- 输出：Exact polynomial-times-Gaussian or rigorously certified radial function with Fourier positivity and sign constraints, plus computed bound.
- 单一标量：`Normalized linear-programming upper bound C(d)`；越小越好。统一高分方向 `-J`。
- 配置：{"d": "Euclidean dimension", "function_family": "radial basis / polynomial-Gaussian representation; exact certificate settings separate"}
- 人类基线证据：Cohn and Elkies (2003) introduced the LP bound; Viazovska (2017) proved its sharpness for E8, and Cohn, Kumar, Miller, Radchenko and Viazovska (2017) for Leech lattice dimension 24. For other dimensions, use published human LP bounds; choose an explicit row before acceptance.
- 验证成本：High: global Fourier positivity and sign verification on continuous domains; interval/analytic certificates required.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Do not score sampled radial values. Dimensions 8 and 24 have solved packing optima; select open dimensions and compare only a certified bound.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/13.html)；[来源2](https://arxiv.org/abs/math/0110009)；[来源3](https://arxiv.org/abs/1603.04246)；[来源4](https://arxiv.org/abs/1603.06518)

### T086 · General one-dimensional Gagliardo–Nirenberg sharp constant

- 类别：极值分析。
- 问题：For fixed admissible (j,p,q,r,m,θ), maximize ||D^j u||_p/(||D^m u||_r^θ ||u||_q^(1−θ)) over nonzero test functions u on R, with the scale relation in the AlphaEvolve problem statement.
- 输出：Explicit analytic or piecewise-polynomial function with rigorous norm and derivative-integral evaluation; certificate for a lower bound on C.
- 单一标量：`||D^j u||_p / (||D^m u||_r^θ ||u||_q^(1−θ)) for the submitted u`；越大越好。统一高分方向 `J`。
- 配置：{"j": "derivative order", "m": "higher derivative order", "p,q,r,theta": "admissible exponents; select one fixed row"}
- 人类基线证据：Classical Gagliardo (1958) and Nirenberg (1959) inequalities establish finiteness for the stated admissible regime. The AlphaEvolve paper states that the tested constants are known theoretically; it supplies the explicit solved special case aa49 but does not identify a single general-parameter human score. A fixed row and its sharp-constant reference remain待核实.
- 验证成本：High: improper integrals and derivative norms require certified tails; upper-bound proof of the sharp constant is harder than a witness score.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：General family is too broad as written; configure a single parameter tuple and distinguish a rigorous lower-bound witness from the unknown sharp constant.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/15.html)；[来源2](https://arxiv.org/abs/2511.02864)

### T087 · Rudin spherical harmonic Lp extremizer

- 类别：极值分析。
- 问题：For fixed d≥2, degree D and p∈{4,∞}, maximize ||u||_Lp(S^d)/||u||_L2(S^d) over real degree-D spherical harmonics, with sphere measure normalized to one.
- 输出：Harmonic coefficient vector in an exact orthonormal basis; certify norm ratio, using exact polynomial integration for p=4 or global optimization on sphere for p=∞.
- 单一标量：`||u||_p/||u||_2 for the submitted spherical harmonic`；越大越好。统一高分方向 `J`。
- 配置：{"d": "sphere dimension", "D": "harmonic degree", "p": "4 or infinity"}
- 人类基线证据：AlphaEvolve repository problem 57 and Georgiev et al. (2025) identify the finite-dimensional extremal problem, but the exact row-level human record/value was not retrieved in this pass; mark score待核实 before inclusion.
- 验证成本：Medium for p=4 (finite algebraic integral); high for p=∞ (continuous sphere supremum).
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Need a published human construction/value for a specific (d,D,p); continuum maximization for p=∞ cannot be sampled as proof.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/57.html)；[来源2](https://arxiv.org/abs/2511.02864)

### T088 · Ovals curvature Schrödinger eigenvalue

- 类别：极值分析。
- 问题：Minimize the lowest periodic eigenvalue λ0 of Hγ=−d²/ds²+κ(s)² over simple closed convex plane curves of length 2π.
- 输出：Certified convex curve (e.g. rational Fourier curvature/tangent data satisfying closure and total turning) and rigorous eigenvalue upper bound; lower-bound claims need proof.
- 单一标量：`λ0(Hγ)`；越小越好。统一高分方向 `-J`。
- 配置：{"length": "fixed 2π", "curve_representation": "Fourier coefficients/breakpoints and exact closure constraints"}
- 人类基线证据：Benguria and Loss (2004) identified the circle/equality family with value 1, giving C≤1; Linde's 2015 work gives a global lower bound C>0.81 and numerical evaluation C>0.8246 (as summarized in later research). AlphaEvolve (2025) recovered the circle but not the noncircular equality family. Human constructions are explicit.
- 验证成本：High: certify convexity/closure and periodic Schrödinger ground-state eigenvalue; use validated spectral bounds.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Circle immediately attains the known upper value 1; to create a useful benchmark, target a different construction such as recovery of noncircular equality family, but that is structural and not a scalar improvement.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/19.html)；[来源2](https://doi.org/10.1007/s00023-004-0186-8)；[来源3](https://arxiv.org/abs/2511.02864)

### T089 · Maximum determinant of sign matrices · MVP

- 类别：矩阵、格与代数极值。
- 问题：Find A in {−1,+1}^{29x29} maximizing |det A|.
- 输出：29x29 sign matrix; exact determinant certificate; optionally a proving upper-bound certificate if optimality is claimed.
- 单一标量：`|det A| (equivalently the normalized determinant in the cited benchmark)`；越大越好。统一高分方向 `J`。
- 配置：{"n": "阶数；原论文实例29，新配置例如31"}
- 人类基线证据：Orrick and Solomon's classical record, as reported by Ye et al. (2026): |det|=320·7^12·2^28 (normalized 0.935673). SimpleTES recovers it; this is AI-assisted and is not the human baseline.
- 验证成本：Low: Bareiss exact determinant; optimality verification is separate and harder.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Do not score only existence of Hadamard; exact determinant is the natural scalar. Published value is a best-known lower bound, not necessarily proved global maximum.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://maths-people.anu.edu.au/~brent/maxdet/order29/)；[来源2](https://arxiv.org/abs/math/0304410)

### T090 · Minkowski lattice packing density

- 类别：矩阵、格与代数极值。
- 问题：For a fixed dimension and specified lattice class, construct a lattice packing maximizing sphere-packing density.
- 输出：Basis matrix plus rigorous determinant/minimum-vector-length certificate.
- 单一标量：`Packing density (equivalently inverse covolume at fixed minimum distance)`；越大越好。统一高分方向 `J`。
- 配置：{"dimension": "d", "lattice_class": "all lattices or specified symmetry"}
- 人类基线证据：Minkowski (1896) introduced the problem; human constructions include root lattices, with exact densest lattice results known in some low dimensions (e.g. dimension 8 and 24 via Viazovska and collaborators for all packings). Row-specific lattice optima vary.
- 验证成本：High: shortest-vector and determinant certification; dimension-dependent.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：May be closed in famous dimensions or difficult to verify in open dimensions; source domain is geometric construction, suitable only with exact finite certificates.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/)；[来源2](https://arxiv.org/abs/1603.04246)；[来源3](https://arxiv.org/abs/1603.06518)

### T091 · Sendov extremal critical-point distance

- 类别：矩阵、格与代数极值。
- 问题：For fixed degree n, maximize over degree-n complex polynomials with all roots in the unit disk the quantity max_k min_j |z_k−w_j|, where z_k are roots and w_j roots of f′; this is the sharp constant C(n).
- 输出：Polynomial coefficients or roots, with certified root/critical-point distances; provide exact algebraic or interval-certified roots.
- 单一标量：`max_k min_j |z_k−w_j| for the submitted polynomial`；越大越好。统一高分方向 `J`。
- 配置：{"n": "polynomial degree; choose a single unresolved medium degree"}
- 人类基线证据：The human construction f(z)=z^n−1 gives C(n)≥1 exactly. Sendov conjectured C(n)=1. Meir–Sharma proved n<6; Brown n<7 and n<8; Brown–Xiang proved n≤8 (1999); Tao proved the sufficiently large-degree regime. Medium degrees remain open in the 2025 paper.
- 验证成本：Medium for candidate polynomial: certify roots and derivative roots; proving global supremum ≤1 is a deep theorem.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：For n≤8 or sufficiently large n human theory proves the conjectured value; choose a genuinely unresolved medium n. Numerical polynomial candidate is only a lower-bound witness.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/20.html)；[来源2](https://arxiv.org/abs/2511.02864)

### T092 · Schmeisser polynomial critical-point barycenter constant

- 类别：矩阵、格与代数极值。
- 问题：For fixed n, determine the least C(n) such that for each degree-n polynomial with roots in the unit disk and every convex combination of its roots, some critical point lies within distance C(n) of that combination.
- 输出：Explicit polynomial roots and convex weights for lower-bound witness; exact derivative roots and certified distances.
- 单一标量：`min_j |Σ_k l_k z_k−w_j| for the submitted polynomial and weights`；越大越好。统一高分方向 `J`。
- 配置：{"n": "degree n≥2", "weights": "simplex weights; part of optimization variables"}
- 人类基线证据：Schmeisser conjectured C(n)=1; the AlphaEvolve repository states the conjectured value but no numeric human construction or row-specific best lower bound was verified in this scan. Treat numerical baseline as待核实.
- 验证成本：Medium/high: polynomial root certification and optimization over a continuum of convex weights.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Human construction/record not verified; worst-case optimization includes a continuous simplex and polynomial family. Need a finite witness protocol.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/21.html)；[来源2](https://arxiv.org/abs/2511.02864)

### T093 · Borcea p-moment critical-point distance constant

- 类别：矩阵、格与代数极值。
- 问题：For fixed (p,n), maximize the worst root-to-nearest-critical-point distance over degree-n polynomials whose roots satisfy n^−1Σ|z_i|^p≤1; this defines C(p,n).
- 输出：Polynomial roots and derivative roots with exact/interval algebraic data; verify moment constraint and distances.
- 单一标量：`max_{root ζ} min_{critical ξ}|ξ−ζ| for the submitted normalized polynomial`；越大越好。统一高分方向 `J`。
- 配置：{"p": "moment exponent, 1≤p<∞", "n": "degree n≥2"}
- 人类基线证据：Borcea (1996) proved Sendov's conjecture for polynomials with at most seven distinct zeros. Khavinson, Pereira, Putinar, Saff and Shimorin (2011) formulated Borcea's variance conjectures; AlphaEvolve paper notes Borcea's conjecture C(p,n)=1 and verifies special cases (p,n)=(1,3),(2,4) in the cited literature. No general numeric row baseline retrieved.
- 验证成本：High: root and derivative root enclosures plus moment constraint; global sharpness unverified.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Related to Sendov but genuinely adds a p-moment condition; parameter p=∞ recovers Sendov-like behavior. Need a concrete open row and numeric human lower construction.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/22.html)；[来源2](https://arxiv.org/abs/2511.02864)

### T094 · Noncommutative matrix AM–GM ratio

- 类别：矩阵、格与代数极值。
- 问题：固定n,m,d和一个明确的酉不变范数，提交n个d×d半正定矩阵A_i，最小化有放回与无放回的长度m乘积范数平均值之比。
- 输出：Finite PSD matrices with rational/algebraic entries; exact products, norms, and ratio or certified eigenvalue bounds.
- 单一标量：`[n^(−m) Σ_{j1,…,jm} ||A_j1⋯A_jm||] / [((n−m)!/n!) Σ_{distinct j1,…,jm} ||A_j1⋯A_jm||]`；越小越好。统一高分方向 `-J`。
- 配置：{"n,m,d": "固定，小n和m限制枚举成本", "norm": "例如operator norm，必须固定"}
- 人类基线证据：Duchi (2012) posed noncommutative AM–GM conjectures; Recht and Ré (2012) gave commentary/counterexample context. De Sa (2020) constructed counterexamples to a related matrix inequality. Exact parameter-row record and theorem status need primary-source audit.
- 验证成本：Medium/high: exact matrix products and spectral norms; PSD/eigenvalue constraints need certification.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：分母必须严格正；PSD和所选范数都需验证。原代理未抄明确方向，本表按官方47题取inf修正。乘积枚举n^m，仅小配置适合快速验证。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/47.html)；[来源2](https://proceedings.mlr.press/v23/recht12.html)

### T095 · Minimum Mahler measure of noncyclotomic integer polynomials

- 类别：矩阵、格与代数极值。
- 问题：For fixed degree bound d, find a noncyclotomic monic integer polynomial minimizing Mahler measure M(P)=∏ max(1,|root|).
- 输出：Integer polynomial with irreducibility/noncyclotomic proof and certified roots/Mahler measure.
- 单一标量：`Mahler measure M(P)`；越小越好。统一高分方向 `-J`。
- 配置：{"degree_bound": "d", "class": "monic integer, irreducible, noncyclotomic"}
- 人类基线证据：Lehmer (1933)给出degree10多项式 x^10+x^9−x^7−x^6−x^5−x^4−x^3+x+1，Mahler measure约1.176280818。这是经典历史人类构造；不就2026最新状态作未经核实断言。
- 验证成本：Medium/high: irreducibility and roots/Mahler measure require exact algebraic certification.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：For degree bounded and broad coefficient sizes the search space is ill-defined; specify coefficient/degree constraints and distinguish known lower bound from conjectured minimum.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://doi.org/10.2307/1968172)；[来源2](https://www.research.ed.ac.uk/files/1874954/Smyth240707.pdf)

### T096 · Integer Chebyshev polynomial construction

- 类别：矩阵、格与代数极值。
- 问题：给定区间 E 与次数上限 n，构造非零整数系数多项式 P，最小化其在 E 上的sup范数。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`||P||_E^(1/n)`；越小越好。统一高分方向 `-J`。
- 配置：{"n": "固定次数上限，归一化指数固定为该n", "E": "例如[0,1]"}
- 人类基线证据：Pritsker (2001/2005)、Habsieger–Salvy、Flammang 等提供显式因子构造。Pritsker原稿有历史界；近年声称新界的预印本不自动作为已核人类纪录。
- 验证成本：中：整数多项式临界点隔离和区间端点求值。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：区别于实系数Chebyshev闭式问题；需要具体次数和因子指数表，不能用渐近常数当有限分数。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/math/0101166)；[来源2](https://math.okstate.edu/people/igor/intcheb.pdf)

### T097 · Shortest addition chain

- 类别：数论与算术构造。
- 问题：固定目标整数 n，输出从1出发的加法链，每项为之前两项之和，末项n。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`number of additions`；越小越好。统一高分方向 `-J`。
- 配置：{"n": "目标整数；大小与位数为配置"}
- 人类基线证据：Flammenkamp、Clift 有精确长度数据库；Wilson/Resta 公开 n<=1024 的实际最短链。大数记录须区分历史人与近期可能AI参与的更新。
- 验证成本：低：逐步验证等式和长度。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：小数多数已知最优，适合校准；单目标最优加法链NP-hard性不能从多目标版本直接推断。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://wwwhomes.uni-bielefeld.de/achim/addition_chain.html)；[来源2](https://webhost.services.iit.cnr.it/staff/giovanni.resta/ac/)

### T098 · Integer complexity

- 类别：数论与算术构造。
- 问题：固定正整数 n，输出只由常数1、+、×、括号组成且值为n的表达式，最小化1的个数。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`number of ones`；越小越好。统一高分方向 `-J`。
- 配置：{"n": "目标整数；表达式按树计数，不允许共享子表达式免费复用"}
- 人类基线证据：Arias de Reyna–van de Lune (2014) 及 Fuller 的算法给出人类精确结果；Iraids等研究展示截至10^12的历史计算范围。具体表达式尚须从构造算法重建。
- 验证成本：低至中：大整数表达式求值。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：已知最优值表不等于已下载表达式；与允许共享中间量的加法链不同。
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://arxiv.org/abs/1404.2183)；[来源2](https://cs.uwaterloo.ca/~shallit/DC2015/iraids2.pdf)

### T099 · Narrow admissible prime k-tuples · MVP

- 类别：数论与算术构造。
- 问题：固定 k，输出 k 个不同整数 H，使每个素数 p 下 H 不覆盖所有剩余类，最小化直径。
- 输出：见定义：提交实际有限构造或可认证函数，不接受仅声明成绩。
- 单一标量：`max(H)-min(H)`；越小越好。统一高分方向 `-J`。
- 配置：{"k": "元组大小"}
- 人类基线证据：Engelsma–Sutherland/Polymath8 2013数据库有k=2..5000的元组、日期和贡献者；本次已下载并精确验证 k50直径246、k100直径558。
- 验证成本：低：只需检验 p<=k 的素数，p>k自动成立。
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：不是直接搜索素数；最窄admissible tuple与是否产生无穷素数簇分开。
- 研究状态：example_witness_recomputed_not_full_task_audit；当前仅为候选。
- 来源：[来源1](https://math.mit.edu/~primegaps/)；[来源2](https://math.mit.edu/~drew/PrimeGapsOberwolfach3.pdf)

### T100 · Factoring N! into N balanced factors

- 类别：数论与算术构造。
- 问题：For a fixed integer N, partition prime factors of N! among N integer factors and maximize the smallest factor; C(N) is the largest c for which N! can be factored into N factors all at least c.
- 输出：N positive integers with product exactly N!; verify exact product and minimum factor.
- 单一标量：`min_i a_i, with the task maximizing this minimum (lower bound on C(N))`；越大越好。统一高分方向 `J`。
- 配置：{"N": "positive integer; choose a fixed table row"}
- 人类基线证据：Guy and Selfridge studied the problem; the AlphaEvolve paper cites asymptotic C(N)/N=1/e−c0/log N+O(1/log^(1+c)N). Andrew Sutherland's public GuySelfridge.m implements a human search, and exact values C(N) for N≤10^4 are listed in the cited erdos-guy-selfridge repository/OEIS A034258. Retrieve a fixed row/value before freeze; not AI baseline.
- 验证成本：Low for witnesses (big integer product); exact optimum is a bin-covering problem and may be expensive.
- 发现空间：按具体配置核定：已证明最优的实例仅作校准；有未闭合上下界且已有可重算见证的实例可进入发现轨。当前不统一标高。
- 缺口/风险：Product factorization means integer factors, not arbitrary reals; fixed N and exact table baseline are mandatory. Optimality verification can be NP-hard.
- 研究状态：pending_configuration_and_witness_audit；当前仅为候选。
- 来源：[来源1](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/38.html)；[来源2](https://github.com/teorth/erdos-guy-selfridge)；[来源3](https://math.mit.edu/~drew/GuySelfridge.m)；[来源4](https://oeis.org/A034258)；[来源5](https://arxiv.org/abs/2511.02864)

## 去重与暂缓项

- 等圆在不同容器归入同一任务的容器配置；等正方形的尺寸、数量也不额外计任务。
- 最大行列式order29属于阶数配置；0/1矩阵与增广±1矩阵的等价版本不重复计数。
- LABS energy与merit factor不重复；线性码长度/维数/距离的反向参数化不重复。
- Sidon interval与Golomb ruler的等价版本合并；Gagliardo–Nirenberg特殊参数并入一般任务。
- 纯Hadamard、Costas、项目平面等存在性任务未入这100项；不能使用任意上限内最大存在阶数凑标量。
- Newman多项式若以所有根最大模为最小化目标，则x^n+1使最优值恒1，原候选被剔除。
- Moving sofa、连续Kakeya、Crouzeix等仍是有名研究问题，但本轮因连续可行性认证或标量重算较重未选入100项主表；记录保存在原始调研文件。
- 约束图族和不同码类仍有关联；主表不是声称100个毫无数学联系的问题。

详见 benchmark_selection_principles.md；原始六份调研文件保留代理的建议与未核实内容，主表用于本轮讨论。
