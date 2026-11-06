# Current review status

**Accepted by Sol on 2026-11-04.** The new configurations are in `task.json`. The text below preserves the Luna submission and its source notes. Current results are in `records.json:configuration_records` and the expansion report.

# T014 configuration expansion

This proposal adds C02 (`n=12`) and C03 (`n=16`). It is staged for Sol review. The accepted `task.json` still contains C01 only.

The objective is the maximum, over distinct points in the unit square, of the smallest area among all triples. The checker parses each coordinate as an exact rational number and checks every triple. C02 has 220 triples. C03 has 560 triples.

## C02: 12 points

Comellas and Yebra's published construction is listed at [Tej Stead's n=12 record](https://math.tejstead.com/heilbronn/square/12/). The page credits the construction to Comellas and Yebra (December 2001) and cites their closed form. The associated paper gives the parameter `x` as the real expression

`x = 1 - ((27 + 3 sqrt(57))^(2/3) + 6) / (6(27 + 3 sqrt(57))^(1/3))`

and `y = 2x² - 3x + 1/2`; the coordinate pattern uses `x`, `1-x`, `y`, and `1-y`. The site publishes coordinates to 30 decimal places. `human.py` stores those published decimal literals as exact decimal rationals. This is a reconstruction of the posted coordinate file, not the exact algebraic number field representation. The checker independently reports the exact score of those literals as

`101871433411936556933637520697548102056943915772631725289 / 3125000000000000000000000000000000000000000000000000000000`

(approximately `0.0325988586918196982187640066232`). Thus the exact score belongs to the finite decimal witness saved here; the cited closed form establishes provenance for the construction. It does not prove optimality for 12 points.

Source: [n=12 points](https://math.tejstead.com/heilbronn/square/12/points.txt), [Comellas and Yebra record page](https://math.tejstead.com/heilbronn/square/12/), and Sudermann-Merx, *From Global Optimization to Exact Coordinates* (arXiv:2603.11107), Appendix B.

## C03: 16 points

The record page credits the construction to Mark Beyleveld (August 2006), describes it as an all-rational configuration, and gives the exact minimum area `7/341`. The published coordinates reduce to fractions with denominators 31 and 33. `human.py` stores these fractions, and the checker confirms the exact score `7/341` over all 560 triples. The affine-tesseract structure is recorded in the cited paper. This witness is not an optimality proof.

Source: [n=16 points](https://math.tejstead.com/heilbronn/square/16/points.txt), [n=16 record page](https://math.tejstead.com/heilbronn/square/16/), and Sudermann-Merx, *From Global Optimization to Exact Coordinates* (arXiv:2603.11107), Appendix B.

## Programs and limitations

`init_program.py` makes a distinct rational parabola seed for the selected `n`. `baseline.py` runs the existing bounded random-restart coordinate search with `n` selected from `MATHBENCH_CONFIG_ID`. `human.py` and `reference.py` replay the selected stored witness. Set `MATHBENCH_CONFIG_ID` to `T014-C02` or `T014-C03` before running these program files for C02 or C03.

These additions do not change the formal run directory. The decimal C02 witness is exact as stored, but it is a finite precision transcription. C03 is exact rational data. Both constructions are feasible witnesses only; neither establishes a global optimum.

## Sol acceptance, 2026-11-04

All four programs passed strict evaluation for each new configuration. Sol checked a cold seed export, independently recomputed a key quantity, rejected a damaged witness, and confirmed that a claimed score cannot change the score. Public record claims remain separate from reproduced witness scores.
