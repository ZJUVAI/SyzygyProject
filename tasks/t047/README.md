# T047: integer difference bases

## English

### Mathematical task

For the fixed integer `N = 6166`, find a finite set `B ⊂ Z` with as few elements as possible such that each integer `d = 1, …, 6166` is a difference `y - x` of two elements of `B`. The score is `|B|`, and lower is better. The checker accepts negative or large marks. Translating every mark by the same integer does not change the differences.

This is the unrestricted integer difference-basis problem `Δ(6166)`. It is distinct from the sparse-ruler problem, which fixes marks inside `[0, 6166]` and usually requires both endpoints. Our witness may have marks above 6166. A sparse ruler is still a valid difference basis when its marks cover the required interval, but its mark-location restriction is not part of this task.

The finite value `Δ(6166)` is not known from the sources checked for this release. Leech and Golay report a 128-mark construction, which gives `Δ(6166) ≤ 128`; it does not prove equality. Their 128 is the strongest source-reported human construction at this parameter. For the frozen comparison value, this task uses the weaker 158-mark Wichmann construction and labels it separately.

The checked analytic lower bound is 123. Banakh and Gavrylkiv prove `lim Δ(n)^2/n = inf Δ(n)^2/n ≥ 2 + max_{0<φ<π} 2 sin(φ)/(φ+π)`. Setting `φ=π/2` and using `π<22/7` gives `lim Δ(n)^2/n > 80/33`. Thus `33·Δ(6166)^2 > 80·6166 = 493280`. Since `122²·33 = 491172 < 493280` and `123²·33 = 499257 > 493280`, `Δ(6166) ≥ 123`. The resulting reported gap is 123–128. The simpler pair-count bound 112 is also valid but weaker.

### Sources and records

- Georgiev, Gómez-Serrano, Tao, and Wagner, [*Mathematical exploration and discovery at scale*, arXiv:2511.02864v1, §6.3](https://arxiv.org/html/2511.02864v1#S6.SS3). The paper defines `Δ(n)` using integer differences and cites `128²/6166` as the earlier upper bound for its asymptotic constant. It reports a later AlphaEvolve improvement to `360²/49109`; that different parameter is not this task's record.
- Banakh and Gavrylkiv, [*Difference bases in cyclic groups*, arXiv:1702.02631v6, §§3–4](https://arxiv.org/html/1702.02631). The paper states Singer's theorem for cyclic difference sets and records the Leech–Golay interval constructions, including `Δ(6166) ≤ 128`.
- The [AlphaEvolve problem repository](https://github.com/google-deepmind/alphaevolve_repository_of_problems) contains its difference-bases notebook. The checked `main` commit is `8f447457957deac61e28bf1676746f0753b3b2f8` (2026-07-11); notebook blob SHA-1 is `0cdb812ada3b6053f749e05301a743fd191e8700`, raw SHA-256 is `e5bd224563055caf53c0fef9b9c67620c7124a14aa77094cce456d9927b65489`. It gives the evolved 49109-parameter construction, not the 6166 witness.
- The saved 128-mark witness is an independently reconstructed Singer/Leech-family product. It uses a Singer difference set for `q=31`, the interval factor `{0,1,4,6}`, and a cyclic multiplier selected by a finite search. The witness passes the exact checker. It is not claimed to be the identical set used by Leech or Golay. The source paper does not report AI provenance for its historical 128-point construction.
- The frozen human baseline is the classical Wichmann ruler `W(38,3)`. Its 158 marks form a complete ruler of length 6548, so they cover all required differences through 6166. Saarela and Vanhatalo give the gap formula and a full proof of completeness in their [2026 paper](https://doi.org/10.37236/13806), Definitions 8 and 16 and Theorem 18. This weaker baseline is distinct from the source-reported 128-mark human record. This ruler is a restricted construction used as a valid witness in the unrestricted task; the task itself does not impose the sparse-ruler mark bound.

### Programs and use

The checker exactly recomputes difference coverage with integer arithmetic and minimizes the number of distinct integer marks. It ignores submitted score fields. `init_program.py` returns the valid but deliberately large interval `[0,6166]`. `baseline.py` runs seeded randomized greedy set cover and does not read either comparison witness. `human.py` rebuilds Wichmann `W(38,3)`. `reference.py` loads the pinned reconstructed 128-mark witness. `evolution.py` exposes the traditional search entry point.

Run one program with:

```sh
MATHBENCH_CONFIG_ID=T047-C01 .venv/bin/python -c 'from tasks.t047.reference import run_code; print(run_code())'
```

Run the task checks with:

```sh
.venv/bin/python -m pytest tasks/t047/test_task.py -q
```

The standard search limits are 300 seconds for generation, 60 seconds for verification, 4 GiB memory, and one CPU thread. Fixed iteration and restart counts are the default. Set `MATHBENCH_SEARCH_SECONDS` only for an explicitly time-limited exploratory run.

### Status and limits

The public 128 result is a feasible upper bound, not an optimality proof. The independent reconstruction verifies another 128-point construction at the fixed parameter. The checked literature does not give an exact value for `Δ(6166)` or a matching lower bound. A current survey found no later proof closing this finite gap; the survey is limited to the sources and snapshots named above.

## 中文

### 数学任务

固定 `N=6166`。寻找整数集 `B⊂Z`，使每个 `d=1,…,6166` 都能写成两个元素之差 `y−x`，并使 `|B|` 尽量小。目标是最小化 `|B|`。检查器允许负数标记，也允许标记大于6166。整体平移不改变差值。

这是无限制整数差基 `Δ(6166)`。它与稀疏尺不同。稀疏尺要求所有标记都在 `[0,6166]` 内，通常还要求包含两个端点。本任务没有这个位置限制。稀疏尺只要覆盖所需差值，也能作为本任务的可行构造；但本任务不要求稀疏尺的限制。

已核查来源没有给出有限值 `Δ(6166)`。Leech 与 Golay 报告了一个128点构造，因此 `Δ(6166)≤128`，但这不证明等号。它是同参数最强的已报告人类构造。冻结对照使用较弱的158点 Wichmann 构造，并单独记录。

核查到的解析下界为123。Banakh 与 Gavrylkiv 证明 `lim Δ(n)^2/n = inf Δ(n)^2/n ≥ 2 + max_{0<φ<π} 2 sin(φ)/(φ+π)`。取 `φ=π/2`，再用 `π<22/7`，得到 `lim Δ(n)^2/n > 80/33`。所以 `33·Δ(6166)^2 > 80·6166 = 493280`。又因 `122²·33=491172<493280`，而 `123²·33=499257>493280`，故 `Δ(6166)≥123`。同参数区间为123到128。简单的成对计数下界112也成立，但较弱。

### 来源与记录

- Georgiev、Gómez-Serrano、Tao、Wagner，[*Mathematical exploration and discovery at scale*，arXiv:2511.02864v1，第6.3节](https://arxiv.org/html/2511.02864v1#S6.SS3)。论文以整数差定义 `Δ(n)`，并用 `128²/6166` 作为渐近常数的旧上界。论文另报 AlphaEvolve 后来把上界改进为 `360²/49109`。该结果的参数不同，不属于本配置。
- Banakh 与 Gavrylkiv，[*Difference bases in cyclic groups*，arXiv:1702.02631v6，第3–4节](https://arxiv.org/html/1702.02631)。论文陈述 Singer 循环差集定理，并记录 Leech–Golay 的区间构造，包括 `Δ(6166)≤128`。
- [AlphaEvolve 问题仓库](https://github.com/google-deepmind/alphaevolve_repository_of_problems)包含差基 notebook。核对的 `main` 提交为 `8f447457957deac61e28bf1676746f0753b3b2f8`（2026-07-11）。Notebook blob SHA-1 为 `0cdb812ada3b6053f749e05301a743fd191e8700`，原始文件 SHA-256 为 `e5bd224563055caf53c0fef9b9c67620c7124a14aa77094cce456d9927b65489`。它给出49109参数的新构造，不是6166见证。
- 保存的128点见证由 Singer/Leech 型乘积独立重建。构造使用 `q=31` 的 Singer 差集、区间因子 `{0,1,4,6}`，并通过有限搜索选择循环乘数。精确检查器验证该见证。我们不声称它与 Leech 或 Golay 使用的原见证相同。来源没有说明历史128点构造的 AI 参与情况。
- 冻结的人类基线使用经典 Wichmann 尺 `W(38,3)`。它有158个标记，构成长度6548的完全稀疏尺，因此覆盖6166以内的差值。Saarela 与 Vanhatalo 在[2026年论文](https://doi.org/10.37236/13806)的定义8、定义16和定理18给出间隔公式和完整证明。这个弱基线与文献报告的128点人类纪录分开。此稀疏尺仅作为无限制整数差基任务中的可行构造；本任务不设置稀疏尺的位置约束。

### 程序与运行

检查器用整数精确重算差值覆盖，并最小化不同整数标记的数量。它不读取候选声明的成绩。`init_program.py` 返回有效但较大的 `[0,6166]`。`baseline.py` 运行固定种子的随机贪心集合覆盖，不读取对照见证。`human.py` 重建 Wichmann `W(38,3)`。`reference.py` 读取固定的128点重建见证。`evolution.py` 提供传统搜索入口。

运行一个程序：

```sh
MATHBENCH_CONFIG_ID=T047-C01 MATHBENCH_SEED=0 .venv/bin/python tasks/t047/reference.py
```

运行任务检查：

```sh
.venv/bin/python -m pytest tasks/t047/test_task.py -q
```

默认生成预算为300秒，验证预算为60秒，内存为4 GiB，使用一个 CPU 线程。默认搜索使用固定迭代数和重启数。只有明确进行限时探索时才设置 `MATHBENCH_SEARCH_SECONDS`。

### 状态与限制

公开的128点构造给出可行上界，不是最优性证明。本任务独立重建并验证了一个同参数128点构造。已核查文献没有给出 `Δ(6166)` 的确切值，也没有匹配的下界。截至本次来源快照，未找到关闭有限差距的更新证明。核查范围仅限上文列出的来源和版本。
