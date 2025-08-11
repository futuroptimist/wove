import pytest

from wove import cm_to_inches, inches_to_cm


def test_inches_to_cm():
    assert inches_to_cm(2) == pytest.approx(5.08)


def test_inches_to_cm_invalid():
    with pytest.raises(ValueError):
        inches_to_cm(0)


def test_cm_to_inches():
    assert cm_to_inches(10) == pytest.approx(3.93700787, rel=1e-6)


def test_cm_to_inches_invalid():
    with pytest.raises(ValueError):
        cm_to_inches(0)
