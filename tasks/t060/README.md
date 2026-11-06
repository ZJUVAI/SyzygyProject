# T060: C(24,14,4)

## English

Find a small collection of 14-point blocks on 24 points that contains every four-point subset. The checker enumerates all 10,626 four-subsets and verifies coverage exactly. The objective is the number of distinct blocks. The task does not ask for an optimality proof.

The reported public construction has 23 blocks. Its source is the [La Jolla Covering Repository](https://ljcr.dmgordon.org/cover.html), also preserved in the [Zenodo dataset](https://doi.org/10.5281/zenodo.19735294). The archive attributes the 2004 improvement to Andrei Ochmat. The witness is stored in `data/sota_witness.json` and is independently checked by the task evaluator. The repository reports best-known coverings, not necessarily proven minima.

## 中文

在24个点上选择尽量少的14点块，使每个四点子集都包含在至少一个块中。检查器会穷举全部10,626个四点子集，并精确验证覆盖。目标值是不同块的数量。本任务不要求证明最优性。

公开资料报告了23块构造，来源为[La Jolla覆盖设计库](https://ljcr.dmgordon.org/cover.html)，并保存在[Zenodo数据集](https://doi.org/10.5281/zenodo.19735294)。归档记录将该改进归于 Andrei Ochmat，日期为2004-07-20。见证保存在 `data/sota_witness.json`，已由检查器精确复算；这不表示已证明最优。

## Reproduced reference / 已复现对照

The frozen human-method reference has 62 blocks. It reconstructs the finite geometry and induced-covering methods of [Gordon, Kuperberg and Patashnik (1995), sections III–IV](https://arxiv.org/html/math/9502238). Take all 62 affine hyperplanes of AG(5,2). Delete points `{1,8,13,15,16,24,28,31}` (binary point labels 0–31). Each hyperplane loses at least two points. Pad each remaining intersection to 14 points. Each four-set lies in an affine hyperplane, so the resulting blocks cover all four-sets. The implementation selected the deleted points. The value 62 is a reproduced instance of a published method; the paper does not report this particular restriction as a record.

固定评分对照为62块。它复现论文第III–IV节中的方法。删除点集由本项目选择。62块构造已精确检查。23块公开见证是独立复现的最佳已知构造。评分仍使用冻结的62块对照。

The classical search uses greedy set cover on500 seeded random14-subsets plus the seed pool. It produces40 blocks at seed0. This saved local result is the reference program; the published-method human normalization stays62.
