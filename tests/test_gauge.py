import pytest

from wove import rows_per_cm, rows_per_inch, stitches_per_cm, stitches_per_inch


def test_stitches_per_inch():
    assert stitches_per_inch(20, 4) == 5.0


def test_stitches_per_inch_invalid_inches():
    with pytest.raises(ValueError):
        stitches_per_inch(10, 0)


def test_stitches_per_inch_invalid_stitches():
    with pytest.raises(ValueError):
        stitches_per_inch(0, 4)


def test_rows_per_inch():
    assert rows_per_inch(30, 4) == 7.5


def test_rows_per_inch_invalid_inches():
    with pytest.raises(ValueError):
        rows_per_inch(10, 0)


def test_rows_per_inch_invalid_rows():
    with pytest.raises(ValueError):
        rows_per_inch(0, 4)


def test_stitches_per_cm():
    assert stitches_per_cm(20, 10) == 2.0


def test_stitches_per_cm_invalid_cm():
    with pytest.raises(ValueError):
        stitches_per_cm(10, 0)


def test_stitches_per_cm_invalid_stitches():
    with pytest.raises(ValueError):
        stitches_per_cm(0, 10)


def test_rows_per_cm():
    assert rows_per_cm(30, 10) == 3.0


def test_rows_per_cm_invalid_cm():
    with pytest.raises(ValueError):
        rows_per_cm(10, 0)


def test_rows_per_cm_invalid_rows():
    with pytest.raises(ValueError):
        rows_per_cm(0, 10)
