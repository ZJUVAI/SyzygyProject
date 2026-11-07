# T093：最大价值多边形装箱

## 中文

### 任务定义

固定 CG:SHOP 2024 实例 `random_cf2_74ae2d30_50`。容器是一个 15 顶点凸多边形。实例含 44 种物品，共可选 50 件。每种物品有一个简单多边形形状、整数价值和可用数量。

每件被选物品只能做整数平移，不能旋转。所有物品必须在容器内。不同物品的内部不能相交。边界接触允许。目标是最大化所选物品价值总和。

唯一配置 `T093-C01` 固定上述实例。原始实例保存在 `data/source/random_cf2_74ae2d30_50.cgshop2024_instance.json`，SHA-256 为 `f2ad180face7d410ec40cf531d8bbf4a5631a9a6c18f9d7a73579717abca9c92`。注意，实例中“50”表示可用物品总数；物品类型数为 44。

解的格式沿用 CG:SHOP：`item_indices` 中的整数是 0 起始的物品类型编号；`x_translations` 和 `y_translations` 是相应的整数平移量。三组数组长度必须相同。每个物品类型的出现次数不能超过数量限制。

### 公开结果与人类基线

Shadoks 队公开了此实例的 2304 分装箱，包含 23 件物品。结果页面还列出 SmartPlacer 的 2268 和 CGA Lab Salzburg 的 2105。Shadoks 论文介绍整数规划和启发式搜索。公开 JSON 的元数据说明它是 `digopt` 优化前的构造。我们逐件读取其平移并用本任务检查器重新验证，准确得到 2304。`human.py` 重放这份公开见证；它不声称重现 Shadoks 的求解程序。

公开的 2304 是可行值，不是最优性证明。CG:SHOP 官方页面定义了竞赛目标和不旋转规则。Shadoks 的论文也描述了整数平移模型。2026-11-06 检查时未找到该固定实例已经证明最优的来源。此结论仅限已查来源。

来源：[CG:SHOP 2024 官方页面](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2024/)；[Shadoks 的实例结果页](https://pageperso.lis-lab.fr/guilherme.fonseca/cgshop24view/HTML_SOLUTIONS/random_cf2_74ae2d30_50.html)；[Shadoks 论文](https://pageperso.lis-lab.fr/guilherme.fonseca/CGSHOP24.pdf)，第 1 节；[官方 pyutils24 格式说明](https://github.com/CG-SHOP/pyutils24)。

### 精确验证

输入顶点、价值、平移坐标都是整数。检查器用耳切法把容器和每种简单多边形分成不重叠三角形。它用有理数半平面裁剪精确计算三角形交面积。物品裁剪到容器三角形后的面积必须等于物品原面积。任意两件物品的交面积必须为零。因此，所有边界接触合法，任何正面积重叠都会被拒绝。检查器最后按选中物品类型重算价值总和。候选程序提供的分数不会参与验证。

### 搜索和预算

初始程序返回空装箱，得分为 0。传统基线只读公开实例，按价值密度排序，再随机抽取整数平移并逐个精确检查。搜索固定种子和尝试次数；可用 `MATHBENCH_SEARCH_SECONDS` 启用时间截断。人类结果和参考见证保存在独立目录，不会给初始程序或搜索基线读取。

默认每次生成限时 300 秒，验证限时 60 秒，内存 4 GiB，单线程。任务状态：已通过 Sol 验收（2026-11-06）。

## English

### Definition

The fixed input is the CG:SHOP 2024 instance `random_cf2_74ae2d30_50`. The container is a convex polygon with 15 vertices. The instance has 44 item types and 50 available items in total. Each type has a simple polygon, an integer value, and a quantity.

Each selected item may move by an integer translation. Rotation is forbidden. Every item must lie inside the container. Item interiors must be pairwise disjoint. Boundary contact is allowed. Maximize the sum of selected item values.

Configuration `T093-C01` fixes this instance. The raw file is `data/source/random_cf2_74ae2d30_50.cgshop2024_instance.json`, with SHA-256 `f2ad180face7d410ec40cf531d8bbf4a5631a9a6c18f9d7a73579717abca9c92`. Here, 50 is the total available item count. The number of item types is 44.

The output uses the CG:SHOP fields. `item_indices` contains zero-based item type indices. `x_translations` and `y_translations` contain the matching integer translations. All three arrays must have the same length. A type cannot be selected more times than its quantity.

### Public result and human baseline

The Shadoks team published a value-2304 packing with 23 selected items. The result page also lists SmartPlacer at 2268 and CGA Lab Salzburg at 2105. The Shadoks paper describes integer programming and heuristic search. The public JSON metadata says that this witness is from before `digopt` optimization. This task replays its translations and recomputes 2304 with the exact checker. `human.py` replays this published witness; it does not reproduce the Shadoks solver.

The reported 2304 is a feasible value, not a proof of optimality. The official CG:SHOP page gives the contest objective and forbids rotation. The Shadoks paper describes the integer-translation model. The source check on 2026-11-06 found no proof that this fixed instance is solved to optimality. This statement is limited to the sources checked.

Sources: [official CG:SHOP 2024 page](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2024/); [Shadoks instance result page](https://pageperso.lis-lab.fr/guilherme.fonseca/cgshop24view/HTML_SOLUTIONS/random_cf2_74ae2d30_50.html); [Shadoks paper](https://pageperso.lis-lab.fr/guilherme.fonseca/CGSHOP24.pdf), Section 1; [official pyutils24 format](https://github.com/CG-SHOP/pyutils24).

### Exact verification

Coordinates, values, and translations are integers. The checker triangulates the container and each simple polygon with exact ear clipping. It clips triangle pairs with rational arithmetic and computes exact intersection areas. Each item must have the same area inside the container as its original area. Every pair of items must have zero intersection area. Thus boundary contact is allowed and any positive-area overlap is rejected. The checker then recomputes the total value. Candidate score claims do not affect verification.

### Search and limits

The initial program returns an empty packing with value 0. The traditional baseline reads only the public instance. It orders items by value density, then samples integer translations and checks each proposed placement exactly. It uses a fixed seed and fixed attempt count by default. `MATHBENCH_SEARCH_SECONDS` enables an explicit time cutoff. Comparison witnesses stay in separate directories and are not read by the initial program or search baseline.

Default limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one thread. Status: accepted by Sol on 2026-11-06.
