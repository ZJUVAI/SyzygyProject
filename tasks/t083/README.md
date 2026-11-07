# T083：四个等边三角形装入正方形

## 定义

把四个边长为 1 的等边三角形放入轴对齐正方形，三角形可独立平移和旋转，内部不得重叠。目标是最小化正方形边长。正方形左下角固定为原点。

形式输入使用 `Q(√3)` 中的坐标和平移，并用有理单位向量表示旋转。该表示在所有实平移和旋转中稠密，因此保持问题的下确界；它不声称精确表示每个实数位姿。证明思路是先以趋近 1 的有理比例分别向内缩每个三角形，制造严格间隙，再用稠密坐标和方向近似，最后围绕正方形原点按该比例的倒数放大整个排布。检查器在 `Q(√3)` 上精确计算，不使用浮点容差。

## 来源与状态

Friedman 的公开表将 n=4 的已知构造记为 `1+1/√3`，归于 1996 年。表中把数值列为已发现的构造，没有称其最优已证。2026-11-06 复核时，表仍把 n=4 列作已知构造；n=3 的证明另列在 2026 年 10 月。重建见 [reference witness](data/reference/friedman4_reconstructed.json)，原页面图及重建来源见 `data/source/`。

冻结人类对照为向上舍入的 `1.577350269189626`。它略高于精确值 `1+√3/3`，这样最小化兼容分数的分母仍是保守对照。该值是可行构造上界，不是最优性证明。

## English

Place four unit equilateral triangles in an axis-aligned square. Each triangle may translate and rotate independently. Triangle interiors must be disjoint. Minimize the square side. The square has lower-left corner `(0,0)`.

The exact input domain uses translations in `Q(sqrt(3))` and rational unit directions. To show that it has the same infimum, shrink each triangle about its centroid by a rational factor tending to 1. This creates positive clearance. Approximate the centers and rotations by domain values, then scale the whole arrangement about the square origin by the inverse shrink factor. The result has unit triangles and a square side tending to the original side. The checker performs exact ordered-field comparisons in `Q(sqrt(3))` and uses no floating-point tolerance.

Friedman's public table lists the n=4 construction with side `1+1/sqrt(3)` and dates it to 1996. It labels the construction as found, not proved optimal. The 2026-11-06 source review found n=4 still listed as a construction; the October 2026 proof is for n=3. The frozen human reference is rounded upward to `1.577350269189626`, slightly above the exact construction value. It is a feasible upper bound, not an optimality proof.

## Files

- `instruction.txt`: model-facing task prompt.
- `check.py`: exact algebraic checker.
- `init_program.py`: self-contained 2-by-2 seed.
- `baseline.py` and `evolution.py`: seeded generic placement searches; they do not read comparison assets.
- `human.py` and `reference.py`: separately generated and archived Friedman construction.
- `IMPLEMENTATION.md`: reproduction, source and test notes.
