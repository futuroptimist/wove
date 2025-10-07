# isort: skip_file

# isort: skip_file

import pytest

from wove import (
    cm_for_rows,
    cm_for_stitches,
    cm_to_inches,
    cm_to_meters,
    meters_for_rows,
    meters_for_stitches,
    height_difference_for_rows,
    stitch_adjustment_for_width,
    row_adjustment_for_height,
    rows_per_yard,
    stitches_per_yard,
    rows_per_meter,
    stitches_per_meter,
    inches_for_rows,
    inches_for_stitches,
    inches_to_cm,
    inches_to_meters,
    inches_to_yards,
    cm_to_yards,
    yards_to_cm,
    yards_for_rows,
    yards_for_stitches,
    width_difference_for_stitches,
    meters_to_yards,
    meters_to_cm,
    meters_to_inches,
    per_cm_to_per_inch,
    per_cm_to_per_meter,
    per_cm_to_per_yard,
    per_inch_to_per_cm,
    per_inch_to_per_meter,
    per_inch_to_per_yard,
    per_meter_to_per_cm,
    per_meter_to_per_inch,
    per_meter_to_per_yard,
    rows_for_cm,
    rows_for_inches,
    rows_for_meters,
    rows_for_yards,
    rows_per_cm,
    rows_per_inch,
    stitches_for_cm,
    stitches_for_inches,
    stitches_for_meters,
    stitches_for_yards,
    stitches_per_cm,
    stitches_per_inch,
    per_yard_to_per_cm,
    per_yard_to_per_inch,
    per_yard_to_per_meter,
    yards_to_inches,
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


def test_stitches_per_yard():
    assert stitches_per_yard(180, 2.0) == 90.0


def test_stitches_per_yard_invalid_yards():
    with pytest.raises(ValueError):
        stitches_per_yard(180, 0)


def test_stitches_per_yard_invalid_stitches():
    with pytest.raises(ValueError):
        stitches_per_yard(0, 2.0)


def test_rows_per_yard():
    assert rows_per_yard(240, 3.0) == 80.0


def test_rows_per_yard_invalid_yards():
    with pytest.raises(ValueError):
        rows_per_yard(240, 0)


def test_rows_per_yard_invalid_rows():
    with pytest.raises(ValueError):
        rows_per_yard(0, 3.0)


def test_stitches_per_meter():
    assert stitches_per_meter(300, 3.0) == 100.0


def test_stitches_per_meter_invalid_meters():
    with pytest.raises(ValueError):
        stitches_per_meter(300, 0)


def test_stitches_per_meter_invalid_stitches():
    with pytest.raises(ValueError):
        stitches_per_meter(0, 3.0)


def test_rows_per_meter():
    assert rows_per_meter(250, 2.5) == 100.0


def test_rows_per_meter_invalid_meters():
    with pytest.raises(ValueError):
        rows_per_meter(250, 0)


def test_rows_per_meter_invalid_rows():
    with pytest.raises(ValueError):
        rows_per_meter(0, 2.5)


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


@pytest.mark.parametrize(
    ("func", "value", "expected"),
    [
        (per_inch_to_per_yard, 5.0, 180.0),
        (per_yard_to_per_inch, 180.0, 5.0),
        (per_inch_to_per_meter, 5.0, 196.8503937007874),
        (per_meter_to_per_inch, 196.8503937007874, 5.0),
        (per_cm_to_per_meter, 2.0, 200.0),
        (per_meter_to_per_cm, 200.0, 2.0),
        (per_cm_to_per_yard, 2.0, 182.88),
        (per_yard_to_per_cm, 182.88, 2.0),
        (per_yard_to_per_meter, 180.0, 196.8503937007874),
        (per_meter_to_per_yard, 196.8503937007874, 180.0),
    ],
)
def test_additional_per_unit_conversions(func, value, expected):
    assert func(value) == pytest.approx(expected)


@pytest.mark.parametrize(
    "func",
    [
        per_inch_to_per_yard,
        per_yard_to_per_inch,
        per_inch_to_per_meter,
        per_meter_to_per_inch,
        per_cm_to_per_meter,
        per_meter_to_per_cm,
        per_cm_to_per_yard,
        per_yard_to_per_cm,
        per_yard_to_per_meter,
        per_meter_to_per_yard,
    ],
)
def test_additional_per_unit_conversions_invalid(func):
    with pytest.raises(ValueError):
        func(0)


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


def test_stitches_for_yards():
    assert stitches_for_yards(180.0, 0.25) == 45


def test_stitches_for_yards_invalid_gauge():
    with pytest.raises(ValueError):
        stitches_for_yards(0, 0.25)


def test_stitches_for_yards_invalid_yards():
    with pytest.raises(ValueError):
        stitches_for_yards(180.0, 0)


def test_stitches_for_meters():
    assert stitches_for_meters(120.0, 0.3) == 36


def test_stitches_for_meters_invalid_gauge():
    with pytest.raises(ValueError):
        stitches_for_meters(0, 0.3)


def test_stitches_for_meters_invalid_meters():
    with pytest.raises(ValueError):
        stitches_for_meters(120.0, 0)


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


def test_yards_for_stitches():
    assert yards_for_stitches(90, 360.0) == pytest.approx(0.25)


def test_yards_for_stitches_invalid_stitches():
    with pytest.raises(ValueError):
        yards_for_stitches(0, 360.0)


def test_yards_for_stitches_invalid_gauge():
    with pytest.raises(ValueError):
        yards_for_stitches(90, 0)


def test_meters_for_stitches():
    assert meters_for_stitches(200, 200.0) == pytest.approx(1.0)


def test_meters_for_stitches_invalid_stitches():
    with pytest.raises(ValueError):
        meters_for_stitches(0, 200.0)


def test_meters_for_stitches_invalid_gauge():
    with pytest.raises(ValueError):
        meters_for_stitches(200, 0)


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


def test_rows_for_yards():
    assert rows_for_yards(270.0, 0.1) == 27


def test_rows_for_yards_invalid_gauge():
    with pytest.raises(ValueError):
        rows_for_yards(0, 0.1)


def test_rows_for_yards_invalid_yards():
    with pytest.raises(ValueError):
        rows_for_yards(270.0, 0)


def test_rows_for_meters():
    assert rows_for_meters(100.0, 0.25) == 25


def test_rows_for_meters_invalid_gauge():
    with pytest.raises(ValueError):
        rows_for_meters(0, 0.25)


def test_rows_for_meters_invalid_meters():
    with pytest.raises(ValueError):
        rows_for_meters(100.0, 0)


def test_inches_for_rows():
    assert inches_for_rows(30, 7.5) == 4.0


def test_inches_for_rows_invalid_rows():
    with pytest.raises(ValueError):
        inches_for_rows(0, 7.5)


def test_inches_for_rows_invalid_gauge():
    with pytest.raises(ValueError):
        inches_for_rows(30, 0)


def test_cm_for_rows():
    assert cm_for_rows(30, 3.0) == 10.0


def test_cm_for_rows_invalid_rows():
    with pytest.raises(ValueError):
        cm_for_rows(0, 3.0)


def test_cm_for_rows_invalid_gauge():
    with pytest.raises(ValueError):
        cm_for_rows(30, 0)


def test_yards_for_rows():
    assert yards_for_rows(36, 120.0) == pytest.approx(0.3)


def test_yards_for_rows_invalid_rows():
    with pytest.raises(ValueError):
        yards_for_rows(0, 120.0)


def test_yards_for_rows_invalid_gauge():
    with pytest.raises(ValueError):
        yards_for_rows(36, 0)


def test_meters_for_rows():
    assert meters_for_rows(400, 400.0) == pytest.approx(1.0)


def test_meters_for_rows_invalid_rows():
    with pytest.raises(ValueError):
        meters_for_rows(0, 400.0)


def test_meters_for_rows_invalid_gauge():
    with pytest.raises(ValueError):
        meters_for_rows(400, 0)


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


def test_meters_to_cm():
    assert meters_to_cm(1.5) == pytest.approx(150.0)


def test_meters_to_cm_invalid():
    with pytest.raises(ValueError):
        meters_to_cm(-1)


def test_cm_to_meters():
    assert cm_to_meters(123) == pytest.approx(1.23)


def test_cm_to_meters_invalid():
    with pytest.raises(ValueError):
        cm_to_meters(-1)


def test_meters_to_inches():
    assert meters_to_inches(1.0) == pytest.approx(39.37007874)


def test_meters_to_inches_invalid():
    with pytest.raises(ValueError):
        meters_to_inches(-1)


def test_inches_to_meters():
    assert inches_to_meters(39.37007874) == pytest.approx(1.0)


def test_inches_to_meters_invalid():
    with pytest.raises(ValueError):
        inches_to_meters(-1)


def test_yards_to_inches():
    assert yards_to_inches(1.0) == pytest.approx(36.0)


def test_yards_to_inches_invalid():
    with pytest.raises(ValueError):
        yards_to_inches(-1)


def test_inches_to_yards():
    assert inches_to_yards(36.0) == pytest.approx(1.0)


def test_inches_to_yards_invalid():
    with pytest.raises(ValueError):
        inches_to_yards(-1)


def test_yards_to_cm():
    assert yards_to_cm(1.0) == pytest.approx(91.44)


def test_yards_to_cm_invalid():
    with pytest.raises(ValueError):
        yards_to_cm(-1)


def test_cm_to_yards():
    assert cm_to_yards(91.44) == pytest.approx(1.0)


def test_cm_to_yards_invalid():
    with pytest.raises(ValueError):
        cm_to_yards(-1)


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


def test_stitches_for_yards_half_up():
    assert stitches_for_yards(2.0, 0.25) == 1


def test_rows_for_meters_half_up():
    assert rows_for_meters(2.0, 0.25) == 1


def test_width_difference_for_stitches():
    diff = width_difference_for_stitches(180, 20, 22)
    assert diff == pytest.approx(-0.8181818182)


def test_width_difference_for_stitches_invalid_inputs():
    with pytest.raises(ValueError):
        width_difference_for_stitches(0, 20, 22)
    with pytest.raises(ValueError):
        width_difference_for_stitches(180, 0, 22)
    with pytest.raises(ValueError):
        width_difference_for_stitches(180, 20, 0)


def test_height_difference_for_rows():
    diff = height_difference_for_rows(220, 30, 28)
    assert diff == pytest.approx(0.5238095238)


def test_height_difference_for_rows_invalid_inputs():
    with pytest.raises(ValueError):
        height_difference_for_rows(0, 30, 28)
    with pytest.raises(ValueError):
        height_difference_for_rows(220, 0, 28)
    with pytest.raises(ValueError):
        height_difference_for_rows(220, 30, 0)


def test_stitch_adjustment_for_width_adds_stitches():
    adjustment = stitch_adjustment_for_width(90, 4.5, 5.25)
    assert adjustment == 15  # requires 105 stitches to maintain width


def test_stitch_adjustment_for_width_removes_stitches():
    adjustment = stitch_adjustment_for_width(100, 5.0, 4.5)
    assert adjustment == -10


def test_stitch_adjustment_for_width_invalid_inputs():
    with pytest.raises(ValueError):
        stitch_adjustment_for_width(0, 5.0, 4.5)
    with pytest.raises(ValueError):
        stitch_adjustment_for_width(100, 0, 4.5)
    with pytest.raises(ValueError):
        stitch_adjustment_for_width(100, 5.0, 0)


def test_stitch_adjustment_for_width_half_up():
    adjustment = stitch_adjustment_for_width(90, 4.5, 5.025)
    assert adjustment == 11  # adjusted stitches round 100.5 -> 101


def test_row_adjustment_for_height_adds_rows():
    adjustment = row_adjustment_for_height(120, 6.0, 6.5)
    assert adjustment == 10  # requires 130 rows to maintain height


def test_row_adjustment_for_height_removes_rows():
    adjustment = row_adjustment_for_height(150, 7.5, 6.0)
    assert adjustment == -30


def test_row_adjustment_for_height_invalid_inputs():
    with pytest.raises(ValueError):
        row_adjustment_for_height(0, 6.0, 6.5)
    with pytest.raises(ValueError):
        row_adjustment_for_height(120, 0, 6.5)
    with pytest.raises(ValueError):
        row_adjustment_for_height(120, 6.0, 0)


def test_row_adjustment_for_height_half_up():
    adjustment = row_adjustment_for_height(120, 6.0, 6.05)
    assert adjustment == 1  # adjusted rows round 121.0 -> 121
