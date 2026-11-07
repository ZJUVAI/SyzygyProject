# T077: 和差集原始对数比

## 数学目标

选取整数集合 \(A\)，满足 \(2\le |A|\le512\)，且所有元素都在 `[-1000000,1000000]`。最大化

\[
\frac{\ln |A-A|}{\ln |A+A|},\qquad
A+A=\{a+b:a,b\in A\},\quad A-A=\{a-b:a,b\in A\}.
\]

所有有序对和对角项都参与运算；相同结果只计一次。检查器精确计算两个整数集合，再用向外舍入区间计算自然对数比。报告区间下端作为最大化时的保守成绩。

固定配置为 `T077-C01`。冷起点是 `{0,1,3}`。公开界限限制在 512 个整数和指定区间内。

## 与 T012 的区别

T012 的目标为

\[
C(A)=\frac{\ln(|A+A|/|A|)}{\ln(|A-A|/|A|)}.
\]

T077 的目标为 \(\ln|A-A|/\ln|A+A|\)。二者没有保持排序的单调变换关系。下面两组集合都满足 T012 的基数、数值区间和检查器前置条件：

| 集合 | \(|A|\) | \(|A+A|\) | \(|A-A|\) | T012 | T077 |
|---|---:|---:|---:|---:|---:|
| `{0,2,3,4,7,11,12,14}` | 8 | 26 | 25 | 1.0344212156 | 0.9879620776 |
| 上一集合与其平移 1000 的并集 | 16 | 78 | 75 | 1.0253872280 | 0.9909976281 |

T012 把第一组排在第二组之前，T077 则把第二组排在第一组之前。精确集合及复算值保存在 `data/source/t012_order_reversal_examples.json`。因此不能用 T012 的最优见证或分数直接替代 T077 的目标。

## 人类方法、冻结对照与更强复现

Gyarmati、Hennecart、Ruzsa 的《Sums and Differences of Finite Sets》手稿日期为 2008-05-30。第 2 节公式 (13)–(15) 定义

\[
V(m,L)=\{(x_1,\ldots,x_m)\in\mathbb{Z}_{\ge0}^m:\sum_i x_i\le L\}
\]

及其和集、差集基数，并给出整数投影权重递推 \(L_0=1, L_{j+1}=2L L_j+1\)。论文明确给出 \(m=6,L=5\) 实例。本任务保留它作为冻结人类对照。其权重为 `[1,11,111,1111,11111,111111]`，投影集合有 462 个不同元素，最大元素 555555。闭式和逐项枚举都得到 `|A+A|=8008`、`|A-A|=39733`。

该有限对照的成绩为

\[
\frac{\ln(39733)}{\ln(8008)}
=1.1782049454028793644760968453682013895930448936\ldots
\]

再按论文同一通用公式取 \(m=7,L=4\)，权重为 `[1,9,73,585,4681,37449,299593]`。原投影有 330 个元素，范围为 0 到 1198372。整体平移 `-599186` 后，元素范围为 `[-599186,599186]`，和差集基数不变。闭式和逐项枚举得到 `|A+A|=6435`、`|A-A|=33111`，成绩为

\[
1+\frac{\ln(33111/6435)}{\ln(1198373)}
=\frac{\ln(33111)}{\ln(6435)}
=1.1867965542406812481762523985613661574193739510\ldots
\]

`human.py` 输出冻结的 m=6、L=5 对照；`reference.py` 输出更强的 m=7、L=4 本地公式实例化。论文给出通用公式，但没有把此 m=7、L=4 分数列为单独纪录。本任务不声称该构造全局最优。论文其他段落的渐近指数也不是此有限目标分数。

## 运行

```sh
.venv/bin/python -m tasks.t077.init_program
.venv/bin/python -m tasks.t077.baseline
.venv/bin/python -m tasks.t077.evolution
.venv/bin/python -m tasks.t077.human
.venv/bin/python -m tasks.t077.reference
.venv/bin/python -m pytest tasks/t077 -q
```

初始程序、传统搜索和演化搜索均从简单起点开始，不读取人类、参考或来源数据。搜索分数使用浮点数作启发式排序；正式评测重新精确枚举整数和差集，并给出保守区间。`human.py` 重放冻结的 m=6、L=5 对照，`reference.py` 重放更强的 m=7、L=4 见证。全部五个程序实现 `run_code()`。默认预算为生成 300 秒、验证 60 秒、4 GiB 内存、单线程。状态：`accepted_by_sol`。

---

# T077: Raw logarithmic sum-difference ratio

## Objective

Choose a set \(A\) of 2 to 512 distinct integers in `[-1000000,1000000]`. Maximize

\[
\frac{\ln |A-A|}{\ln |A+A|},\qquad
A+A=\{a+b:a,b\in A\},\quad A-A=\{a-b:a,b\in A\}.
\]

Use all ordered pairs and diagonal pairs. Count each result once. The checker recomputes both integer sets exactly and evaluates the natural-log ratio with outward-rounded interval arithmetic. It reports the lower endpoint as a conservative maximization score.

The fixed configuration is `T077-C01`. The cold seed is `{0,1,3}`. The public limits are 512 elements and the stated integer interval.

## Difference from T012

T012 scores \(C(A)=\ln(|A+A|/|A|)/\ln(|A-A|/|A|)\). T077 scores \(\ln|A-A|/\ln|A+A|\). These objectives do not preserve candidate rankings. The two sets below both meet T012's cardinality, interval, and checker preconditions:

| Set | \(|A|\) | \(|A+A|\) | \(|A-A|\) | T012 | T077 |
|---|---:|---:|---:|---:|---:|
| `{0,2,3,4,7,11,12,14}` | 8 | 26 | 25 | 1.0344212156 | 0.9879620776 |
| The first set union its translate by 1000 | 16 | 78 | 75 | 1.0253872280 | 0.9909976281 |

T012 ranks the first set higher. T077 ranks the second set higher. Exact sets and recomputed scores are saved in `data/source/t012_order_reversal_examples.json`. A T012 score or witness cannot stand in for this objective.

## Human method, frozen baseline, and stronger reproduction

The May 30, 2008 manuscript *Sums and Differences of Finite Sets* by Gyarmati, Hennecart, and Ruzsa gives, in Section 2 equations (13)–(15), the set

\[
V(m,L)=\{(x_1,\ldots,x_m)\in\mathbb{Z}_{\ge0}^m:\sum_i x_i\le L\}
\]

and formulas for its sumset and difference-set sizes. It projects the vectors to integers with weights \(L_0=1, L_{j+1}=2L L_j+1\). The paper explicitly gives the \(m=6,L=5\) instance. This task keeps it as the frozen human baseline. Its weights are `[1,11,111,1111,11111,111111]`; the projection has 462 distinct elements and maximum 555555. The formulas and full enumeration give `|A+A|=8008` and `|A-A|=39733`.

Its score for this finite objective is

\[
\frac{\ln(39733)}{\ln(8008)}
=1.1782049454028793644760968453682013895930448936\ldots
\]

Next, instantiate the same published general formula with \(m=7,L=4\). The weights are `[1,9,73,585,4681,37449,299593]`. Its 330-element projection ranges from 0 to 1198372. Translate it by `-599186` to fit the configured interval; translation preserves both set cardinalities. The closed forms and full enumeration give `|A+A|=6435` and `|A-A|=33111`. Its score is

\[
1+\frac{\ln(33111/6435)}{\ln(1198373)}
=\frac{\ln(33111)}{\ln(6435)}
=1.1867965542406812481762523985613661574193739510\ldots
\]

`human.py` emits the m=6,L=5 frozen baseline. `reference.py` emits the stronger local m=7,L=4 formula instance. The paper gives the general formula but does not list this score as a separate record. This task does not claim global optimality. The paper's asymptotic exponents are not this finite score.

## Run

```sh
.venv/bin/python -m tasks.t077.init_program
.venv/bin/python -m tasks.t077.baseline
.venv/bin/python -m tasks.t077.evolution
.venv/bin/python -m tasks.t077.human
.venv/bin/python -m tasks.t077.reference
.venv/bin/python -m pytest tasks/t077 -q
```

The initial, traditional-search, and evolutionary programs start from the simple seed and do not read human, reference, or source data. Search uses floating point only to rank proposals. Formal evaluation recomputes exact integer sets and a certified score interval. `human.py` replays the frozen m=6,L=5 baseline; `reference.py` replays the stronger m=7,L=4 witness. All five programs expose `run_code()`. Default budgets are 300 seconds for generation, 60 seconds for verification, 4 GiB memory, and one thread. Status: `accepted_by_sol`.
