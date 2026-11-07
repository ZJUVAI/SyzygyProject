"""Keep reported records separate from reproduced public witnesses."""
from scripts.result_table import collect, display, markdown


def test_pending_task_is_excluded_before_record_files_exist(tmp_path, monkeypatch):
    import json
    from scripts import result_table
    directory = tmp_path / 'tasks' / 't999'
    directory.mkdir(parents=True)
    (directory / 'task.json').write_text(json.dumps({
        'task_id': 'T999', 'acceptance_status': 'pending_sol_review',
        'configurations': [{'id': 'T999-C01'}]}))
    from mathbench import registry
    monkeypatch.setattr(registry, 'TASKS', tmp_path / 'tasks')
    monkeypatch.setattr(registry, 'INITIAL_TASKS', ('T999',))
    assert result_table.collect() == []


def test_reported_unavailable_code_is_separate_from_reproduction():
    row = next(row for row in collect() if row['config_id'] == 'T010-C01')
    assert row['best_reproduced'] == 256
    assert str(row['best_reported']) == '258'


def test_unregistered_draft_is_not_read(tmp_path, monkeypatch):
    from scripts import result_table
    directory = tmp_path / 'tasks' / 't999'
    directory.mkdir(parents=True)
    (directory / 'task.json').write_text('incomplete draft metadata')
    from mathbench import registry
    monkeypatch.setattr(registry, 'TASKS', tmp_path / 'tasks')
    assert result_table.collect() == []


def test_four_columns_preserve_missing_results():
    text = markdown([dict(config_id='example', direction='maximize',
                          initial=1, search=None, best_reproduced=2, best_reported=3)])
    assert '| example ↑ | 1 | — | 2 | 3 |' in text


def test_algebraic_source_value_can_be_displayed():
    assert display('6+1/2*sqrt(2)') == '6.70710678118655'


def test_underline_follows_direction_and_marks_ties():
    text = markdown([dict(config_id='example', direction='minimize',
                          initial=7, search=6, best_reproduced=5, best_reported=5)],
                    underline_best=True)
    assert '| example ↓ | 7 | 6 | <u>5</u> | <u>5</u> |' in text


def test_visible_highlight_marks_all_best_values():
    text = markdown([dict(config_id='example', direction='maximize', initial=1,
                          search=3, best_reproduced=3, best_reported=2)],
                    highlight_best=True)
    assert '| example ↑ | 1 | **🏆 3** | **🏆 3** | 2 |' in text


def test_tiny_numerical_differences_do_not_get_a_record_trophy():
    text = markdown([dict(config_id='sphere', direction='maximize', initial='0.79',
                          search='0.911836721599916',
                          best_reproduced='0.9118367215999157',
                          best_reported='0.91183672159953295334')], highlight_best=True)
    assert text.count('**≈ ') == 3
    assert '🏆' not in text
    assert '0.9118367215999157' in text


def test_large_integer_ranking_remains_exact():
    text = markdown([dict(config_id='integer', direction='maximize', initial=1,
                          search=9007199254740993,
                          best_reproduced=9007199254740992,
                          best_reported=9007199254740992)], highlight_best=True)
    assert '**🏆 9007199254740993**' in text
    assert '≈' not in text


def test_small_norms_with_large_relative_gaps_are_distinct():
    text = markdown([dict(config_id='polynomial', direction='minimize', initial=1,
                          search='1e-52', best_reproduced='1e-44',
                          best_reported='1e-55')], highlight_best=True)
    assert '≈' not in text
    assert '**🏆 1e-55**' in text


def test_quadratic_triangle_side_keeps_raw_value_and_displays_same_units():
    assert display('[1,1/3]',quadratic_radicand=3)=='1.57735026918963'
    text=markdown([dict(task_id='T083',config_id='T083-C01',direction='minimize',
        initial='[2,0]',search='[2,0]',best_reproduced='[1,1/3]',best_reported=1.577350269189626)])
    assert '| T083-C01 ↓ | 2 | 2 | 1.577350269189626 | 1.577350269189626 |' in text


def test_spherical_fourth_root_is_displayed_in_ratio_units():
    raw='fourth_root(58188232951867590/10575651537777253)'
    assert display(raw)=='1.53155292496130'
    text=markdown([dict(task_id='T092',config_id='T092-C01',direction='maximize',
        initial=1,search=raw,best_reproduced=raw,best_reported=1.5315529249613016)],highlight_best=True)
    assert 'fourth_root' not in text
    assert '1.531552924961301' in text


def test_eighth_root_is_displayed_as_the_raw_norm_ratio():
    assert display('(1/256)^(1/8)')=='0.5'
    assert display('eighth_root(1/256)')=='0.5'
    assert display('(345/3344)^(1/8)')=='0.752825122156389'
    text=markdown([dict(task_id='T086',config_id='T086-C01',direction='maximize',
        initial='(1/256)^(1/8)',search=None,best_reproduced='(345/3344)^(1/8)',best_reported=None)])
    assert '| T086-C01 ↑ | 0.5 | — | 0.7528251221563891 | — |' in text


def test_exact_square_root_sum_display():
    import pytest
    assert display('sqrt_sum:[1,4,9]') == '6'
    assert display('sqrt_sum:[2,8]') == '4.24264068711929'
    for bad in ('sqrt_sum:[-1]', 'sqrt_sum:[true]', 'sqrt_sum:[]'):
        with pytest.raises(ValueError):
            display(bad)
