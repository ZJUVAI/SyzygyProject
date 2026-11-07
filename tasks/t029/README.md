# T029：有理数域上的 3×3 矩阵乘法秩

## 中文

### 数学定义与配置

配置 `T029-C01` 固定两个 3×3 矩阵，系数域为有理数域 \(\mathbb Q\)。候选给出若干项

\[
\alpha_s(A)\,\beta_s(B)\,\gamma_s,
\]

其中 \(\alpha_s\) 只依赖输入矩阵 \(A\)，\(\beta_s\) 只依赖输入矩阵 \(B\)，\(\gamma_s\) 是输出矩阵的系数向量。每个因子按行优先排列成 9 个有理数。全部项相加后必须精确等于 \(AB\)。目标是最小化项数，也就是双线性算法中的标量乘法数。每项系数可为任意有理数，不设置分母或系数大小限制。

评测器用精确 `Fraction` 算术重算 729 个张量系数。输出采用 \(C_{ik}=\sum_j A_{ij}B_{jk}\) 的顺序。整数和形如 `"-3/2"` 的字符串是 JSON 表示；本地接口也接受 `Fraction`。布尔值、浮点数、零因子和错误张量都会拒绝。27 项是基于学校算法种子的资源上限，不是最优性下界。

### 基线和见证

`init_program.py` 是标准 27 次乘法程序。`baseline.py` 对左上角 2×2 子问题使用 Strassen 七项公式，其余标量乘积直接计算，共 26 项。两者均不读取对照数据。`human.py` 解析 Lille 公布的 Laderman Maple 张量数据，令非零参数 \(\lambda=1\)，并按源文件表达式对第三因子转置。`reference.py` 读取归一化后的 23 项见证。

### 来源与未解状态

Laderman 于 1976 年给出 23 次乘法的非交换双线性算法。Université de Lille 的[算法页](https://fmm.univ-lille.fr/3x3x3.html)列出该算法及 [Maple 张量表示](https://fmm.univ-lille.fr/3x3x3_tensor.mpl.bz2)。原始压缩文件保存在 `data/source/`，重建的有理系数保存在 `data/laderman_rank23.json`。

Tomar 的[2026 年论文第 1 节](https://arxiv.org/html/2610.11823v3)明确说，特征零域上的秩仍未知，范围为 19 至 23。该文证明的是 \(\mathbb F_2\) 上秩为 23，并推出整数系数算法至少需要 23 次乘法。这些结论不能推出任意有理系数算法的秩为 23。故本配置在 \(\mathbb Q\) 上仍开放，23 只是已复现上界。

**状态：已通过 Sol 验收（2026-11-06）。**

## English

### Definition and configuration

`T029-C01` asks for the bilinear rank of multiplying two 3×3 matrices over the rational field \(\mathbb Q\). A term is \(\alpha_s(A)\beta_s(B)\gamma_s\). The first linear form depends only on input `A`; the second depends only on input `B`; the third gives coefficients for the output matrix. Each factor is a row-major vector of nine rational values. The sum of all terms must equal `AB` exactly. The objective is to minimize the number of terms, which is the scalar multiplication count of the bilinear algorithm. Coefficients may be any rational numbers. There is no denominator or magnitude limit.

The checker uses exact `Fraction` arithmetic and checks all 729 tensor coefficients. Its output convention is `C[i,k] = sum_j A[i,j] * B[j,k]`. JSON inputs may use integers or rational strings such as `"-3/2"`; the local API also accepts `Fraction` values. Booleans, floats, zero factors, and an incorrect tensor are rejected. The 27-term limit is a resource cap from the schoolbook seed, not a lower bound on the optimum.

### Baselines and witness

`init_program.py` gives the elementary 27-product algorithm. `baseline.py` applies Strassen's seven-product formula to the upper-left 2×2 subproblem and computes the other scalar products directly, for 26 terms. Neither reads comparison data. `human.py` parses Laderman's public Maple tensor data from Lille, sets its nonzero parameter to `lambda=1`, and transposes the third factor as required by the source expression. `reference.py` reads the normalized 23-term witness.

### Sources and open status

Laderman published a noncommutative 23-multiplication algorithm in 1976. The Université de Lille [algorithm page](https://fmm.univ-lille.fr/3x3x3.html) links to the [Maple tensor representation](https://fmm.univ-lille.fr/3x3x3_tensor.mpl.bz2). The compressed source is archived under `data/source/`; the reconstructed rational factors are in `data/laderman_rank23.json`.

Section 1 of Tomar's [2026 paper](https://arxiv.org/html/2610.11823v3) states that the rank over characteristic-zero fields remains unknown, between 19 and 23. The paper proves rank 23 over \(\mathbb F_2\) and derives the same lower bound for integer-coefficient algorithms. Those results do not settle arbitrary rational coefficients. The rank over \(\mathbb Q\) remains open; 23 is a reproduced upper bound.

**Status: accepted by Sol on 2026-11-06.**
