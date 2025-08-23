import pytest

from wove import (
    cm_for_stitches,
    cm_to_inches,
    inches_for_stitches,
    inches_to_cm,
    meters_to_yards,
    per_cm_to_per_inch,
    per_inch_to_per_cm,
    rows_for_cm,
    rows_for_inches,
    rows_per_cm,
    rows_per_inch,
    stitches_for_cm,
    stitches_for_inches,
    stitches_per_cm,
    stitches_per_inch,
    yards_to_meters,
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


def test_stitches_for_inches():
    assert stitches_for_inches(5.0, 4) == 20


def test_stitches_for_inches_invalid_gauge():
    with pytest.raises(ValueError):
        stitches_for_inches(0, 4)


def test_stitches_for_inches_invalid_inches():
    with pytest.raises(ValueError):
        stitches_for_inches(5.0, 0)


def test_stitches_for_cm():
    assert stitches_for_cm(2.0, 10) == 20


def test_stitches_for_cm_invalid_gauge():
    with pytest.raises(ValueError):
        stitches_for_cm(0, 10)


def test_stitches_for_cm_invalid_cm():
    with pytest.raises(ValueError):
        stitches_for_cm(2.0, 0)


def test_inches_for_stitches():
    assert inches_for_stitches(20, 5.0) == 4.0


def test_inches_for_stitches_invalid_stitches():
    with pytest.raises(ValueError):
        inches_for_stitches(0, 5.0)


def test_inches_for_stitches_invalid_gauge():
    with pytest.raises(ValueError):
        inches_for_stitches(20, 0)


def test_cm_for_stitches():
    assert cm_for_stitches(20, 2.0) == 10.0


def test_cm_for_stitches_invalid_stitches():
    with pytest.raises(ValueError):
        cm_for_stitches(0, 2.0)


def test_cm_for_stitches_invalid_gauge():
    with pytest.raises(ValueError):
        cm_for_stitches(20, 0)


def test_rows_for_inches():
    assert rows_for_inches(7.5, 4) == 30


def test_rows_for_inches_invalid_gauge():
    with pytest.raises(ValueError):
        rows_for_inches(0, 4)


def test_rows_for_inches_invalid_inches():
    with pytest.raises(ValueError):
        rows_for_inches(7.5, 0)


def test_rows_for_cm():
    assert rows_for_cm(3.0, 10) == 30


def test_rows_for_cm_invalid_gauge():
    with pytest.raises(ValueError):
        rows_for_cm(0, 10)


def test_rows_for_cm_invalid_cm():
    with pytest.raises(ValueError):
        rows_for_cm(3.0, 0)


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


def test_yards_to_meters():
    assert yards_to_meters(1.0) == pytest.approx(0.9144)


def test_yards_to_meters_invalid():
    with pytest.raises(ValueError):
        yards_to_meters(-1)


def test_meters_to_yards():
    assert meters_to_yards(0.9144) == pytest.approx(1.0)


def test_meters_to_yards_invalid():
    with pytest.raises(ValueError):
        meters_to_yards(-1)


def test_stitches_for_inches_half_up():
    assert stitches_for_inches(2.5, 1) == 3


def test_rows_for_cm_half_up():
    assert rows_for_cm(2.5, 1) == 3
