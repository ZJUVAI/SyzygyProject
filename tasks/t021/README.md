# T021: Thomson problem on the sphere

## 中文

在单位球面上放置 32 个不同点，最小化所有无序点对的库仑能量 \(E=\sum_{i<j}1/\|x_i-x_j\|_2\)。配置为 T021-C01、T021-C02 和 T021-C03，分别固定 n=32、40、50。输入用有理立体投影参数表示；检查器精确构造球面点，并用整数平方根得到每一项的有理能量区间。严格模式不依赖浮点容差。

人类基线采用 Cambridge Cluster Database 的 32 点 \(I_h\) 构造。数据库列出的能量为 412.2612746，并提供坐标档案。数据库称其为已找到的最低结构；此处不把它说成已证明全局最优。原始坐标以小数存储。`human.py` 将其作为有理数读取，旋转坐标轴后转换为有理立体投影参数，因此球面约束由定义精确满足。转换后复算能量与来源的舍入值会有微小差异。

## English

Place the configured number of distinct points on the unit sphere and minimize the Coulomb energy \(E=\sum_{i<j}1/\|x_i-x_j\|_2\). The configurations fix n=32, 40, and 50. Inputs use rational stereographic parameters. The checker constructs exact sphere points and uses integer square roots to give rational energy bounds for every pair. Strict validation does not use floating-point tolerances.

The existing C01 human baseline uses the 32-point \(I_h\) construction in the Cambridge Cluster Database. The database reports energy 412.2612746 and provides a coordinate archive. It lists this as a lowest structure found; this task does not claim a proof of global optimality. The source coordinates are decimal values. `human.py` reads them as rational numbers, applies a coordinate-axis rotation, and converts them to rational stereographic parameters. The sphere constraint then holds exactly by construction. The reconstructed energy can differ slightly from the rounded source value.

## Sources

- Wales and Ulker, “Structure and Dynamics of Spherical Crystals Characterised for the Thomson Problem,” *Physical Review B* 74, 212101 (2006), linked from the [Cambridge Cluster Database table](https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html).
- [N=32 coordinate file](https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/xyz/32.xyz), archived as `data/ccd_32.xyz`.

## Configurations

| Configuration | Charges | CCD energy | Point group | Status |
|---|---:|---:|---|---|
| T021-C01 | 32 | 412.2612746 | I_h | Accepted by Sol (2026-11-06) |
| T021-C02 | 40 | 660.6752788 | T_d | Accepted by Sol |
| T021-C03 | 50 | 1055.1823147 | D_6d | Accepted by Sol |

Set `MATHBENCH_CONFIG_ID` to choose the count. `human.py`, `reference.py`, `init_program.py`, and the classical search baseline use that configuration. The starter is a self-contained file and passes isolated cold-export execution.

The original CCD coordinate files and a snapshot of the table are saved in `data/`. The table calls these records “Global Minima,” but the listed energies and coordinates are numerical constructions. We do not treat that label as an optimality proof. Chen and Mehta (2014), §III, state that deterministic results were known only for N=2, 3, 4, 5, 6, and 12. The checked literature therefore leaves N=40 and N=50 open. The exact rational checker certifies the energy of the stereographically reconstructed witness, which can differ slightly from the rounded CCD energy because the published coordinates have finite decimal precision.

The n=40 and n=50 saved witnesses under `best/T021-C02/` and `best/T021-C03/` remain accepted by Sol on 2026-11-07.
