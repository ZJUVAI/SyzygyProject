"""Local evolution for finite integer sum-difference sets.

Use the simple seed or a runner-supplied own witness. Exact bit supports speed
small-set search. Periodic interior expansion explores larger constructions.
The checker decides which final construction is retained.
"""
from collections import Counter
import math
import json
import os
import random
import time

from tasks.t012.check import validate
from tasks.t012.init_program import run_code as initial_program


_CONFIG = {"id": "T012-C01", "parameters": {
    "max_cardinality": 512, "integer_interval": [-1000000, 1000000]}}
_LOW, _HIGH = -1_000_000, 1_000_000


def _measure(values):
    """Return (score, sum size, difference size), or None when undefined."""
    n = len(values)
    sums = {a + b for a in values for b in values}
    diffs = {a - b for a in values for b in values}
    s, d = len(sums), len(diffs)
    if s <= d or d <= n:
        return None
    return math.log(s / n) / math.log(d / n), s, d


def _incremental_measure(before, after, sums, diffs):
    """Update exact representation counts only for changed points."""
    sums, diffs = sums.copy(), diffs.copy()
    live = set(before)
    def change(counter, key, delta):
        counter[key] += delta
        if counter[key] == 0:
            del counter[key]
    for x in set(before) - set(after):
        live.remove(x)
        change(sums, 2*x, -1)
        change(diffs, 0, -1)
        for y in live:
            change(sums, x+y, -1)
            change(diffs, x-y, -1)
            change(diffs, y-x, -1)
    for x in set(after) - set(before):
        change(sums, 2*x, 1)
        change(diffs, 0, 1)
        for y in live:
            change(sums, x+y, 1)
            change(diffs, x-y, 1)
            change(diffs, y-x, 1)
        live.add(x)
    n = len(after)
    score = None if len(sums) <= len(diffs) or len(diffs) <= n else math.log(len(sums)/n)/math.log(len(diffs)/n)
    return score, sums, diffs


def _counts(values):
    return (Counter(a+b for i,a in enumerate(values) for b in values[i:]),
            Counter(a-b for a in values for b in values))


def _proposal(current, rng):
    """Make a local or structured edit at several coordinate scales."""
    trial = current.copy()
    mode = rng.random()
    if mode < 0.16:
        # Keep the two fringes and vary a dense middle interval. This changes
        # cross-fringe sums without using a score-invariant global transform.
        ordered = sorted(trial)
        low, high = ordered[0], ordered[-1]
        fringe = rng.randint(2, min(12, max(2, (high-low)//2)))
        shift = rng.choice((-3, -2, -1, 1, 2, 3, 6, 12))
        split = (low + high)//2
        trial = [x for x in ordered if x <= low+fringe]
        trial += [x+shift for x in ordered if x >= high-fringe and x > low+fringe]
        left, right = low+fringe+1, high-fringe+shift
        trial += list(range(left, max(left, right)))
        trial = sorted(set(trial))
        if len(trial)>512 or any(x < _LOW or x > _HIGH for x in trial):
            return current[:]
    elif mode < 0.48:
        # Move one existing point by a short amount. Occasionally move it
        # farther, while keeping the rest of a structured core intact.
        i = rng.randrange(len(trial))
        scale = rng.choice((1, 2, 3, 4, 6, 8, 12, 20, 40, 80, 160, 320))
        delta = rng.choice((-scale, scale))
        value = trial[i] + delta
        if _LOW <= value <= _HIGH and value not in trial:
            trial[i] = value
    elif mode < 0.68 and len(trial) < 512:
        # Prefer adding near the current fringe or in a small gap. A rare
        # wider move explores a new fringe without spraying huge coordinates.
        ordered = sorted(trial)
        if rng.random() < 0.72:
            gap = rng.randrange(len(ordered) - 1)
            left, right = ordered[gap], ordered[gap + 1]
            if right - left > 1:
                value = rng.randint(left + 1, right - 1)
            else:
                value = ordered[0] - rng.randint(1, 8) if rng.random() < .5 else ordered[-1] + rng.randint(1, 8)
        else:
            span = max(8, ordered[-1] - ordered[0])
            value = (ordered[0] if rng.random() < .5 else ordered[-1]) + rng.choice((-1, 1)) * rng.randint(1, min(span, 64))
        if _LOW <= value <= _HIGH and value not in trial:
            trial.append(value)
    elif mode < 0.80:
        # Deletion is useful for pruning points that inflate A-A.
        if len(trial) > 2:
            trial.pop(rng.randrange(len(trial)))
    elif mode < 0.91:
        # Shift a short consecutive block. This preserves local structure
        # while changing its interaction with the rest of the set.
        ordered = sorted(trial)
        start = rng.randrange(len(ordered))
        width = rng.randint(1, min(4, len(ordered) - start))
        block = ordered[start:start + width]
        delta = rng.choice((-1, 1)) * rng.choice((1, 2, 4, 8, 16, 32, 64))
        moved = [x + delta for x in block]
        rest = set(ordered) - set(block)
        if all(_LOW <= x <= _HIGH for x in moved) and not rest.intersection(moved):
            trial = sorted(rest.union(moved))
    else:
        # Reflect a randomly selected block around its midpoint, optionally
        # then translate it. Reflection and translation preserve its shape.
        ordered = sorted(trial)
        start = rng.randrange(len(ordered))
        width = rng.randint(2, min(5, len(ordered) - start)) if len(ordered) - start >= 2 else 1
        block = ordered[start:start + width]
        pivot_sum = block[0] + block[-1]
        shift = rng.choice((-1, 0, 1)) * rng.choice((0, 2, 8, 24))
        moved = [pivot_sum - x + shift for x in block]
        rest = set(ordered) - set(block)
        if all(_LOW <= x <= _HIGH for x in moved) and len(set(moved)) == len(moved) and not rest.intersection(moved):
            trial = sorted(rest.union(moved))
    return sorted(trial)


def _python_run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T012-C01") != "T012-C01":
        raise ValueError("unsupported configuration")
    try:
        budget = max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    except (TypeError, ValueError):
        budget = 45.0
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    deadline = time.monotonic() + budget

    # Normalize ordering and deduplicate the supplied cold-start seed. The
    # exact checker establishes the incumbent before search begins.
    best = sorted(set(initial_program()["set"]))
    warm_path = os.environ.get("MATHBENCH_WARM_START")
    if warm_path:
        with open(warm_path, encoding="utf-8") as stream:
            warm = json.load(stream)
        warm_values = sorted(set(warm["set"]))
        # The runner supplies only this task's own archived best. Still
        # validate it here before it can become the search incumbent.
        warm_result = validate({"set": warm_values}, _CONFIG)
        if float(warm_result["objective"]) > float(validate({"set": best}, _CONFIG)["objective"]):
            best = warm_values
    checked = validate({"set": best}, _CONFIG)
    best_score = float(checked["objective"])
    def fast_measure(values):
        values = sorted(values)
        n = len(values)
        if n < 3:
            return None
        low, high = values[0], values[-1]
        if high-low > 100000:
            result = _measure(values)
            return None if result is None else result[0]
        points = [v-low for v in values]
        bits = sum(1 << v for v in points)
        sum_bits = diff_bits = 0
        for v in points:
            sum_bits |= bits << v
            diff_bits |= bits << (high-low-v)
        ns, nd = sum_bits.bit_count(), diff_bits.bit_count()
        if nd <= n:
            return None
        return math.log(ns/n)/math.log(nd/n)

    current = best[:]
    current_score = best_score
    iteration = restarts = 0
    cycle_started = time.monotonic()
    while time.monotonic() < deadline:
        iteration += 1
        now = time.monotonic()
        if now-cycle_started > 1.5:
            restarts += 1
            current = best[:]
            if restarts % 4 == 0:
                span = rng.randint(18, 100)
                density = rng.uniform(.35, .85)
                current = [i for i in range(span) if rng.random()<density]
                if len(current)<3:
                    current = best[:]
            else:
                for _ in range(1+restarts%5):
                    current = _proposal(current, rng)
            current_score = fast_measure(current)
            if current_score is None:
                current, current_score = best[:], best_score
            cycle_started = now
        trial = _proposal(current, rng)
        score = fast_measure(trial)
        if score is None:
            continue
        # Short cooling cycles keep the search near promising small sets.
        phase = min(1.0, (now-cycle_started)/1.5)
        temperature = .004*(1-phase)**2 + .00003
        if score>=current_score or rng.random()<math.exp(max(-700,(score-current_score)/temperature)):
            current, current_score = trial, score
        if score > best_score + 1e-14:
            result = validate({"set": trial}, _CONFIG)
            exact_score = float(result["objective"])
            if exact_score > best_score:
                best, best_score = trial, exact_score

    # Recheck the archived construction at the return boundary.
    validate({"set": best}, _CONFIG)
    return {"set": best, "search_metadata": {"iterations": iteration, "restarts": restarts, "budget_seconds": budget, "method": "integer bitset sum-difference evaluation with short annealing cycles"}}



def _bit_score(values):
    """Compute support cardinalities with exact Python integer bit operations."""
    points=sorted(values)
    if len(points)<3:
        return -1.0
    low=points[0];points=[x-low for x in points];high=points[-1]
    bits=sum(1<<x for x in points);sums=diffs=0
    for x in points:
        sums|=bits<<x;diffs|=bits<<(high-x)
    n=len(points);ns=sums.bit_count();nd=diffs.bit_count()
    return -1.0 if nd<=n else math.log(ns/n)/math.log(nd/n)


def _expand_and_polish(values,deadline,rng):
    """Repeat interior patterns, then search local edits under the size bound."""
    base=sorted(values);base=[x-min(base) for x in base]
    best=base[:];best_score=_bit_score(best);trials=0
    periods=list(range(1,min(49,max(base))));rng.shuffle(periods)
    for period in periods:
        if time.monotonic()>=deadline:
            break
        for cut in range(1,max(base)-period):
            low=[x for x in base if x<cut]
            block=[x for x in base if cut<=x<cut+period]
            high=[x for x in base if x>=cut+period]
            if not block:
                continue
            max_k=(512-len(base))//len(block)
            ks=sorted({1,2,4,8,16,32,64,128,max_k})
            for k in ks:
                if k<1 or k>max_k:
                    continue
                trial=low+[x+j*period for j in range(k+1) for x in block]+[x+k*period for x in high]
                score=_bit_score(trial);trials+=1
                if score>best_score:
                    best,best_score=trial,score
            if time.monotonic()>=deadline:
                break
    current=sorted(best);current_score=best_score
    while time.monotonic()<deadline:
        trial=_proposal(current,rng)
        if max(trial)-min(trial)>100000:
            continue
        score=_bit_score(trial);trials+=1
        temperature=.00025
        if score>=current_score or rng.random()<math.exp(max(-700,(score-current_score)/temperature)):
            current,current_score=trial,score
        if score>best_score:
            best,best_score=trial,score
        if trials%1000==0:
            current,current_score=sorted(best),best_score
    return sorted(best),trials

def run_code():
    """Use exact bit supports for fast search within a 64-position interval."""
    import subprocess
    import tempfile
    import shutil
    if shutil.which("g++") is None:
        return _python_run_code()
    from pathlib import Path
    budget = max(.1,float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS","45")))
    seed = int(os.environ.get("MATHBENCH_SEED","0"))
    start = time.monotonic()
    best = sorted(initial_program()["set"])
    warm = os.environ.get("MATHBENCH_WARM_START")
    if warm:
        candidate = json.loads(Path(warm).read_text())["set"]
        if float(validate({"set":candidate},_CONFIG)["objective"])>float(validate({"set":best},_CONFIG)["objective"]):
            best = sorted(candidate)
    shifted = [v-min(best) for v in best]
    if max(shifted)>63:
        return _python_run_code()
    run_dir=Path(__file__).resolve().parent/"runs"
    run_dir.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sets_kernel_",dir=run_dir) as folder:
        executable=str(Path(folder)/"sets")
        subprocess.run(["g++","-O3","-std=c++17",str(Path(__file__).with_name("search_sets.cpp")),"-o",executable],check=True,capture_output=True,timeout=30)
        remaining=max(.01,budget*.70-(time.monotonic()-start)-.1)
        result=subprocess.run([executable,str(remaining),str(seed)],input=str(len(shifted))+"\n"+" ".join(map(str,shifted))+"\n",capture_output=True,text=True,check=True,timeout=remaining+5)
    numbers=list(map(int,result.stdout.split()))
    iterations,restarts=numbers[:2]
    candidate=numbers[2:]
    candidate,periodic_trials=_expand_and_polish(candidate,start+budget-.1,random.Random(seed+991))
    if float(validate({"set":candidate},_CONFIG)["objective"])>float(validate({"set":best},_CONFIG)["objective"]):
        best=candidate
    return {"set":best,"search_metadata":{"iterations":iterations,"restarts":restarts,"budget_seconds":budget,"periodic_trials":periodic_trials,"method":"compiled bit-support annealing, periodic interior expansion, and exact-support local polish"}}


if __name__ == "__main__":
    print(run_code())
