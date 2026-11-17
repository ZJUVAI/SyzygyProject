# T084: Ring loading discrepancy

For fixed `m=15`, choose feasible rational pairs `(u_i,v_i)`, with nonnegative entries and `u_i+v_i<=1`. A route chooses one of `v_i` and `-u_i` at each position. For one-based cuts `k=1,...,15`, its discrepancy is the maximum of `|sum_{i<=k} z_i - sum_{i>k} z_i|`. The objective is to maximize the minimum discrepancy over all routes.

The checker evaluates all 32,768 routes and 15 cuts with exact integer arithmetic after scaling by a common denominator. The Skutella Figure 2 human construction scores `11/10`; the pinned AlphaEvolve witness rationalized to denominator 84 scores `47/42`. Both witnesses are saved with SHA-256 hashes. The task remains accepted by Sol on 2026-11-09.
