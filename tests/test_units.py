"""Unit tests for the shared unit registry."""

from __future__ import annotations

import pytest

from wove.units import UNIT_REGISTRY, UnitRegistry


def test_convert_length_aliases() -> None:
    inches_to_cm = UNIT_REGISTRY.convert_length(2.0, "inch", "centimeter")
    cm_to_meters = UNIT_REGISTRY.convert_length(10.0, "CM", "meter")
    meters_to_yard = UNIT_REGISTRY.convert_length(0.9144, "meters", "yard")

    assert inches_to_cm == pytest.approx(5.08)
    assert cm_to_meters == pytest.approx(0.1)
    assert meters_to_yard == pytest.approx(1.0)


def test_convert_per_length() -> None:
    per_inch = UNIT_REGISTRY.convert_per_length(5.0, "inch", "yard")
    per_cm = UNIT_REGISTRY.convert_per_length(2.0, "centimeter", "inch")

    assert per_inch == pytest.approx(180.0)
    assert per_cm == pytest.approx(5.08)


def test_conversion_ratio_symmetry() -> None:
    ratio = UNIT_REGISTRY.conversion_ratio("inch", "meter")
    inverse = UNIT_REGISTRY.conversion_ratio("meter", "inch")
    assert ratio * inverse == pytest.approx(1.0)


def test_unknown_unit_raises() -> None:
    with pytest.raises(ValueError):
        UNIT_REGISTRY.convert_length(1.0, "parsec", "inch")
    with pytest.raises(ValueError):
        UNIT_REGISTRY.convert_per_length(1.0, "inch", "parsec")


def test_custom_registry_normalization() -> None:
    registry = UnitRegistry()
    assert registry.normalize_length_unit("Inches") == "inch"
    assert "centimeter" in registry.length_units
