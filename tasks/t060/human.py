"""Gordon--Kuperberg--Patashnik (1995), finite geometry and induced coverings.

The restriction is an implementation choice, not the historical 23-block record.
"""
DELETED = {1, 8, 13, 15, 16, 24, 28, 31}


def run_code():
    points = sorted(set(range(32)) - DELETED)
    labels = {x: i for i, x in enumerate(points)}
    blocks = set()
    for normal in range(1, 32):
        for offset in (0, 1):
            plane = {x for x in range(32) if (normal & x).bit_count() % 2 == offset}
            assert len(plane & DELETED) >= 2
            block = {labels[x] for x in plane if x in labels}
            for x in range(24):
                if len(block) == 14:
                    break
                block.add(x)
            assert len(block) == 14
            blocks.add(tuple(sorted(block)))
    return {"blocks": [list(b) for b in sorted(blocks)]}
