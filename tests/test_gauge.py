import pytest

from wove import rows_per_cm, rows_per_inch, stitches_per_cm, stitches_per_inch


def test_stitches_per_inch():
    assert stitches_per_inch(20, 4) == 5.0


@pytest.mark.parametrize("bad_inches", [0, -4])
def test_stitches_per_inch_invalid_inches(bad_inches: float) -> None:
    with pytest.raises(ValueError):
        stitches_per_inch(10, bad_inches)


@pytest.mark.parametrize("bad_stitches", [0, -10])
def test_stitches_per_inch_invalid_stitches(bad_stitches: int) -> None:
    with pytest.raises(ValueError):
        stitches_per_inch(bad_stitches, 4)


def test_rows_per_inch():
    assert rows_per_inch(30, 4) == 7.5


@pytest.mark.parametrize("bad_inches", [0, -4])
def test_rows_per_inch_invalid_inches(bad_inches: float) -> None:
    with pytest.raises(ValueError):
        rows_per_inch(10, bad_inches)


@pytest.mark.parametrize("bad_rows", [0, -10])
def test_rows_per_inch_invalid_rows(bad_rows: int) -> None:
    with pytest.raises(ValueError):
        rows_per_inch(bad_rows, 4)


def test_stitches_per_cm():
    assert stitches_per_cm(20, 10) == 2.0


@pytest.mark.parametrize("bad_cm", [0, -10])
def test_stitches_per_cm_invalid_cm(bad_cm: float) -> None:
    with pytest.raises(ValueError):
        stitches_per_cm(10, bad_cm)


@pytest.mark.parametrize("bad_stitches", [0, -10])
def test_stitches_per_cm_invalid_stitches(bad_stitches: int) -> None:
    with pytest.raises(ValueError):
        stitches_per_cm(bad_stitches, 10)


def test_rows_per_cm():
    assert rows_per_cm(30, 10) == 3.0


@pytest.mark.parametrize("bad_cm", [0, -10])
def test_rows_per_cm_invalid_cm(bad_cm: float) -> None:
    with pytest.raises(ValueError):
        rows_per_cm(10, bad_cm)


@pytest.mark.parametrize("bad_rows", [0, -10])
def test_rows_per_cm_invalid_rows(bad_rows: int) -> None:
    with pytest.raises(ValueError):
        rows_per_cm(bad_rows, 10)
