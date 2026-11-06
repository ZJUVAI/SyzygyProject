# T009: Tammes problem on S²

## 中文

在单位球面 S² 上放置 n 个不同方向，最大化最小两点夹角，单位为弧度。评测器对每个输入坐标按精确有理数解释，检查全部点对，并在严格模式下给出保守角度区间。它验证构造和分数，不证明全局最优。

C02（n=16）、C03（n=17）和C04（n=19）均通过Sol验收，已加入正式运行目录。公开坐标来自 spherical-codes.org 对应参数页，来源归属和复现情况见 `records.json` 与 `EXPANSION.md`。

## English

Place n distinct directions on the unit sphere S² and maximize the minimum pairwise angle in radians. The checker interprets each input coordinate as an exact rational, checks every pair, and returns a conservative angle interval in strict mode. It verifies the construction and score; it does not prove global optimality.

C02 (n=16), C03 (n=17), and C04 (n=19) passed Sol review and are in the run registry. Their public coordinate files are archived. See `records.json` and `EXPANSION.md` for provenance and reproduction status.
