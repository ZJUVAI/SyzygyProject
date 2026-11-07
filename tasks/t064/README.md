# T064: ortho40 的最少非钝角三角剖分

## 中文

配置 `T064-C01` 固定 CG:SHOP 2025 的正交简单多边形 `ortho_40_56a6f463`。输入有 40 个顶点，没有额外约束边。目标是用尽量少的新增 Steiner 点，把整个多边形剖分为非钝角三角形。直角允许。

评测器要求候选给出全部 Steiner 坐标和无向边。它使用有理数精确运算检查坐标唯一性、点在多边形内或边界上、边不相交且位于多边形内、边界完整覆盖、图连通，以及每个有界面恰为非退化三角形。每个角的点积必须非负。所有三角形面积之和必须与输入多边形面积相等。评测器不采样、不使用浮点容差，也不信任候选分数。

坐标接口接受任意精度整数、有理数字符串，以及按其精确 IEEE 二进制有理数解释的有限 JSON 浮点数，不设分母位数或字符串长度上限。每次正式验证仍受 16 MiB 输出、4 GiB 内存和 60 秒验证时间限制。Steiner 点数上限为 2000；已知可行上界为 19，因此任何更优构造最多有 18 个 Steiner 点，不会被此上限排除。原几何问题允许任意实坐标；本配置只接收有理坐标见证，不能据此声称覆盖所有实坐标构造。

人类基线为 129 个 Steiner 点。`human.py` 从输入顶点的全部 x/y 坐标构造笛卡尔网格，并把多边形内的每个网格矩形分成两个直角三角形。这是对公开网格式非钝角剖分方法的弱基线重建，不是竞赛纪录。Ahn 等人的 SoCG 2025 论文报告了以输入点网格为基础的正交实例构造方法。[论文与算法](https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.80/LIPIcs.SoCG.2025.80.html)

公开参考构造有 19 个 Steiner 点。Abrahamsen、Brunck、Conradi、Kolbe 和 Nusser 的获胜实现论文在 Figure 10 明确展示本实例及 19 点解；固定源代码版本为提交 `77920a0e578e5bff13c710f988ec1c52d61dcfd8`，见证已存入 `data/reference/` 并精确复核。[SoCG 2025 论文，Figure 10](https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.79/LIPIcs.SoCG.2025.79.html) · [归档软件](https://doi.org/10.4230/artifacts.23288)

已检查的来源没有证明 19 点最优，也没有报告本实例更小的见证。我们在 2026-11-06 复查了论文、归档软件和公开实例数据；这不是穷尽所有资料的声明。获胜团队论文未披露该构造是否使用 AI，因此记录为来源未说明。

## English

Configuration `T064-C01` fixes the CG:SHOP 2025 orthogonal simple polygon `ortho_40_56a6f463`. It has 40 vertices and no extra constraint edges. The objective is to minimize the number of added Steiner points in a triangulation of the full polygon. Every triangle must be non-obtuse; right angles are allowed.

The checker takes all Steiner coordinates and undirected edges. It uses exact rational arithmetic to check unique coordinates, point containment, non-crossing edges inside the polygon, full boundary coverage, graph connectivity, and triangular bounded faces. At each triangle vertex, the exact dot product must be non-negative. The sum of triangle areas must equal the polygon area. The checker uses no sampling, floating-point tolerance, or candidate score.

The coordinate interface accepts arbitrary-precision integers, rational strings, and finite JSON floats interpreted as their exact IEEE binary rational values. It sets no denominator-bit or coordinate-string-length limit. Each verification still uses the shared 16 MiB output, 4 GiB memory, and 60 second limits. The checker caps the number of Steiner points at 2,000. Since the known feasible upper bound is 19, any improvement has at most 18 Steiner points and is not excluded by that cap. The geometric problem permits arbitrary real coordinates; this configuration accepts rational-coordinate witnesses only and does not claim to represent every real-coordinate construction.

The reconstructed human baseline has 129 Steiner points. `human.py` builds a Cartesian grid from all input x and y coordinates, then splits each grid rectangle inside the polygon into two right triangles. This is a weak reconstruction of a published grid-based method, not a competition record. Ahn et al. describe grid-based constructions for orthogonal instances in their SoCG 2025 paper. [Paper and method](https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.80/LIPIcs.SoCG.2025.80.html)

The public reference has 19 Steiner points. Figure 10 of the winning implementation paper by Abrahamsen, Brunck, Conradi, Kolbe, and Nusser shows this instance and the 19-point construction. The fixed software commit is `77920a0e578e5bff13c710f988ec1c52d61dcfd8`. The witness is stored under `data/reference/` and was checked with exact arithmetic. [SoCG 2025 paper, Figure 10](https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.79/LIPIcs.SoCG.2025.79.html) · [Archived software](https://doi.org/10.4230/artifacts.23288)

The reviewed sources do not prove that 19 is optimal and do not report a smaller witness for this instance. We checked the paper, archived software, and public instance data on 2026-11-06. This is not an exhaustive survey. The winning team did not state whether AI tools were used for this construction, so its AI provenance is recorded as unstated.
