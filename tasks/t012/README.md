# T012: Thomson problem on the sphere

## 中文

在单位球面上放置 32 个不同点，最小化所有无序点对的库仑能量 \(E=\sum_{i<j}1/\|x_i-x_j\|_2\)。正式配置 T012-C01 固定 n=32。输入用有理立体投影参数表示；检查器精确构造球面点，并用整数平方根得到每一项的有理能量区间。严格模式不依赖浮点容差。

人类基线采用 Cambridge Cluster Database 的 32 点 \(I_h\) 构造。数据库列出的能量为 412.2612746，并提供坐标档案。数据库称其为已找到的最低结构；此处不把它说成已证明全局最优。原始坐标以小数存储。`human.py` 将其作为有理数读取，旋转坐标轴后转换为有理立体投影参数，因此球面约束由定义精确满足。转换后复算能量与来源的舍入值会有微小差异。

## English

Place the configured number of distinct points on the unit sphere and minimize the Coulomb energy \(E=\sum_{i<j}1/\|x_i-x_j\|_2\). T012-C01 uses 32 points. Inputs use rational stereographic parameters. The checker constructs exact sphere points and uses integer square roots to give rational energy bounds for every pair. Strict validation does not use floating-point tolerances.

The existing C01 human baseline uses the 32-point \(I_h\) construction in the Cambridge Cluster Database. The database reports energy 412.2612746 and provides a coordinate archive. It lists this as a lowest structure found; this task does not claim a proof of global optimality. The source coordinates are decimal values. `human.py` reads them as rational numbers, applies a coordinate-axis rotation, and converts them to rational stereographic parameters. The sphere constraint then holds exactly by construction. The reconstructed energy can differ slightly from the rounded source value.

## Sources

- Wales and Ulker, “Structure and Dynamics of Spherical Crystals Characterised for the Thomson Problem,” *Physical Review B* 74, 212101 (2006), linked from the [Cambridge Cluster Database table](https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html).
- [N=32 coordinate file](https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/xyz/32.xyz), archived as `data/ccd_32.xyz`.
