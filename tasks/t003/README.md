# T003: Packing unit squares in a square

## English

Place 26 non-overlapping unit squares in a square and minimize the enclosing side. T003-C01 is the only configuration. The checker uses exact arithmetic in Q(√2). Rotation is encoded by a half-angle tangent in this field. The strict check uses separating axes for every pair and computes the full bounding width and height. It checks feasibility and score, not optimality.

The human construction is Erich Friedman’s 1997 off-center construction, shown in Section 3, Figure 9. Its formula gives the side `(7+3√2)/2 ≈ 5.62132034355964`. The witness file reconstructs the formula for `(a,b)=(2,3)`: a 3 by 3 block of 45-degree squares, the surrounding axis-aligned squares, and the added column. The exact checker certifies its 26 squares and score in `Q(√2)`. The Squares Project lists the record as open with bounds `5.545 ≤ s(26) ≤ 5.62132034355964`.

## 中文

将 26 个互不重叠的单位正方形放入一个正方形，并最小化外框边长。T003-C01 是唯一配置。检查器在 Q(√2) 中作精确运算。旋转由该数域中的半角正切表示。严格检查会对每对方块使用分离轴，并计算完整包围框的宽和高。检查器验证可行性和分数，不证明最优性。

人类构造来自 Erich Friedman（1997）论文第三节图 9 的偏心构造。公式给出边长 `(7+3√2)/2 ≈ 5.62132034355964`。见证文件按 `(a,b)=(2,3)` 重建公式：中间为 3 乘 3 个 45 度方块，周围为轴对齐方块，右侧再加一列。精确检查器在 `Q(√2)` 中验证 26 个方块和分数。Squares Project 将该问题标为未解决，给出界 `5.545 ≤ s(26) ≤ 5.62132034355964`。
