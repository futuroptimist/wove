import pytest

from wove import stitches_per_inch


def test_stitches_per_inch():
    assert stitches_per_inch(20, 4) == 5.0


def test_stitches_per_inch_invalid():
    with pytest.raises(ValueError):
        stitches_per_inch(10, 0)
