# T080: 有限和差集指数证书

## 数学目标

选择非负整数集合 \(U\)，满足 `2≤|U|≤512`、`0∈U`、`max(U)≤1000000`。令

\[
s=|U+U|,\qquad d=|U-U|,\qquad q=2\max(U)+1.
\]

所有有序对都参与和差运算。最大化

\[
\theta(U)=1+\frac{\ln(d/s)}{\ln(q)}.
\]

另须严格满足 `d<q`。这条严格不等式是 GHR 有限构造引理的明确前提。检查器用整数精确计算 `s`、`d` 和 `q`，再用向外舍入区间计算对数分数，并将区间下端作为最大化的保守成绩。

## 来源与有限人类见证

Gyarmati、Hennecart、Ruzsa 的《Sums and Differences of Finite Sets》手稿日期为 2008-05-30。第 2 节在式 (11) 前的引理中，对含 0 的有限非负整数集定义 `s=|U+U|`、`d=|U-U|`、`q=2 max(U)+1` 和 `θ=1+ln(d/s)/ln(q)`。引理要求严格 `d<q`，然后用该指数构造具有任意大 `|B|` 的整数集对，并给出和集上界及差集指数下界。因此本任务优化的是一个有限见证所提供的指数参数；它不等于 T012 或 T077 的单集合目标，也不是该渐近定理本身的结论。

同一论文第 2 节式 (13)–(15) 给出

\[
V(m,L)=\{(x_1,\ldots,x_m)\in\mathbb{Z}_{\ge0}^m:\sum_i x_i\le L\}
\]

的基数、和集与差集基数，以及整数投影权重递推 \(L_0=1,L_{j+1}=2L L_j+1\)。取 `m=6,L=5` 得权重 `[1,11,111,1111,11111,111111]`。完整投影有 462 个不同整数，最大值 555555；闭式和全对枚举都给出 `s=8008,d=39733`。因此 `q=1111111`，严格条件 `39733<1111111` 成立。分数区间为

\[
1+\frac{\ln(39733/8008)}{\ln(1111111)}
=1.1150604037411407350410450588386944094785376751\ldots
\]

论文还讨论了最多 11 个元素的小集合上的最佳指数，但本配置允许最多 512 个元素，不能据此断言本配置最优。文中其他渐近指数也不是这个有限见证的分数。本任务没有发现本配置的最优性证明。

## 与 T012 和 T077 的区别

T012 的目标是 `ln(|A+A|/|A|)/ln(|A-A|/|A|)`。令 `A={0,2,3,4,7,11,12,14}`，以及 `B=A∪(A+1000)`。两者都满足 T012 的 `s>d>n` 前置检查，也满足 T080 的 `d<q`。T012 的成绩分别为 `1.0344212156…` 和 `1.0253872280…`，将 A 排在 B 前；T080 的成绩分别为 `0.9883524599…` 和 `0.9948497470…`，将 B 排在 A 前。

T077 的目标是 `ln(|U-U|)/ln(|U+U|)`。令 C 为 `V(2,3)` 投影，D 为 `V(18,1)` 投影。两者都满足 T080 配置和严格条件。T077 将 D 排在 C 前，分数约为 `1.1125793` 和 `1.0836423`；T080 将 C 排在 D 前，分数约为 `1.0741023` 和 `1.0448531`。四个集合和精确区间保存在 `data/source/objective_distinction_examples.json`。

## 运行

```sh
.venv/bin/python -m tasks.t080.init_program
.venv/bin/python -m tasks.t080.baseline
.venv/bin/python -m tasks.t080.evolution
.venv/bin/python -m tasks.t080.human
.venv/bin/python -m tasks.t080.reference
.venv/bin/python -m pytest tasks/t080 -q
```

初始程序是简单可行集合 `{0,1,4}`。传统搜索和演化搜索从该集合开始，只尝试自己的整数增删和替换，不读取对照数据。全部五个程序实现 `run_code()`。默认生成预算为 300 秒，验证预算为 60 秒，内存上限 4 GiB，单线程。状态：`accepted_by_sol`。

---

# T080: Finite sum-difference exponent certificate

## Objective

Choose a set \(U\) of nonnegative integers with `2≤|U|≤512`, `0∈U`, and `max(U)≤1000000`. Let

\[
s=|U+U|,\qquad d=|U-U|,\qquad q=2\max(U)+1.
\]

Use all ordered pairs. Maximize

\[
\theta(U)=1+\frac{\ln(d/s)}{\ln(q)}.
\]

The set must also satisfy `d<q`. This strict inequality is an explicit hypothesis of the GHR finite construction lemma. The checker counts both integer sets exactly, checks the inequality, then computes an outward-rounded score interval. It reports the lower endpoint as a conservative maximization score.

## Source and finite human witness

The May 30, 2008 manuscript *Sums and Differences of Finite Sets* by Gyarmati, Hennecart, and Ruzsa defines `s`, `d`, `q`, and `theta` in a lemma in Section 2 before equation (11). It requires `d<q` before deriving finite integer-set pairs with arbitrarily large `|B|` and an exponent bound. T080 optimizes this finite witness parameter. It is not the T012 or T077 single-set score and is not the asymptotic theorem itself.

Section 2 equations (13)–(15) give the simplex vectors `V(m,L)`, exact counts, and projection weights `L_0=1`, `L_(j+1)=2L L_j+1`. With `m=6,L=5`, the weights are `[1,11,111,1111,11111,111111]`. The projected set has 462 distinct elements, maximum 555555, `s=8008`, and `d=39733`. Thus `q=1111111` and `39733<1111111`. Its score interval contains `1.1150604037411407350410450588386944094785376751...`.

The paper also studies optimal exponents for small sets of at most 11 elements. This configuration allows up to 512 elements, so that small-set result does not settle it. No optimality proof for this bounded configuration was found.

## Difference from T012 and T077

T012 scores `ln(|A+A|/|A|)/ln(|A-A|/|A|)`. For `A={0,2,3,4,7,11,12,14}` and `B=A∪(A+1000)`, both satisfy T012's `s>d>n` precondition and T080's `d<q`. T012 scores them `1.0344212156...` and `1.0253872280...`, ranking A first. T080 scores them `0.9883524599...` and `0.9948497470...`, ranking B first.

T077 scores `ln(|U-U|)/ln(|U+U|)`. Let C be the `V(2,3)` projection and D the `V(18,1)` projection. Both meet T080's limits and strict condition. T077 ranks D over C, with scores about `1.1125793` and `1.0836423`. T080 ranks C over D, with scores about `1.0741023` and `1.0448531`. All sets and certified intervals are saved in `data/source/objective_distinction_examples.json`.

## Run

```sh
.venv/bin/python -m tasks.t080.init_program
.venv/bin/python -m tasks.t080.baseline
.venv/bin/python -m tasks.t080.evolution
.venv/bin/python -m tasks.t080.human
.venv/bin/python -m tasks.t080.reference
.venv/bin/python -m pytest tasks/t080 -q
```

The initial program is `{0,1,4}`. Traditional and evolutionary search start there and make their own integer-set changes. They do not read comparison data. All five programs expose `run_code()`. Default budgets are 300 seconds for generation, 60 seconds for verification, 4 GiB memory, and one thread. Status: `accepted_by_sol`.
