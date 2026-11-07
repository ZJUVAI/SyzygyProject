# T070 implementation and verification record

## Configuration

- Configuration: `T070-C01`, integer-square dissection of the 1000 by 1000 square.
- Objective: minimize the number of tile squares.
- Constraints: positive integer sides below 1000; integer lower-left coordinates; full cover; no interior overlap; side gcd 1; compound dissections allowed.
- Reproduced public and human witness: 27 squares.
- Status: `accepted_by_sol`.

## Source and record status

The primary problem page defines a Mrs Perkins quilt as a square made from smaller integer squares whose side lengths have gcd 1. It distinguishes “primitive” from optimality and says most published values past order 18 have not been proved best possible. Ed Pegg Jr's July 2017 update includes a source row for outer side 1000 with 27 squares. The current source page lists A005670 exact values only through outer side 120. Ed Wynn's exhaustive search covers order at most 18. The 27-piece 1000-square construction is reproduced, but no proof of minimum order was found.

Only source row 1000 is kept under `data/source/`. The source ZIP SHA-256 is `ea43c7728ada8bec7fe93d4ffc3dfa88f3b37f0b6be9a36e1e8ea1b1b64bb98a`; the source TXT SHA-256 is `ec6b0f9b21eda14648de00317371cf6f07f456c72fab235fa9ecaaffe798c2e7`. The saved 110-byte row has SHA-256 `011cbfe1a1933cf20ba51f78f4c721ca447636bc4e52d8ea1255b7cb92a5e880`.

The saved 27-placement witness has SHA-256 `237d543109959c8939d22f98e91832d3bda47603cfe243f19a6e7beee0c7bfee`. The decoder reconstructs it from the listed side lengths by placing each square at the lowest available y coordinate, then the lowest x coordinate. The reconstructed placements match the saved witness exactly.

## Programs

- `check.py` rejects invalid integer data, checks the total tile area and gcd, then uses a 1000-bit mask per integer x-column. Each square contributes its vertical bit range to every covered column. Any repeated bit is an overlap. All 1000 masks must equal the full-column mask. This proves exact full coverage without floating-point arithmetic.
- `init_program.py` is standalone and returns 2000 tiles: one 999 square and the 1999 unit tiles in the top and right strips.
- `baseline.py` performs a finite scan over 15 uniform guillotine block counts. It refines one block with a Euclidean strip dissection, so every result has gcd 1.
- `evolution.py` mutates integer guillotine split plans. Each plan yields an exact rectangle dissection by Euclidean square tiling; a tile is refined if needed to make the side gcd 1.
- `human.py` reconstructs the 27-piece published construction from its source size row.
- `reference.py` replays the saved fixed witness.
- `evaluator.py` connects the shared runner.

The initial and search programs do not read comparison data. The human and reference programs read only the task-local source row or fixed reference file. No witness is placed under `best/`.

## Checks performed

Tests independently compare the 27 source sizes with the decoded witness, check area and gcd, and test all 351 pairs for interior overlap. They cover the initial construction, baseline, evolution, repeated tile sizes, overlap, missing area, non-coprime side lengths, bool/float/NaN values, invalid bounds, forged scores, and worker errors and timeouts.

Run commands:

```sh
.venv/bin/python -m pytest tasks/t070 -q
.venv/bin/python -m json.tool tasks/t070/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t070/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t070/records.json > /dev/null
```

Results:

- `.venv/bin/python -m pytest tasks/t070 -q`: 9 passed in 1.30 seconds on the final run.
- JSON parsing for `task.json`, `sota.json`, `records.json`, and `data/source/source_notes.json`: passed.
- Python environment: CPython 3.13.12, Linux x86_64. Runner limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one thread.
- Default traditional search replay with `MATHBENCH_CONFIG_ID=T070-C01`, seed 0, no time cutoff: all 15 divisor-based candidates checked, 0.394 seconds, exact checker score 299.
- Default evolutionary search replay with `MATHBENCH_CONFIG_ID=T070-C01`, seed 0, no time cutoff: 60/60 generations, population 6, 0.005 seconds, exact checker score 75.
- Replay commands: `.venv/bin/python -m tasks.t070.human` and `.venv/bin/python -m tasks.t070.reference`; each returns the 27-square published dissection.

Budgets are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one thread. Search uses fixed seeds and iteration counts unless `MATHBENCH_SEARCH_SECONDS` is explicitly set.
