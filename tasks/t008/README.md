# T008: Covering numbers

## English

For each fixed configuration, find a small collection of k-point blocks on v points that contains every t-point subset. The checker enumerates all required subsets and verifies coverage exactly. The objective is the number of distinct blocks. The task does not ask for an optimality proof.

The reported public construction has 23 blocks. Its source is the [La Jolla Covering Repository](https://ljcr.dmgordon.org/cover.html), also preserved in the [Zenodo dataset](https://doi.org/10.5281/zenodo.19735294). The archive attributes the 2004 improvement to Andrei Ochmat. The witness is stored in `data/sota_witness.json` and is independently checked by the task evaluator. The repository reports best-known coverings, not necessarily proven minima.

Configuration T008-C02 is C(20,10,4). LJCR gives 32 <= C(20,10,4) <= 36 and publishes a 36-block construction by Rade Belic. Deliever et al. list a 35-block tabu-search attempt with 18 uncovered four-subsets. It is infeasible. The verified 36-block witness is in `data/search_reference_C02.json` and covers all 4,845 four-subsets. This configuration is accepted by Sol on 2026-11-07. The minimum is open because the best public lower bound is 32.

## 中文

对每个固定配置，在 v 个点上选择尽量少的 k 点块，使每个 t 点子集都至少出现在一个块中。检查器会穷举全部目标子集并精确验证覆盖。目标值是不同块的数量。本任务不要求证明最优性。

公开资料报告了23块构造，来源为[La Jolla覆盖设计库](https://ljcr.dmgordon.org/cover.html)，并保存在[Zenodo数据集](https://doi.org/10.5281/zenodo.19735294)。归档记录将该改进归于 Andrei Ochmat，日期为2004-07-20。见证保存在 `data/sota_witness.json`，已由检查器精确复算；这不表示已证明最优。

## Reproduced reference / 已复现对照

The frozen human-method reference has 62 blocks. It reconstructs the finite geometry and induced-covering methods of [Gordon, Kuperberg and Patashnik (1995), sections III–IV](https://arxiv.org/html/math/9502238). Take all 62 affine hyperplanes of AG(5,2). Delete points `{1,8,13,15,16,24,28,31}` (binary point labels 0–31). Each hyperplane loses at least two points. Pad each remaining intersection to 14 points. Each four-set lies in an affine hyperplane, so the resulting blocks cover all four-sets. The implementation selected the deleted points. The value 62 is a reproduced instance of a published method; the paper does not report this particular restriction as a record.

固定评分对照为62块。它复现论文第III–IV节中的方法。删除点集由本项目选择。62块构造已精确检查。23块公开见证是独立复现的最佳已知构造。评分仍使用冻结的62块对照。

配置 T008-C02 为 C(20,10,4)。LJCR 给出 32 <= C(20,10,4) <= 36，并收录 Rade Belic 的36块构造。Deliever 等列出的35块禁忌搜索尝试仍有18个四点子集未覆盖，因此不可行。已验证的36块见证在 `data/search_reference_C02.json`，精确覆盖全部4,845个四点子集。该配置已通过 Sol 验收（2026-11-07）。公开下界为32，因此最优值未定。

The classical search uses greedy set cover on500 seeded random14-subsets plus the seed pool. It produces40 blocks at seed0. This saved local result is the reference program; the published-method human normalization stays62.
