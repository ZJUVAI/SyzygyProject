# T002 implementation and review evidence

T002-C02 fixes 32 circles with positive radii in a unit square. The checker verifies every wall and all 496 circle pairs with exact rational arithmetic. It recomputes the sum of the radii.

The human baseline uses the 32-circle equal-radius coordinates in `csq32.txt`. The reconstructed witness is `human32.json`. Its exact sum is 2.811460994816.

The public variable-radius coordinates are in `packomania32_source.txt`. The table reports 2.939572771205. The generator `../reduce_sota.py` reduces each rounded radius by 566391/10^18. It checks all walls and pairs exactly. The next smaller decrement on the same grid fails a constraint. The exact replay of `sota32.json` gives 91861649099589859/31250000000000000. See [the source record](bestknown.json) for provenance and the difference from the displayed value.

The initial program uses a regular grid. The baseline and evolution start from a grid and compute their own constructions. They do not read the comparison witnesses.

The task tests cover the fixed configuration, exact witness scores, invalid walls and overlaps, ignored score claims, and the search budget controls.
