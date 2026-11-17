"""Read packed adjacency for a simple undirected graph."""

import hashlib


def load_adjacency(path, vertices, edges, sha256):
    """Read verified bytes and return one integer neighbor mask per vertex."""
    data = path.read_bytes()
    pair_count = vertices * (vertices - 1) // 2
    if len(data) != (pair_count + 7) // 8:
        raise RuntimeError("packed graph has the wrong byte count")
    if pair_count % 8 and data[-1] >> (pair_count % 8):
        raise RuntimeError("packed graph has nonzero padding")
    if hashlib.sha256(data).hexdigest() != sha256:
        raise RuntimeError("packed graph hash does not match the fixed input")
    if sum(byte.bit_count() for byte in data) != edges:
        raise RuntimeError("packed graph has the wrong edge count")

    adjacency = [0] * vertices
    for v in range(1, vertices):
        start = v * (v - 1) // 2
        stop = start + v
        row_bytes = data[start // 8:(stop + 7) // 8]
        lower_neighbors = (int.from_bytes(row_bytes, "little") >> (start % 8)) & ((1 << v) - 1)
        adjacency[v] |= lower_neighbors
        upper_bit = 1 << v
        while lower_neighbors:
            edge_bit = lower_neighbors & -lower_neighbors
            adjacency[edge_bit.bit_length() - 1] |= upper_bit
            lower_neighbors ^= edge_bit
    return tuple(adjacency)
