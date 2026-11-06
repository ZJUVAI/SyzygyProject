# T002: Packing unit squares in a square

## English

Place n non-overlapping unit squares (n=26, 29, or 38) in a square and minimize the enclosing side. The checker uses exact arithmetic in Q(√2). Rotation is encoded by a half-angle tangent in this field. The strict check uses separating axes for every pair and computes the full bounding width and height. It checks feasibility and score, not optimality.

The human construction is Erich Friedman’s 1997 off-center construction, shown in Section 3, Figure 9. Its formula gives the side `(7+3√2)/2 ≈ 5.62132034355964`. The witness file reconstructs the formula for `(a,b)=(2,3)`: a 3 by 3 block of 45-degree squares, the surrounding axis-aligned squares, and the added column. The exact checker certifies its 26 squares and score in `Q(√2)`. The Squares Project lists the record as open with bounds `5.545 ≤ s(26) ≤ 5.62132034355964`.

## 中文

将n个互不重叠的单位正方形（n=26、29或38）放入一个正方形，并最小化外框边长。检查器在Q(√2)中作精确运算。旋转由该数域中的半角正切表示。严格检查会对每对方块使用分离轴，并计算完整包围框的宽和高。检查器验证可行性和分数，不证明最优性。

人类构造来自 Erich Friedman（1997）论文第三节图 9 的偏心构造。公式给出边长 `(7+3√2)/2 ≈ 5.62132034355964`。见证文件按 `(a,b)=(2,3)` 重建公式：中间为 3 乘 3 个 45 度方块，周围为轴对齐方块，右侧再加一列。精确检查器在 `Q(√2)` 中验证 26 个方块和分数。Squares Project 将该问题标为未解决，给出界 `5.545 ≤ s(26) ≤ 5.62132034355964`。

## Added configurations accepted by Sol

C03 (`n=29`) and C04 (`n=38`) passed Sol review and appear in `task.json`. C03 uses the rational construction based on Thomas Schadt’s 2025 human-computed packing; the published current best is slightly better and is listed separately. C04 reconstructs Göbel’s diagonal-strip family from Friedman’s Figure 1. `EXPANSION.md` and `records_expansion.json` give the source history and verification status.

## 已通过Sol验收的新增配置

C03（`n=29`）和C04（`n=38`）通过Sol验收，已加入`task.json`。C03 使用 Thomas Schadt 于 2025 年通过传统计算搜索得到的构造，并从保存的有理顶点证书重建输入坐标。当前公开最好值略优于此构造，记录中单独列出。C04 根据 Friedman 图 1 重建 Göbel 的斜带构造。来源和验证状态见 `EXPANSION.md` 与 `records_expansion.json`。
