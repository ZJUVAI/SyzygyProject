"""Bounded structural search for ordinary addition chains.

Exponent chains, positive tails and exact dependency graph choices generate
new chains. Only public targets and runner-supplied owned starts are read.
"""
import json
import os
import random
import time

TARGETS = {
    "T020-C01": 2**192 - 2**64 - 3,
    "T020-C02": 2**221 - 5,
    "T020-C03": 2**521 - 3,
}


def _chain_for_widths(target, widths, prefix_override=None):
    bits = bin(target)[2:]
    # Start with the leading run of one-bits. This permits a monotone odd
    # precomputation table whose final entry is also the accumulator prefix.
    prefix_len = 1
    if prefix_override is None:
        while prefix_len < min(max(widths), len(bits)) and bits[prefix_len] == "1":
            prefix_len += 1
    else:
        prefix_len = min(prefix_override, len(bits))
        while prefix_len > 1 and bits[prefix_len - 1] != "1":
            prefix_len -= 1
    prefix = (1 << prefix_len) - 1
    chain = [1]
    odd = {1: 0}
    if prefix_len > 1:
        chain.append(2)
        for value in range(3, prefix + 1, 2):
            chain.append(chain[odd[value - 2]] + 2)
            odd[value] = len(chain) - 1
    current = prefix
    i = prefix_len
    segment = 0
    while i < len(bits):
        w = widths[segment % len(widths)]
        if prefix_override is not None:
            w = min(w, prefix_len)
        segment += 1
        if bits[i] == "0":
            current *= 2
            chain.append(current)
            i += 1
            continue
        end = min(i + w, len(bits))
        while bits[end - 1] == "0":
            end -= 1
        digit = int(bits[i:end], 2)
        for _ in range(end - i):
            current *= 2
            chain.append(current)
        current += chain[odd[digit]]
        chain.append(current)
        i = end
    return chain


def _prune(chain):
    """Keep a valid dependency closure for the endpoint, dropping dead nodes."""
    needed = {len(chain) - 1}
    index = {value: i for i, value in enumerate(chain)}
    for i in range(len(chain) - 1, 0, -1):
        if i not in needed:
            continue
        value = chain[i]
        # Prefer a balanced witness; each operand is strictly earlier.
        witness = None
        for j in range(i - 1, -1, -1):
            k = index.get(value - chain[j])
            if k is not None and k <= j:
                witness = (j, k)
                break
        if witness is None:
            return chain
        needed.update(witness)
    return [v for i, v in enumerate(chain) if i in needed]


def _witnesses(chain):
    """Return every earlier addition pair available for each chain entry."""
    positions = {value: i for i, value in enumerate(chain)}
    result = [()] * len(chain)
    for i in range(1, len(chain)):
        pairs = []
        for j in range(i - 1, -1, -1):
            k = positions.get(chain[i] - chain[j])
            if k is not None and k <= j:
                pairs.append((j, k))
        result[i] = tuple(pairs)
    return result


def _alternate_prune(chain, rng, mode, pairs=None):
    """Choose alternate exact witnesses and retain only their dependency closure."""
    if pairs is None:
        pairs = _witnesses(chain)
    chosen = {len(chain) - 1}
    expanded = set()
    stack = [len(chain) - 1]
    while stack:
        i = stack.pop()
        if i == 0 or i in expanded:
            continue
        expanded.add(i)
        options = pairs[i]
        if not options:
            return chain

        def rank(pair):
            j, k = pair
            new = int(j not in chosen) + int(k not in chosen)
            if mode == 0:
                return (new, -(j + k), abs(j-k), rng.random())
            if mode == 1:
                return (new, -max(j, k), -(j+k), rng.random())
            if mode == 2:
                return (new, abs(j-k), -(j+k), rng.random())
            return (new + rng.randrange(3), rng.random(), abs(j-k))

        j, k = min(options, key=rank)
        for dep in (j, k):
            if dep not in chosen:
                chosen.add(dep)
                stack.append(dep)
    return [value for i, value in enumerate(chain) if i in chosen]


_EXPONENT_PATHS = {}


def _star_exponents(target, deadline):
    """Find a short star addition chain for a small exponent by bounded DFS."""
    path = [1]
    visits = 0
    def visit(left):
        nonlocal visits
        visits += 1
        if visits % 256 == 0 and time.monotonic() >= deadline:
            raise TimeoutError
        last = path[-1]
        if left == 0:
            return path.copy() if last == target else None
        if last << left < target:
            return None
        seen = set()
        for operand in reversed(path):
            value = last + operand
            if value > target or value in seen or value << (left - 1) < target:
                continue
            seen.add(value)
            path.append(value)
            result = visit(left - 1)
            path.pop()
            if result is not None:
                return result
        return None
    try:
        for depth in range((target - 1).bit_length(), target.bit_length() + target.bit_count() - 1):
            result = visit(depth)
            if result:
                return result
    except TimeoutError:
        pass
    return None


def _expand_exponent_path(path):
    """Lift e=a+b to M_e=2**b M_a+M_b with exact addition witnesses."""
    chain = [1]
    for old, exponent in zip(path, path[1:]):
        delta = exponent - old
        value = (1 << old) - 1
        for _ in range(delta):
            value *= 2
            chain.append(value)
        chain.append(value + (1 << delta) - 1)
    return chain


def _three_part_candidate(p):
    # N = 2**(192-p) M_p + 2**65 M_(127-p) + (8 M_61+5).
    paths = [_mersenne_chain(61), _mersenne_chain(p)]
    if p < 127:
        paths.append(_mersenne_chain(127-p))
    values = {1, 2, 3, 5}
    for path in paths:
        values.update(path)
    small = 8*((1 << 61)-1)+5
    values.update([2*((1 << 61)-1),4*((1 << 61)-1),8*((1 << 61)-1),small])
    terms = [small]
    for e, shift in ((p,192-p),(127-p,65)):
        if not e:
            continue
        value = (1 << e)-1
        for _ in range(shift):
            value *= 2
            values.add(value)
        terms.append(value)
    terms.sort()
    value = terms[0]
    for term in terms[1:]:
        value += term
        values.add(value)
    return sorted(values)


def _mersenne_chain(exponent):
    """Build 2**exponent-1 from the binary addition chain of exponent."""
    if exponent in _EXPONENT_PATHS:
        return _expand_exponent_path(_EXPONENT_PATHS[exponent])
    chain = [1]
    current_exponent = 1
    for bit in bin(exponent)[3:]:
        base = chain[-1]
        value = base
        for _ in range(current_exponent):
            value *= 2
            chain.append(value)
        value += base
        chain.append(value)
        current_exponent *= 2
        if bit == "1":
            value *= 2
            chain.append(value)
            value += 1
            chain.append(value)
            current_exponent += 1
    return chain


def _mersenne_split_chain(exponent, low_exponent):
    """Build M_(a+b) from M_a and M_b, where M_n = 2**n - 1."""
    if not 0 < low_exponent < exponent:
        raise ValueError("split must have two positive parts")
    high_exponent = exponent - low_exponent
    high = _mersenne_chain(high_exponent)
    low = _mersenne_chain(low_exponent)
    scaled = []
    value = high[-1]
    for _ in range(low_exponent):
        value *= 2
        scaled.append(value)
    scaled.append(value + low[-1])
    # Each input path has exact witnesses. The values from both paths and the
    # scaled path can be merged in increasing order because all witnesses are
    # smaller than their result.
    return sorted(set(high) | set(low) | set(scaled))


def _split_structured_candidate(cid, low_exponent):
    if cid == "T020-C02":
        exponent, trailing_doublings, tail = 218, 3, 3
    elif cid == "T020-C03":
        exponent, trailing_doublings, tail = 519, 2, 1
    else:
        return None
    chain = _mersenne_split_chain(exponent, low_exponent)
    for _ in range(trailing_doublings):
        chain.append(chain[-1] * 2)
    chain.append(chain[-1] + tail)
    return chain


def _structured_candidate(cid):
    """Use 2**(a+b)-1 = 2**b*(2**a-1) + (2**b-1)."""
    if cid == "T020-C03":
        chain = _mersenne_chain(519)
        for _ in range(2):
            chain.append(chain[-1] * 2)
        chain.append(chain[-1] + 1)
        return chain
    if cid == "T020-C02":
        chain = _mersenne_chain(218)
        for _ in range(3):
            chain.append(chain[-1] * 2)
        chain.append(chain[-1] + 3)
        return chain
    # 2**192-2**64-3 = 2**65*(2**127-1) + (2**64-3),
    # and 2**64-3 = 8*(2**61-1)+5. Merge the two independently
    # constructed chains in increasing order; their addition witnesses remain.
    m61 = _mersenne_chain(61)
    m61_value = m61[-1]
    # Build the smaller addend and M127 from the same M61 prefix. These
    # independent monotone paths can be merged by value while retaining every
    # addition witness.
    small_part = [m61_value * 2, m61_value * 4, m61_value * 8,
                  m61_value * 8 + 5]
    m63_path = [m61_value * 2, m61_value * 4]
    m63_path.append(m63_path[-1] + 3)
    m126_path = []
    value = m63_path[-1]
    for _ in range(63):
        value *= 2
        m126_path.append(value)
    value += m63_path[-1]
    m126_path.append(value)
    m127_path = [value * 2, value * 2 + 1]
    value = m127_path[-1]
    merged = sorted(set(m61) | {1, 2, 3, 5} | set(small_part) |
                    set(m63_path) | set(m126_path) | set(m127_path))
    base = value
    # The final scale terms are larger than every merged entry.
    for _ in range(65):
        base *= 2
        merged.append(base)
    merged.append(base + small_part[-1])
    return merged


def _near_power_search(cid, best, rng, deadline):
    """Search new structural DAGs and merge their exact dependency choices."""
    from tasks.t020.structured_search import (
        binary_chain, divisors_for_target, exponent_search,
        quotient_chain, tail_candidate,
    )
    bits, defect = (221, 5) if cid == "T020-C02" else (521, 3)
    target = (1 << bits)-defect
    minimum = defect.bit_length()
    splits = list(range(minimum, min(bits-1, 65)))
    splits += [bits-e for e in range(2, bits) if e & (e-1) == 0]
    splits = sorted(set(splits))
    rng.shuffle(splits)
    paths = dict(_EXPONENT_PATHS)
    archive = [best]
    counts = {"tail_proposals": 0, "quotient_proposals": 0,
              "ordinary_exponent_searches": 0, "dependency_merges": 0}
    round_number = 0
    while time.monotonic() < deadline:
        trailing = splits[round_number % len(splits)] if round_number < len(splits) else rng.choice(splits)
        exponent = bits-trailing
        general = round_number % 5 == 0
        path = exponent_search(exponent, rng, min(deadline, time.monotonic()+0.07),
                               node_limit=14000, general=general)
        counts["ordinary_exponent_searches"] += int(general)
        old = paths.get(exponent)
        if old is None or len(path) <= len(old):
            paths[exponent] = path
        elif rng.random() < 0.8:
            path = old
        proposal = tail_candidate(bits, defect, trailing, path, rng)
        proposals = [proposal]
        counts["tail_proposals"] += 1
        if round_number % 3 == 0:
            for divisor in divisors_for_target(target, rng):
                if 1 < divisor < target:
                    proposals.append(quotient_chain(target, divisor, paths, rng))
                    counts["quotient_proposals"] += 1
        for raw in proposals:
            if time.monotonic() >= deadline:
                break
            candidate = _prune(raw)
            if len(candidate) < len(best):
                best = candidate
            # Keep near-best alternatives. Merging them can create valid
            # non-star witnesses that neither original dependency DAG used.
            if len(candidate) <= len(best)+4 and candidate not in archive:
                archive.append(candidate)
                archive.sort(key=len)
                if len(archive) > 20:
                    del archive[rng.randrange(10, len(archive))]
            if len(candidate) <= len(best)+8 and round_number % 2 == 0:
                union = sorted(set(candidate) | set(rng.choice(archive)) | set(range(1,33)))
                pairs = _witnesses(union)
                counts["dependency_merges"] += 1
                for mode in range(4):
                    reduced = _alternate_prune(union, rng, mode, pairs)
                    if len(reduced) < len(best):
                        best = reduced
                        archive.insert(0, reduced)
        round_number += 1
    return best, counts


def _shared_target_search(best, rng, deadline):
    """Search shared exponent paths and Euclidean DAGs for the sparse defect."""
    from tasks.t020.structured_search import (
        append_tail, binary_chain, exponent_search, lift_exponents,
        quotient_chain,
    )
    target = TARGETS['T020-C01']
    archive = [best]
    rounds = 0
    counts = {'shared_exponent_proposals': 0, 'quotient_proposals': 0,
              'dependency_merges': 0}
    while time.monotonic() < deadline:
        rounds += 1
        exponent = rng.choice((59, 60, 61, 62))
        path = exponent_search(exponent, rng, min(deadline,time.monotonic()+0.025),
                               node_limit=5000, general=rounds%7==0)
        # Extend the same exponent chain to 127. Every proposed step has an
        # earlier pair, and lifting retains exact ordinary-addition witnesses.
        prefix = path[:]
        def extend(left):
            last = prefix[-1]
            if last == 127:
                return prefix[:]
            if not left or last << left < 127:
                return None
            values = list({last+x for x in prefix if last+x <= 127})
            rng.shuffle(values)
            for value in values:
                prefix.append(value)
                answer=extend(left-1)
                prefix.pop()
                if answer is not None:
                    return answer
            return None
        full_path = None
        for depth in (2,3,4,5):
            full_path=extend(depth)
            if full_path is not None:
                break
        proposals=[]
        if full_path is not None:
            values=set(lift_exponents(full_path,rng))
            trailing=64-exponent
            tail=(1 << trailing)-3
            if tail <= 0:
                raise ValueError('shared exponent split requires a positive tail')
            values=set(append_tail(sorted(values),tail))
            value=(1 << exponent)-1
            for _ in range(trailing):
                value*=2
                values.add(value)
            small=value+tail
            values.add(small)
            value=(1 << 127)-1
            for _ in range(65):
                value*=2
                values.add(value)
            values.add(value+small)
            proposals.append(sorted(values))
            counts['shared_exponent_proposals']+=1
        if rounds%4==0:
            shift=rng.randrange(3,128)
            divisor=(1 << shift)-rng.choice((1,3,5))
            proposals.append(quotient_chain(target,divisor,{},rng))
            counts['quotient_proposals']+=1
        for proposal in proposals:
            candidate=_prune(proposal)
            if len(candidate)<len(best):
                best=candidate
            if len(candidate)<=len(best)+6:
                if candidate not in archive:
                    archive.append(candidate)
                    archive.sort(key=len)
                    del archive[16:]
                union=sorted(set(candidate)|set(rng.choice(archive))|set(range(1,33)))
                pairs=_witnesses(union)
                counts['dependency_merges']+=1
                for mode in range(4):
                    candidate=_alternate_prune(union,rng,mode,pairs)
                    if len(candidate)<len(best):
                        best=candidate
    return best, counts


def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T020-C01")
    target = TARGETS.get(cid)
    if target is None:
        raise ValueError("unsupported T020 configuration")
    try:
        budget = max(0.01, min(240.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45"))))
    except ValueError:
        budget = 45.0
    deadline = time.monotonic() + budget
    try:
        seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    except ValueError:
        seed = 0
    rng = random.Random(seed)
    best = _prune(_chain_for_widths(target, (1,)))
    candidates_considered = 1
    # Search small exponent chains first. A star step with increment b lifts
    # to b doublings and one addition; all large integer steps remain exact.
    exponents = (61, 63, 127) if cid == "T020-C01" else ((218,) if cid == "T020-C02" else (519,))
    exponent_deadline = min(deadline, time.monotonic() + min(20.0, budget * 0.25))
    for exponent in exponents:
        path = _star_exponents(exponent, exponent_deadline)
        if path is not None:
            _EXPONENT_PATHS[exponent] = path
    structured = _prune(_structured_candidate(cid))
    candidates_considered += 1
    if structured[-1] == target and len(structured) < len(best):
        best = structured
    if cid in ("T020-C02", "T020-C03"):
        exponent = 218 if cid == "T020-C02" else 519
        split_values = {1, 2, 3, 4, 5, 7, 8, 15, 16, 31, 32,
                        exponent // 2, exponent // 2 + 1}
        split_values.update(1 << k for k in range(1, exponent.bit_length() - 1))
        for low in sorted(x for x in split_values if 0 < x < exponent):
            if time.monotonic() >= deadline:
                break
            raw = _split_structured_candidate(cid, low)
            candidate = _prune(raw)
            candidates_considered += 1
            if candidate[-1] == target and len(candidate) < len(best):
                best = candidate
    # The runner may supply this task's own saved incumbent. Check it exactly;
    # the search remains valid as a cold run when no warm start is present.
    warm_path = os.environ.get("MATHBENCH_WARM_START")
    if warm_path:
        try:
            with open(warm_path, encoding="utf-8") as stream:
                warm = json.load(stream)
            from tasks.t020.check import validate
            label = os.environ.get("MATHBENCH_CONFIG_ID", "T020-C01")
            target_text = {"T020-C01": "2^192-2^64-3", "T020-C02": "2^221-5",
                           "T020-C03": "2^521-3"}[label]
            validate(warm, {"id": label, "parameters": {"target": target_text}}, strict=True)
            if warm["chain"][-1] == target and len(warm["chain"]) < len(best):
                best = warm["chain"]
                candidates_considered += 1
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            pass
    if cid == "T020-C01":
        for p in range(65, 128):
            if time.monotonic() >= deadline:
                break
            for exponent in (p, 127-p):
                if exponent > 1 and exponent not in _EXPONENT_PATHS:
                    path = _star_exponents(exponent, min(deadline, time.monotonic()+0.05))
                    if path is not None:
                        _EXPONENT_PATHS[exponent] = path
            candidate = _prune(_three_part_candidate(p))
            candidates_considered += 1
            if len(candidate) < len(best):
                best = candidate
    if cid == 'T020-C03':
        # Alternative small precomputations can reuse the tail value at no
        # extra cost. Every added integer is certified by 1+(value-1).
        from tasks.t020.structured_search import tail_candidate
        path = _star_exponents(518, min(deadline,time.monotonic()+0.1))
        if path is not None:
            augmented=sorted(set(tail_candidate(521,3,3,path))|set(range(1,33)))
            pairs=_witnesses(augmented)
            for mode in range(16):
                candidate=_alternate_prune(augmented,rng,mode%4,pairs)
                if len(candidate)<len(best):
                    best=candidate
    if cid in ("T020-C02", "T020-C03"):
        best, counts = _near_power_search(cid, best, rng, deadline)
        return {"chain": best, "search_metadata": {
            **counts, "candidates_considered": candidates_considered + counts["tail_proposals"] + counts["quotient_proposals"],
            "search_method": "ordinary exponent DFS, variable Mersenne tails, Euclidean quotient DAGs, merged dependency closures",
            "addition_count": len(best)-1, "chain_entries": len(best),
        }}
    best, counts = _shared_target_search(best, rng, deadline)
    return {'chain':best,'search_metadata':{
        **counts, 'search_method':'shared forced exponent paths, Euclidean DAGs and merged dependency closures',
        'addition_count':len(best)-1,'chain_entries':len(best)}}
