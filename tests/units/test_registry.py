from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from wove.units import UNIT_REGISTRY

_UNIT_STRATEGY = st.sampled_from(
    (
        "millimeter",
        "mm",
        "Millimeters",
        "centimeter",
        "CM",
        "centimeters",
        "meter",
        "Meters",
        "inch",
        "IN",
        "inches",
        "yard",
        "YARD",
        "yards",
    )
)
_POSITIVE_LENGTHS = st.floats(
    min_value=0.0,
    max_value=1_000_000.0,
    allow_nan=False,
    allow_infinity=False,
)
_NEGATIVE_LENGTHS = st.floats(
    max_value=-1e-9,
    allow_nan=False,
    allow_infinity=False,
)


@given(
    value=_POSITIVE_LENGTHS,
    from_unit=_UNIT_STRATEGY,
    to_unit=_UNIT_STRATEGY,
)
def test_convert_length_round_trip(
    value: float,
    from_unit: str,
    to_unit: str,
) -> None:
    converted = UNIT_REGISTRY.convert_length(value, from_unit, to_unit)
    returned = UNIT_REGISTRY.convert_length(converted, to_unit, from_unit)
    assert returned == pytest.approx(
        value,
        rel=1e-9,
        abs=1e-9,
    )


@given(
    value=_POSITIVE_LENGTHS,
    from_unit=_UNIT_STRATEGY,
    to_unit=_UNIT_STRATEGY,
)
def test_convert_per_length_round_trip(
    value: float,
    from_unit: str,
    to_unit: str,
) -> None:
    converted = UNIT_REGISTRY.convert_per_length(value, from_unit, to_unit)
    returned = UNIT_REGISTRY.convert_per_length(converted, to_unit, from_unit)
    assert returned == pytest.approx(
        value,
        rel=1e-9,
        abs=1e-9,
    )


@given(
    value=_POSITIVE_LENGTHS,
    from_unit=_UNIT_STRATEGY,
    to_unit=_UNIT_STRATEGY,
)
def test_convert_per_length_matches_ratio(
    value: float,
    from_unit: str,
    to_unit: str,
) -> None:
    converted = UNIT_REGISTRY.convert_per_length(value, from_unit, to_unit)
    ratio = UNIT_REGISTRY.conversion_ratio(to_unit, from_unit)
    assert converted == pytest.approx(
        value * ratio,
        rel=1e-9,
        abs=1e-9,
    )


@given(
    value=_NEGATIVE_LENGTHS,
    from_unit=_UNIT_STRATEGY,
    to_unit=_UNIT_STRATEGY,
)
def test_convert_length_rejects_negative(
    value: float,
    from_unit: str,
    to_unit: str,
) -> None:
    with pytest.raises(ValueError):
        UNIT_REGISTRY.convert_length(value, from_unit, to_unit)


@given(
    value=_NEGATIVE_LENGTHS,
    from_unit=_UNIT_STRATEGY,
    to_unit=_UNIT_STRATEGY,
)
def test_convert_per_length_rejects_negative(
    value: float,
    from_unit: str,
    to_unit: str,
) -> None:
    with pytest.raises(ValueError):
        UNIT_REGISTRY.convert_per_length(value, from_unit, to_unit)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_convert_length_rejects_non_finite(value: float) -> None:
    with pytest.raises(ValueError):
        UNIT_REGISTRY.convert_length(value, "inch", "centimeter")


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_convert_per_length_rejects_non_finite(value: float) -> None:
    with pytest.raises(ValueError):
        UNIT_REGISTRY.convert_per_length(value, "inch", "centimeter")
