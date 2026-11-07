"""Fixed-order greedy maximal C6-free graph on 100 vertices."""

import os


N = 100


def _path5_exists(adjacency, start, target):
    if start == target or adjacency[start] & (1 << target):
        return False

    def visit(vertex, depth, seen):
        if depth == 5:
            return vertex == target
        choices = adjacency[vertex] & ~seen
        while choices:
            bit = choices & -choices
            choices ^= bit
            neighbor = bit.bit_length() - 1
            if neighbor == target:
                if depth == 4:
                    return True
            elif visit(neighbor, depth + 1, seen | bit):
                return True
        return False

    return visit(start, 0, 1 << start)


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T061-C01")
    if chosen != "T061-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    # EVOLVE-BLOCK-START
    adjacency = [0] * N
    edges = []
    for left in range(N):
        for right in range(left + 1, N):
            if not _path5_exists(adjacency, left, right):
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
                edges.append([left, right])
    return {"vertices": N, "edges": edges}
    # EVOLVE-BLOCK-END
