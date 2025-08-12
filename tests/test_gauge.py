import pytest

from wove import (
    cm_to_inches,
    inches_to_cm,
    per_cm_to_per_inch,
    per_inch_to_per_cm,
    rows_per_cm,
    rows_per_inch,
    stitches_per_cm,
    stitches_per_inch,
)


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


def test_per_inch_to_per_cm():
    assert per_inch_to_per_cm(5.08) == pytest.approx(2.0)


def test_per_inch_to_per_cm_invalid():
    with pytest.raises(ValueError):
        per_inch_to_per_cm(0)


def test_per_cm_to_per_inch():
    assert per_cm_to_per_inch(2.0) == pytest.approx(5.08)


def test_per_cm_to_per_inch_invalid():
    with pytest.raises(ValueError):
        per_cm_to_per_inch(0)


def test_inches_to_cm():
    assert inches_to_cm(1.0) == pytest.approx(2.54)


def test_inches_to_cm_invalid():
    with pytest.raises(ValueError):
        inches_to_cm(-1)


def test_cm_to_inches():
    assert cm_to_inches(2.54) == pytest.approx(1.0)


def test_cm_to_inches_invalid():
    with pytest.raises(ValueError):
        cm_to_inches(-1)
