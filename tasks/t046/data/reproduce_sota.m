// Magma V2.30-1, public calculator, queried 2026-11-05.
// Prints the exact generator rows saved in sota_generator.json.
SetColumns(0);
C, has_code := BestKnownLinearCode(GF(2), 68, 15);
assert has_code;
G := GeneratorMatrix(C);
assert Nrows(G) eq 15 and Ncols(G) eq 68;
for i in [1..Nrows(G)] do
    for j in [1..Ncols(G)] do
        printf "%o", Integers()!G[i,j];
    end for;
    printf "\n";
end for;
