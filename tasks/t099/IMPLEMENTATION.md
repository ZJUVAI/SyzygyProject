# T099 implementation record

## Definition and sources

The fixed tile is the 11-cell `11P1` shape. A feasible result is a tiling of any axis-aligned integer rectangle by translations, rotations, and reflections of this tile. The score is the number of tiles, to minimize. The source's 54 by 55 tiling uses 270 tiles. The exact cell checker verifies the saved witness. The source calls 270 the smallest known order and labels the bound `<= 270`; no proof of a global minimum was found in the checked sources through 2026-11-06.

Sources: [Polyominoes.org P1 11-omino](https://polyominoes.org/data/11P1), [Michael Reid's 11-omino page](https://sicherman.net/mikereid/11omino7_rect.html), and [MIT Tiling Search K12](https://tilingsearch.mit.edu/HTML/data113/K12.html). The fixed shape and its source-page hash are saved in `data/source`. The public witness is saved separately in `data/reference` and is read only by `human.py` and `reference.py`.

## Verification

`check.py` recomputes all transformed tile cells, rejects invalid orientations and coordinates, checks for overlap, and verifies complete rectangle coverage. It does not use claimed objective fields. Tests cover valid source tilings, invalid dimensions and translations, invalid orientation values, overlap, incomplete coverage, fixed configuration types, forged scores, worker errors, and timeouts.

## Independent initialization search

The initial program must not read the public tiling. Offline independent searches use only the fixed cell set and target rectangle dimensions. The tracked replay script is `search_exact_cover.py`; it uses OR-Tools CP-SAT and an exact-cover model with one Boolean variable per tile placement and an exactly-one constraint for each board cell. It does not read `data/reference`.

With OR-Tools 9.15.6755, Python 3.13.12, one search worker, and seed `20261106`, CP-SAT found a 270-tile tiling of 54 by 55 in 477.481 seconds, under an 1800-second cap. The search reported 6,754,866 branches and 556,126 conflicts. The exact task checker independently recomputed all 2,970 cells. The witness is saved in `best/independent_cpsat_seed_270.json`. This was an offline search and did not run under the benchmark's 300-second generation limit. CP-SAT's `OPTIMAL` status applies to this satisfaction model for the fixed 54 by 55 board. It confirms a feasible tiling on that board. It does not prove a minimum over all rectangles.

The initial program repeats this independent witness twice, with the second copy translated by 55 rows. This gives a 540-tile tiling of 54 by 110. `baseline.py` checks all eight rectangle symmetries and tile-aligned rectangular cuts. It finds one 54 by 55 half with 270 tiles. `evolution.py` uses 12 seeded generations. Each generation mutates a rectangle symmetry, checks clean cuts, and keeps the four candidates with the lowest tile counts. Both programs start from `init_program.py`; neither reads `human.py`, `reference.py`, or `data/reference`.

An initial 300-second CP-SAT attempt on 54 by 55 returned `UNKNOWN` after 5,187,855 branches and 384,303 conflicts. A separate DLX attempt and a SciPy MILP attempt did not find an incumbent. A 600-second CP-SAT attempt on the reported 47 by 99 rectangle also returned `UNKNOWN`, after 11,688,881 branches and 737,300 conflicts. These attempts are not used as results.

Validation command: `.venv/bin/python -m pytest tasks/t099/test_task.py -q` (8 passed). JSON files were parsed with `.venv/bin/python -m json.tool`. The public witness, the self-generated seed, and all five program entries are checked by `check.py`.

## Review state

`accepted_by_sol`. The 270-copy public construction is a verified feasible upper bound, not a proof of optimality.
