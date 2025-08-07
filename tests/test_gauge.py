import pytest

from wove import rows_per_inch, stitches_per_inch


def test_stitches_per_inch():
    assert stitches_per_inch(20, 4) == 5.0


def test_stitches_per_inch_invalid():
    with pytest.raises(ValueError):
        stitches_per_inch(10, 0)


def test_rows_per_inch():
    assert rows_per_inch(30, 4) == 7.5


def test_rows_per_inch_invalid():
    with pytest.raises(ValueError):
        rows_per_inch(10, 0)
