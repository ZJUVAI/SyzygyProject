# T067: binary constant-weight code A(17,4,5)

## 中文

### 定义和配置

配置 `T067-C01` 固定二元码字长度为 17、每个码字的汉明重量为 5、任意两个不同码字的汉明距离至少为 4。目标是最大化码字数，记作 (A(17,4,5))。输入为 17 位二进制字符串列表。检查器逐个检查长度、重量和重复项，并精确检查全部无序码字对。

这也可看作在所有 5 元子集中选取最大集合，使不同集合的交集大小至多为 3，即 packing (D(17,5,4))。本项目按原始 constant-weight-code 任务记录；等价表述不另计任务。

### 来源和已知状态

Milshtein 于 2022-10-08 在线发表的论文报告了 444 个码字。论文将发现归于最大独立集的随机局部搜索，并说明所用方法基于 Generic Scuba Search。任务目录保存了原始码字文件及 SHA-256，也保存了解析后的复播数据。论文摘要没有提到生成式 AI；论文没有单独说明 AI 来源，因此记录只写“未报告”，不推断更强结论。

截至 2026-11-06 检查的 Brouwer 表，(A(17,4,5)) 下界为 444，没有最优标记。Milshtein 论文称已知上界为 474，并引用 Östergård (2010)。本任务精确复现下界 444。没有找到证明 444 达到上界，故配置仍开放。论文的 2023 勘误保留该码及 444 记录。

### 数据和程序

- `data/source/milshtein_a17_4_5_444.txt`：保存的原始 444 码字文件；其 SHA-256 为 `bc5261c3f1b9229985dcd4a95388bf15b42f9d657aa1fa55fd017121d255216a`。
- `data/reference/a17_4_5_444.json`：供 `human.py` 和 `reference.py` 复播的同一见证。
- `check.py`：校验每个字的 17 位长度、重量 5、唯一性和全部点对的距离至少 4。目标完全从输入重算。
- `init_program.py`：返回一个有效码字，目标为 1；该文件自包含。
- `baseline.py`：在固定的 6,188 个重量 5 字中，对候选优先级做定种子随机重排，再贪心构造独立集。它不读取参考数据。
- `evolution.py`：对候选优先级序列进行定种子块变异和精英选择，再用同一精确贪心过程构造码。它不读取参考数据。
- `human.py`：复播论文中的传统计算搜索结果。
- `reference.py`：固定复播已验证的 444 字见证。
- `evaluator.py`：连接共享候选评测接口。

程序默认使用固定重启数或代数。设置 `MATHBENCH_SEARCH_SECONDS` 后可使用共享时间截断。程序从 `MATHBENCH_CONFIG_ID` 读取配置，从 `MATHBENCH_SEED` 读取随机种子。生成限时 300 秒，验证限时 60 秒，内存 4 GiB，单线程。

### 验证

运行以下命令：

```sh
.venv/bin/python -m pytest tasks/t067 -q
.venv/bin/python -m json.tool tasks/t067/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t067/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t067/records.json > /dev/null
```

测试涵盖已发表见证、初始构造、搜索程序、精确距离、重量和长度、重复字、破坏距离、配置错误、伪造分数、程序异常及超时。独立复算全部 (444*443/2 = 98,346) 个字对。状态为已通过 Sol 验收（2026-11-06）。

## English

### Definition and configuration

`T067-C01` fixes binary word length 17, weight 5, and minimum pairwise Hamming distance 4. Maximize the number of codewords, denoted (A(17,4,5)). A solution is a list of 17-bit binary strings. The checker validates each word, rejects duplicates, and checks every unordered pair.

This is also a packing problem: select 5-subsets of a 17-set so that any two selected subsets intersect in at most 3 points. This equivalent view does not create a separate benchmark task.

### Sources and current status

Milshtein's paper, published online on 2022-10-08, reports 444 codewords. It attributes the discovery to a stochastic local search for maximum independent set based on Generic Scuba Search. The task stores the original word file and its SHA-256, as well as a replay file. The abstract does not report generative AI use. The paper gives no separate AI-provenance statement, so this record makes no stronger claim.

The Brouwer table checked on 2026-11-06 lists 444 as a lower bound for (A(17,4,5)), with no optimum marker. Milshtein's paper states a known upper bound of 474 and cites Östergård (2010). This task exactly reproduces the 444 lower bound. No proof that 444 is optimal was found, so the configuration remains open. The 2023 correction leaves the code and its 444 record unchanged.

### Data and programs

- `data/source/milshtein_a17_4_5_444.txt` is the saved original 444-word file. Its SHA-256 is `bc5261c3f1b9229985dcd4a95388bf15b42f9d657aa1fa55fd017121d255216a`.
- `data/reference/a17_4_5_444.json` is the replay witness used by `human.py` and `reference.py`.
- `check.py` validates word length, weight, uniqueness, and all pair distances. It recomputes the objective from the input.
- `init_program.py` returns one valid codeword and is standalone.
- `baseline.py` shuffles the fixed set of 6,188 weight-five words with a seeded random order and builds a greedy independent set. It does not read comparison data.
- `evolution.py` mutates candidate orderings with seeded block shuffles and elitist selection, then builds a code with the same exact greedy rule. It does not read comparison data.
- `human.py` replays the traditional computational result in the paper.
- `reference.py` replays the verified 444-word witness.
- `evaluator.py` connects the shared candidate-evaluation interface.

Programs use fixed restart or generation counts by default. Set `MATHBENCH_SEARCH_SECONDS` for the shared time cutoff. Programs read `MATHBENCH_CONFIG_ID` and `MATHBENCH_SEED`. Generation is limited to 300 seconds, verification to 60 seconds, memory to 4 GiB, and one thread.

### Validation

Run:

```sh
.venv/bin/python -m pytest tasks/t067 -q
.venv/bin/python -m json.tool tasks/t067/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t067/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t067/records.json > /dev/null
```

Tests cover the published witness, the initial construction, search programs, exact distance, weight and length, duplicates, a broken distance constraint, wrong configuration, forged scores, worker errors, and timeouts. An independent count checks all 444*443/2 = 98,346 word pairs. Status is accepted by Sol on 2026-11-06.
