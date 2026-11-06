# T014: Heilbronn problem for 11 points in the unit square

Choose 11 distinct points in the unit square to maximize the area of the smallest triangle formed by any three points. The objective is the exact minimum of the 165 triangle areas. The checker uses rational arithmetic and checks every triple and each coordinate bound.

The public record is Goldberg's 1972 construction with area `1/27`. The coordinate list is available at [the exact-coordinate record](https://math.tejstead.com/heilbronn/square/11/points.txt), which credits Goldberg and provides a rational configuration. We store the coordinates as fractions and recompute the minimum area exactly. This verifies the witness score; it does not prove global optimality.

The generated seed uses `(i/10, i²/100)` for `i=0,…,10`. It is distinct and has no three collinear points. The baseline performs bounded random-restart local coordinate search. Its decimal coordinates are converted to exact decimal fractions for final scoring. This is a heuristic, not a certificate.

## Added configurations / 新增配置

C02 has n=12 points; C03 has n=16 points. Both passed Sol review and appear in `task.json`. The checker examines all 220 or 560 triangles with exact rational arithmetic. The n=12 witness uses published decimal coordinate literals as exact rationals. The n=16 witness has minimum area 7/341. Sources and exact scores are in `records.json:configuration_records`.

C02为12点，C03为16点。两者均通过Sol验收。检查器用精确有理数运算检查全部220或560个三角形。12点构造按公开十进制坐标解释为有理数；16点构造的最小面积为7/341。来源及精确成绩见`records.json:configuration_records`。
