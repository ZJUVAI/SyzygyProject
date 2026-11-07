"""Independent exact-cover search; uses only the fixed 11-cell shape."""
import json, random, sys, time
from pathlib import Path
from ortools.sat.python import cp_model

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261106
W = int(sys.argv[2]) if len(sys.argv) > 2 else 54
H = int(sys.argv[3]) if len(sys.argv) > 3 else 55
time_limit = int(sys.argv[4]) if len(sys.argv) > 4 else 1800
rng = random.Random(seed)
shape = {(x, 0) for x in range(5)} | {(x, y) for x in range(3) for y in (1, 2)}
placements = []
for orientation in range(8):
    cells=[]
    for x0,y0 in shape:
        x,y=x0,y0
        if orientation & 1: x,y=y,x
        if orientation & 2: x=-x
        if orientation & 4: y=-y
        cells.append((x,y))
    mx=min(x for x,y in cells); my=min(y for x,y in cells)
    cells={(x-mx,y-my) for x,y in cells}
    ww=max(x for x,y in cells)+1; hh=max(y for x,y in cells)+1
    for oy in range(H-hh+1):
        for ox in range(W-ww+1):
            placements.append((orientation,ox,oy,[(oy+y)*W+ox+x for x,y in cells]))
rng.shuffle(placements)
by_cell=[[] for _ in range(W*H)]
for i,p in enumerate(placements):
    for c in p[3]: by_cell[c].append(i)
model=cp_model.CpModel()
x=[model.new_bool_var(f'p{i}') for i in range(len(placements))]
for ids in by_cell: model.add(sum(x[i] for i in ids)==1)
solver=cp_model.CpSolver()
solver.parameters.max_time_in_seconds=time_limit
solver.parameters.num_search_workers=1
solver.parameters.random_seed=seed
solver.parameters.cp_model_presolve=True
solver.parameters.log_search_progress=True
print(f"seed={seed} W={W} H={H} placements={len(placements)} vars={len(x)}", flush=True)
t=time.time(); status=solver.solve(model); elapsed=time.time()-t
print(f"status={solver.status_name(status)} elapsed={elapsed:.3f} branches={solver.num_branches} conflicts={solver.num_conflicts}",flush=True)
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    out={"rectangle":[W,H],"placements":[{"orientation":p[0],"x":p[1],"y":p[2]} for i,p in enumerate(placements) if solver.value(x[i])]}
    path=f"tasks/t099/runs/research/cpsat_seed_{W}x{H}_{seed}.json"
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    open(path,'w').write(json.dumps(out,separators=(',',':'))+'\n')
    print(f"saved={path} tiles={len(out['placements'])}",flush=True)
