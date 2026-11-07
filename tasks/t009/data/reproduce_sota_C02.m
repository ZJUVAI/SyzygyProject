// Public Magma Calculator, version 2.30-1; checked 2026-11-07.
SetColumns(0);
C, has_code := BestKnownLinearCode(GF(2), 80, 20);
assert has_code;
assert MinimumDistance(C) eq 25;
MinimumDistance(C);
