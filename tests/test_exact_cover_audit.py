"""Independent clipping must retain exact fractions for empty intersections."""
from fractions import Fraction as F
import pytest
from scripts.audits.convex_cover_audit import audit_polygons
from scripts.audits.square_cover_audit import area


def test_rational_cover_with_empty_triangle_intersections():
    p=[(F(x,3),F(y,3)) for x,y in [(0,0),(2,0),(2,1),(1,1),(1,2),(0,2)]]
    covers=[[(F(x,3),F(y,3)) for x,y in q] for q in [
        [(0,0),(2,0),(2,1),(0,1)],[(0,1),(1,1),(1,2),(0,2)]]]
    assert type(area([])) is F
    result=audit_polygons(p,covers)
    assert result['target_area']=='1/3' and result['uncovered_area']=='0'
    with pytest.raises(AssertionError):audit_polygons(p,covers[:1])
