# T048: Minimum size of sorting networks

## English

A comparator sorts the values on two wires into ascending order. The task is to build a network that sorts every sequence on 17 wires while using as few comparators as possible. The objective is network size. Depth is not the objective.

The current Dobbelaere table lists a 71-comparator, 12-layer network and gives size bounds 63 to 71. The listed lower bound 63 is based on an unpublished, unrefereed strengthening; the strongest bound in published work found here is 60. Its 17-input, 10-layer network uses 74 comparators; depth 10 is proved optimal, but that does not prove a minimum size of 74. The 2013 Valsalam–Miikkulainen paper also reports a 71-comparator network from evolutionary search. The source does not state AI use. The best network in the current table is reproduced by exact exhaustive testing of all 131,072 binary inputs. The fixed human-method reference is the 85-comparator Batcher odd-even mergesort construction. Search starts from a separate 136-comparator network and does not read the comparison witness. See [IMPLEMENTATION.md](IMPLEMENTATION.md) for source pins and status.

## 中文

一个比较器会把两条线上的数按升序排列。本任务要求构造一个能排序 17 个输入的比较网络，并尽量减少比较器数量。目标是网络大小，不是层数。

Dobbelaere 当前表列出一个 71 比较器、12 层的网络，并给出大小界 63 至 71。已发表的下界为 60；表列的 63 来自未发表、未同行评审的加强结果。表中另一个 17 输入、10 层网络使用 74 个比较器；层数 10 已证明最优，但这不能证明比较器数量最少为 74。Valsalam 和 Miikkulainen 的 2013 年论文也报告了通过进化搜索找到的 71 比较器网络。来源没有说明是否使用 AI。当前表中的网络已通过全部 131,072 个二元输入的精确穷举检查。固定的人类方法参考值来自 Batcher 奇偶归并排序构造，共 85 个比较器。搜索从独立的 136 比较器起点开始，不读取对照见证。来源版本和开放状态见 [IMPLEMENTATION.md](IMPLEMENTATION.md)。

## Additional configurations: 18 and 19 inputs

The task includes C02 (`n=18`) and C03 (`n=19`). The current SorterHunter table lists a 77-comparator, 12-layer network for 18 inputs and an 85-comparator, 12-layer network for 19 inputs. It gives size bounds 68–77 and 73–85. These are open size gaps. Depth bounds of 10–11 are separate and do not prove minimum size.

The table sequences are pinned under `data/reference/` and checked against all `2^18` and `2^19` binary inputs. The human comparison uses Batcher odd-even mergesort padded to 32 wires, with sentinel-wire comparisons removed. It has 90 comparators for 18 inputs and 98 for 19, both exhaustively verified. The public SorterHunter output is labeled automated; AI provenance is unknown. New configurations are accepted by Sol on 2026-11-07.

## 新增配置：18 和 19 输入

任务新增 C02（`n=18`）和 C03（`n=19`）。当前 SorterHunter 表列出的网络分别有 77 和 85 个比较器，深度均为 12。表中大小下界分别为 68 和 73，因此大小最优性仍有缺口。深度下界 10–11 单独记录，不能证明比较器数量最少。

表中网络已固定保存在 `data/reference/`，并对全部 `2^18` 和 `2^19` 个二元输入做穷举验证。人类对照使用 Batcher 奇偶归并排序，补到 32 根线后移除哨兵线比较。18、19 输入分别有 90 和 98 个比较器，均已穷举验证。SorterHunter 将公开网络标为自动生成；是否使用 AI 未知。新增配置已通过 Sol 验收（2026-11-07）。
