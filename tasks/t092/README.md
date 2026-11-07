# T092：S² 上 20 次实球谐的 L4/L2 集中度最大化

## 定义

令 \(P(x,y,z)\) 为非零、实、齐次 20 次调和多项式。限制在单位球面 \(S^2\) 上，令 \(M_p\) 表示相对于归一化均匀面积测度的 \(|P|^p\) 平均值。本任务最大化
\[
J=\frac{\|P\|_{L^4(S^2)}}{\|P\|_{L^2(S^2)}}=\left(\frac{M_4}{M_2^2}\right)^{1/4}.
\]
固定参数为次数 20 和实球谐空间。系数可整体缩放，目标不变。

输入用 231 个有理系数，按 \(x^a y^b z^{20-a-b}\) 的顺序排列：先让 \(a\) 从 20 降到 0，再让 \(b\) 从 \(20-a\) 降到 0。系数可以是整数或精确有理数字符串。不设分子、分母或系数大小限制。调和性用精确 Laplacian=0 验证。

正式模型将系数限于 \(\mathbb Q\)。度 20 调和条件是有理系数线性方程组的核。有理解在其实系数核中稠密；目标在非零多项式上连续且尺度不变。因此此表示范围与实系数模型有相同上确界。每个实球谐不必能用单个有理系数向量精确表示。

## 精确检查

球面单项式矩满足：若任一指数为奇数，平均值为零；若指数为 \((2a,2b,2c)\)，则
\[
\mathbb E[x^{2a}y^{2b}z^{2c}]=\frac{(2a-1)!!(2b-1)!!(2c-1)!!}{(2(a+b+c)+1)!!}.
\]
检查器精确卷积得到 \(P^2\) 和 \(P^4\)，计算有理数 \(M_2,M_4\)，并输出 \(J\) 的精确四次根表达式和有理夹逼。它不使用球面采样作为证明。

## 人类构造和未解状态

Stanton 和 Weinstein 证明每个次数的最高权函数是 L4 范数的局部极大值。他们没有证明固定次数的全局最优。人类对照采用最高权实球谐
\[
P(x,y,z)=\operatorname{Re}(x+iy)^{20}.
\]
其整数系数为 \((-1)^j\binom{20}{2j}x^{20-2j}y^{2j}\)。独立矩计算还复核了文献公式 \(M_2=B_{20}/2\)、\(M_4=3B_{40}/8\)，其中 \(B_k=4^k(k!)^2/(2k+1)!\)。该构造是已发表的局部极大值，不宣称为全局最优。

- Stanton–Weinstein, *On the L4 norm of spherical harmonics*, 1981，[DOI 10.1017/S0305004100058229](https://doi.org/10.1017/S0305004100058229)。摘要明确说的是局部最大值。全文第 6 节给出 \(O(\ell\log\ell)\) 上界，不给固定次数 20 的全局最佳常数。
- Sogge 1986 的结果确定渐近阶，不确定本配置的最优常数。
- 2026 年 Rudin 有界正交基论文研究复球面上的齐次全纯多项式基，与本题的固定次数实球谐最大化不同。

截至 2026-11-06，未找到次数 20 全局最优证明。

## English

Maximize the normalized ratio \(J=\|P\|_{L^4(S^2)}/\|P\|_{L^2(S^2)}=(M_4/M_2^2)^{1/4}\) over nonzero real homogeneous harmonic polynomials of degree 20 in three variables. Moments use uniform probability measure on the unit sphere.

The input is 231 exact rational coefficients in the order \(x^a y^b z^{20-a-b}\), with \(a\) descending from 20 to 0, and then \(b\) descending from \(20-a\) to 0. There is no coefficient or denominator cap. Rational harmonic polynomials are dense in the real harmonic subspace because the Laplacian constraints are a rational linear system. This dense domain has the same supremum for the continuous, scale-invariant objective.

The checker verifies the exact Laplacian and integrates \(P^2\) and \(P^4\) by rational monomial moments. It returns an exact fourth-root expression and a certified rational interval. No sample estimate is used as a certificate.

Stanton and Weinstein prove that the highest-weight harmonic is a local L4 maximizer for each degree. They do not establish the global optimum at degree 20. The human witness is \(\operatorname{Re}(x+iy)^{20}\), independently verified by exact sphere moments. The 2026 Rudin orthonormal-basis result concerns a different complex holomorphic problem. No degree-20 global proof was found in sources checked on 2026-11-06.
