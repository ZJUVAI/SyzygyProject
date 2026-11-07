"""A rounded display score cannot replace an exact reproduced objective."""
from scripts.audit_sota import same_exact_value


def test_display_rounding_cannot_pass_exact_metadata_check():
    assert not same_exact_value(
        '0.8892261730897966',
        '108065664771600646574507764702/121527759800529249872686490775')
    assert not same_exact_value('1.0', '10000000000000001/10000000000000000')


def test_exact_equivalent_forms_are_supported():
    assert same_exact_value('0.125', '1/8')
    assert same_exact_value('7/2+3/2*sqrt2', '(7+3*sqrt(2))/2')


def test_radical_sum_archive_preserves_all_exact_terms():
    assert same_exact_value('sqrt_sum:[2,8,7]', 'sqrt_sum:[7,2,8]')
    assert not same_exact_value('sqrt_sum:[2,8,7]', 'sqrt_sum:[7,2,9]')
    assert not same_exact_value('sqrt_sum:[true]', 'sqrt_sum:[1]')
    assert same_exact_value('sqrt_sum:[1,4]', '3')
    assert same_exact_value('sqrt_sum:[8]', '2*sqrt(2)')
