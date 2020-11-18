import pytest

from progress_keeper import Progress


@pytest.fixture
def prog_no_var():
    return Progress('tests/tmp/progress.cfg')


@pytest.fixture
def prog_with_vars():
    return Progress('tests/tmp/progress_with_vars.cfg', vars=['tracker_1', 'tracker_2', 'tracker_3'])


def test_initialize_no_vars_def(prog_no_var):
    assert prog_no_var.values['last_index_processed'] == 0


def test_initialize_with_vars(prog_with_vars):
    assert prog_with_vars.values['tracker_1'] == 0
    assert prog_with_vars.values['tracker_2'] == 0
    assert prog_with_vars.values['tracker_3'] == 0


def test_increment_no_vars_def_1(prog_no_var):
    prog_no_var.increment()
    assert prog_no_var.values['last_index_processed'] == 1


def test_increment_no_vars_def_2(prog_no_var):
    prog_no_var.increment()
    prog_no_var.increment()
    prog_no_var.increment()
    assert prog_no_var.values['last_index_processed'] == 3


def test_increment_no_vars_def_does_not_exist(prog_no_var):
    prog_no_var.increment('do_not_exist')
    assert prog_no_var.values['last_index_processed'] == 0


def test_increment_with_vars_1(prog_with_vars):
    prog_with_vars.increment('tracker_1')
    prog_with_vars.increment('tracker_3')
    assert prog_with_vars.values['tracker_1'] == 1
    assert prog_with_vars.values['tracker_3'] == 1


def test_increment_with_vars_2(prog_with_vars):
    prog_with_vars.increment('tracker_1')
    prog_with_vars.increment('tracker_2')
    prog_with_vars.increment('tracker_2')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.increment()
    assert prog_with_vars.values['tracker_1'] == 1
    assert prog_with_vars.values['tracker_2'] == 2
    assert prog_with_vars.values['tracker_3'] == 3


def test_increment_with_vars_does_not_exist(prog_with_vars):
    prog_with_vars.increment('do_not_exist')
    assert prog_with_vars.values['tracker_1'] == 0
    assert prog_with_vars.values['tracker_2'] == 0
    assert prog_with_vars.values['tracker_3'] == 0


def test_reset_no_vars_def(prog_no_var):
    prog_no_var.increment()
    prog_no_var.increment()
    prog_no_var.reset()
    assert prog_no_var.values['last_index_processed'] == 0


def test_reset_no_vars_def(prog_no_var):
    prog_no_var.increment()
    prog_no_var.increment()
    prog_no_var.reset('does_not_exist')
    assert prog_no_var.values['last_index_processed'] == 2


def test_reset_with_vars_1(prog_with_vars):
    prog_with_vars.increment('tracker_1')
    prog_with_vars.increment('tracker_2')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.reset('tracker_1')
    prog_with_vars.reset('tracker_3')
    assert prog_with_vars.values['tracker_1'] == 0
    assert prog_with_vars.values['tracker_2'] == 1
    assert prog_with_vars.values['tracker_3'] == 0


def test_reset_with_vars_not_exist(prog_with_vars):
    prog_with_vars.increment('tracker_1')
    prog_with_vars.increment('tracker_2')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.increment('tracker_3')
    prog_with_vars.reset('tracker_1')
    prog_with_vars.reset('tracker_3')
    prog_with_vars.reset('does_not_exist')
    assert prog_with_vars.values['tracker_1'] == 0
    assert prog_with_vars.values['tracker_2'] == 1
    assert prog_with_vars.values['tracker_3'] == 0


def test_delete(prog_no_var):
    prog_no_var.delete()
