import time
from tasks.t008.evolution import QUADS, UNIVERSE, _cover_mask, _milp_repair
from tasks.t008.init_program import run_code


def test_local_milp_restores_deleted_block():
    blocks = run_code()['blocks']
    index = {q:i for i,q in enumerate(QUADS)}
    masks = [_cover_mask(b, index) for b in blocks]
    candidate = _milp_repair(list(range(1, len(blocks))), masks, 1, time.monotonic()+5)
    assert candidate is not None
    mask = 0
    for i in candidate:
        mask |= masks[i]
    assert mask == UNIVERSE
