# T003 implementation and review evidence

## Fixed configurations

C01 fixes 26 circles and C02 fixes 32 circles. Their accepted human baselines and best records are retained unchanged. C03 fixes 40 circles with variable positive radii in a unit square and maximizes the exact sum of radii.

The checker maps each configuration ID to its fixed order and rejects conflicting `n`, container, or radii parameters. It checks positive radii, all four walls, and all pair distances with exact rational arithmetic. It does not inspect a candidate-declared objective.

## C03 comparison and witness

Packomania's variable-radius square-packing table (last update 2026-10-31) lists N=40 with sum 3.292391572608 and cites reference [8]. Its official coordinate file is archived at `data/packomania40_source.txt`. The rounded source coordinates were translated from centered coordinates and all radii were reduced by 611401/10^18, the minimum common decrement on that grid that yields exact feasibility. Exact recomputation gives 82309789314588599/25000000000000000. The public witness remains the reference comparison only. Its source attribution is not confirmed as human. C03 human H instead uses the classical equal-circle order-40 packing by R. L. Graham and B. D. Lubachevsky (1996), cited as [11] by the equal-circle Packomania table; its saved coordinates pass exact feasibility with unchanged radius, giving sum 79186752517/25000000000. `task.json` freezes this human value. The displayed table value remains separate and is not claimed to be exactly reproduced.

C03 cold start is a self-contained 5 by 8 equal-radius grid with radius 1/16 and sum 2.5. The baseline and evolution programs generate from this seed and do not read comparison witnesses. The human/reference programs load saved external witness files only.

The full T003 test suite checks all three orders, exact witness scores, invalid dimensions and walls, overlaps, ignored claimed objectives, config-ID/parameter mismatch, deterministic evolution, exact feasibility, and bounded search behavior. New C03 status is accepted by Sol on 2026-11-07.
