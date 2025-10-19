from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction

import hypothesis.strategies as st
import pytest
from hypothesis import given

from wove.units import UNIT_REGISTRY

UNIT_CHOICES = tuple(UNIT_REGISTRY.length_units)


@st.composite
def unit_pairs(draw) -> tuple[str, str]:
    from_unit = draw(st.sampled_from(UNIT_CHOICES))
    to_unit = draw(st.sampled_from(UNIT_CHOICES))
    return from_unit, to_unit


@given(
    value=st.floats(
        min_value=1e-6,
        max_value=1e6,
        allow_nan=False,
        allow_infinity=False,
    ),
    units=unit_pairs(),
)
def test_round_trip_length_float(value: float, units: tuple[str, str]) -> None:
    from_unit, to_unit = units
    forward = UNIT_REGISTRY.convert_length(value, from_unit, to_unit)
    backward = UNIT_REGISTRY.convert_length(forward, to_unit, from_unit)
    assert backward == pytest.approx(value, rel=1e-9, abs=1e-9)


@given(
    value=st.decimals(
        min_value=Decimal("0.0001"),
        max_value=Decimal("100000"),
        allow_nan=False,
        allow_infinity=False,
        places=4,
    ),
    units=unit_pairs(),
)
def test_round_trip_length_decimal(
    value: Decimal,
    units: tuple[str, str],
) -> None:
    from_unit, to_unit = units
    forward = UNIT_REGISTRY.convert_length(value, from_unit, to_unit)
    back_input = Decimal(str(forward))
    backward = UNIT_REGISTRY.convert_length(
        back_input,
        to_unit,
        from_unit,
    )
    assert backward == pytest.approx(float(value), rel=1e-9, abs=1e-9)


@given(
    numerator=st.integers(min_value=1, max_value=5000),
    denominator=st.integers(min_value=1, max_value=5000),
    units=unit_pairs(),
)
def test_fraction_matches_float(
    numerator: int, denominator: int, units: tuple[str, str]
) -> None:
    value_fraction = Fraction(numerator, denominator)
    from_unit, to_unit = units
    fraction_result = UNIT_REGISTRY.convert_length(
        value_fraction,
        from_unit,
        to_unit,
    )
    float_result = UNIT_REGISTRY.convert_length(
        float(value_fraction),
        from_unit,
        to_unit,
    )
    assert fraction_result == pytest.approx(
        float_result,
        rel=1e-12,
        abs=1e-12,
    )


def test_convert_length_rejects_non_numeric_input() -> None:
    with pytest.raises(TypeError):
        UNIT_REGISTRY.convert_length("twelve", "inch", "meter")


@pytest.mark.parametrize(
    "bad_value",
    [
        math.inf,
        float("-inf"),
        float("nan"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
        Decimal("NaN"),
    ],
)
def test_convert_length_rejects_non_finite_values(bad_value: float) -> None:
    with pytest.raises(ValueError):
        UNIT_REGISTRY.convert_length(bad_value, "meter", "inch")


def test_convert_length_rejects_negative_value() -> None:
    with pytest.raises(ValueError):
        UNIT_REGISTRY.convert_length(-1.0, "meter", "inch")


@pytest.mark.parametrize(
    "value, from_unit, to_unit, expected",
    [
        (
            10.0,
            "inch",
            "centimeter",
            pytest.approx(3.937007874015748),
        ),
        (
            Decimal("2.5"),
            "meter",
            "yard",
            pytest.approx(
                UNIT_REGISTRY.conversion_ratio("yard", "meter") * 2.5,
            ),
        ),
        (
            Fraction(3, 2),
            "centimeter",
            "inch",
            pytest.approx(
                UNIT_REGISTRY.conversion_ratio("inch", "centimeter")
                * 1.5,
                rel=1e-12,
                abs=1e-12,
            ),
        ),
    ],
)
def test_convert_per_length_handles_supported_numbers(
    value: float | Decimal | Fraction,
    from_unit: str,
    to_unit: str,
    expected,
) -> None:
    result = UNIT_REGISTRY.convert_per_length(value, from_unit, to_unit)
    assert result == expected


@pytest.mark.parametrize(
    "bad_value",
    [
        math.inf,
        float("-inf"),
        float("nan"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
        Decimal("NaN"),
    ],
)
def test_convert_per_length_rejects_non_finite_values(
    bad_value: float,
) -> None:
    with pytest.raises(ValueError):
        UNIT_REGISTRY.convert_per_length(bad_value, "meter", "inch")


def test_convert_per_length_rejects_negative_value() -> None:
    with pytest.raises(ValueError):
        UNIT_REGISTRY.convert_per_length(-0.5, "meter", "inch")
