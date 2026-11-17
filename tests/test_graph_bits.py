import hashlib

import pytest

from mathbench.graph_bits import load_adjacency


def test_packed_adjacency_across_byte_boundary(tmp_path):
    graph = tmp_path / "graph.bits"
    data = b"\x41\x01"
    graph.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    assert load_adjacency(graph, 5, 3, digest) == (18, 1, 16, 0, 5)


@pytest.mark.parametrize(
    ("data", "edges", "use_own_hash", "error"),
    [
        (b"\x41", 3, True, "byte count"),
        (b"\x41\x81", 4, True, "padding"),
        (b"\x41\x02", 3, False, "hash"),
        (b"\x41\x01", 4, True, "edge count"),
    ],
)
def test_reject_invalid_packed_adjacency(tmp_path, data, edges, use_own_hash, error):
    graph = tmp_path / "graph.bits"
    graph.write_bytes(data)
    digest = hashlib.sha256(data if use_own_hash else b"\x41\x01").hexdigest()
    with pytest.raises(RuntimeError, match=error):
        load_adjacency(graph, 5, edges, digest)
