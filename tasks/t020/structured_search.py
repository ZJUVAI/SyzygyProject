"""Exact structural proposals for addition chains; no stored witness inputs."""
import math
import time


def binary_chain(target):
    chain = [1]
    for bit in bin(target)[3:]:
        chain.append(2 * chain[-1])
        if bit == '1':
            chain.append(chain[-1] + 1)
    return chain


def exponent_search(target, rng, deadline, node_limit=12000, general=False):
    """Bounded DFS over star or ordinary addition chains of a small integer.

    A failed bounded search is not a lower bound or an optimality claim.
    Ordinary steps can use any two previous entries, including neither last.
    """
    fallback = binary_chain(target)
    if target < 3:
        return fallback
    path = [1]
    visits = 0
    stopped = False

    def visit(left):
        nonlocal visits, stopped
        visits += 1
        if visits >= node_limit or (visits % 128 == 0 and time.monotonic() >= deadline):
            stopped = True
            return None
        last = path[-1]
        if last << left < target:
            return None
        if left == 1:
            if any(target - x in path for x in (path if general else [last])):
                return path + [target]
            return None
        if general:
            values = {x + y for i, x in enumerate(path) for y in path[:i+1]
                      if last < x+y < target and (x+y) << (left-1) >= target}
        else:
            values = {last + x for x in path if last+x < target and (last+x) << (left-1) >= target}
        values = sorted(values, reverse=True)
        # Random ordering visits distinct shortest paths with the same depth.
        if rng.random() < 0.65:
            rng.shuffle(values)
        for value in values:
            path.append(value)
            answer = visit(left - 1)
            path.pop()
            if answer is not None or stopped:
                return answer
        return None

    depths = list(range((target - 1).bit_length(), len(fallback)))
    # Each depth gets a fresh bounded search. An exhausted lower depth must
    # not prevent searching feasible depths with different exponent paths.
    if rng.random() < 0.7:
        rng.shuffle(depths)
    for depth in depths:
        visits = 0
        stopped = False
        answer = visit(depth)
        if answer is not None:
            return answer
        if time.monotonic() >= deadline:
            break
    return fallback


def lift_exponents(path, rng=None):
    """Lift any ordinary exponent chain, with both shift orientations.

    For e=a+b, M_e=2**b*M_a+M_b. A non-star step is allowed. All
    intermediate integer additions are retained before dependency pruning.
    """
    values = {1}
    prior = {1}
    for exponent in path[1:]:
        options = []
        for a in prior:
            b = exponent-a
            if b not in prior:
                continue
            base = (1 << a)-1
            extra = {base << shift for shift in range(1, b+1)}
            extra.add((1 << exponent)-1)
            options.append((len(extra-values), rng.random() if rng else b, extra))
        if not options:
            raise ValueError('invalid exponent addition chain')
        values.update(min(options, key=lambda item: item[:2])[2])
        prior.add(exponent)
    return sorted(values)


def append_tail(chain, tail):
    """Build a tail with exact sums and shift-and-add completions.

    All operands come from earlier values. Binary construction supplies
    a valid fallback when the bounded completion families do not help.
    """
    existing = {x for x in chain if x <= tail}
    if tail in existing:
        return chain
    candidates = set(binary_chain(tail)) | set(chain)
    # One new sum is common for tails close to a short Mersenne number.
    if any(tail-x in existing for x in existing):
        return sorted(set(chain) | {tail})
    # Search shift-and-add completions with small exact positive remainders.
    for shift in range(1, tail.bit_length()):
        quotient, remainder = divmod(tail, 1 << shift)
        if quotient not in existing or remainder not in existing | {0}:
            continue
        additions = {quotient << j for j in range(1, shift+1)} | {tail}
        proposal = set(chain) | additions
        if len(proposal) < len(candidates):
            candidates = proposal
    # Two new sums may exploit nonconsecutive earlier nodes.
    ordered = sorted(existing)
    for x in ordered:
        missing = tail-x
        if missing <= 0:
            continue
        if any(missing-y in existing for y in ordered if y < missing):
            proposal = set(chain) | {missing, tail}
            if len(proposal) < len(candidates):
                candidates = proposal
    return sorted(candidates)


def tail_candidate(bits, defect, trailing, path, rng=None):
    """Use 2**bits-c = 2**k*M_(bits-k) + (2**k-c)."""
    tail = (1 << trailing)-defect
    if tail <= 0 or path[-1] != bits-trailing:
        raise ValueError('invalid tail split')
    chain = append_tail(lift_exponents(path, rng), tail)
    value = (1 << path[-1])-1
    values = set(chain)
    for _ in range(trailing):
        value *= 2
        values.add(value)
    values.add(value+tail)
    return sorted(values)


def quotient_chain(target, divisor, paths, rng=None):
    """Build a target through an exact Euclidean quotient/remainder DAG.

    Multiplication by q is expanded as an addition chain scaled by a
    previously constructed value. All operations are ordinary additions.
    """
    values = {1}

    def scalar_path(q):
        if q <= 1024 and q in paths:
            return paths[q]
        exponent = q.bit_length()
        if q == (1 << exponent)-1:
            path = paths.get(exponent, binary_chain(exponent))
            return lift_exponents(path, rng)
        return binary_chain(q)

    def pair(a, b):
        if a < b:
            a, b = b, a
        if a in values and b in values:
            return
        if b == 1:
            values.update(scalar_path(a))
            return
        q, r = divmod(a, b)
        if r:
            pair(b, r)
        else:
            pair(b, 1)
        values.update(b*x for x in scalar_path(q))
        if r:
            values.add(a)

    if not 1 < divisor < target:
        raise ValueError('divisor must lie between 1 and target')
    pair(target, divisor)
    return sorted(values)


def divisors_for_target(target, rng):
    """Choose near-power, near-square, and small quotient decompositions."""
    bits = target.bit_length()
    shift = rng.randrange(2, bits-1)
    offset = rng.choice([-5, -3, -1, 0, 1, 3, 5])
    return [(1 << shift)+offset, (target >> shift)+offset,
            math.isqrt(target)+offset, target//rng.randrange(2, 33)]
