"""Canonical unit conversions shared across Wove tooling."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class _LengthUnit:
    """Definition for a length unit tracked by :class:`UnitRegistry`."""

    name: str
    meters_per_unit: float
    aliases: tuple[str, ...]


class UnitRegistry:
    """Registry that converts between supported length units.

    The curriculum and tooling reference imperial and metric measurements.
    Centralizing conversion logic keeps gauge calculators, tension analyzers,
    and motion planners aligned.  The registry recognizes a handful of
    canonical units plus pluralized and abbreviated aliases and converts
    through meters as the base unit.
    """

    def __init__(self) -> None:
        length_units = (
            _LengthUnit("millimeter", 0.001, ("mm", "millimeters")),
            _LengthUnit("centimeter", 0.01, ("cm", "centimeters")),
            _LengthUnit("meter", 1.0, ("m", "meters")),
            _LengthUnit("inch", 0.0254, ("in", "inches")),
            _LengthUnit("yard", 0.9144, ("yd", "yards")),
        )
        aliases: Dict[str, str] = {}
        factors: Dict[str, float] = {}
        for unit in length_units:
            canonical = unit.name
            factors[canonical] = unit.meters_per_unit
            aliases[canonical] = canonical
            for alias in unit.aliases:
                aliases[alias] = canonical
        alias_map: Dict[str, str] = {}
        for key, value in aliases.items():
            alias_map[key.lower()] = value
        self._length_aliases = alias_map
        self._length_factors = factors

    def normalize_length_unit(self, unit: str) -> str:
        """Return the canonical name for ``unit``.

        Args:
            unit: Unit name or alias (case insensitive).

        Raises:
            ValueError: If the unit is not registered.
        """

        key = unit.strip().lower()
        try:
            return self._length_aliases[key]
        except KeyError as error:
            raise ValueError(f"Unknown length unit: {unit!r}") from error

    def _length_factor(self, unit: str) -> float:
        canonical = self.normalize_length_unit(unit)
        return self._length_factors[canonical]

    def conversion_ratio(self, from_unit: str, to_unit: str) -> float:
        """Return the multiplicative ratio between two length units."""

        from_factor = self._length_factor(from_unit)
        to_factor = self._length_factor(to_unit)
        return from_factor / to_factor

    def _validate_value(self, value: float, *, label: str) -> None:
        if not math.isfinite(value):
            raise ValueError(f"{label} must be a finite value")
        if value < 0:
            raise ValueError(f"{label} must be non-negative")

    def convert_length(
        self,
        value: float,
        from_unit: str,
        to_unit: str,
    ) -> float:
        """Convert a length value between supported units."""

        self._validate_value(value, label="value")
        ratio = self.conversion_ratio(from_unit, to_unit)
        return value * ratio

    def convert_per_length(
        self,
        value: float,
        from_unit: str,
        to_unit: str,
    ) -> float:
        """Convert a per-length density into a different unit."""

        self._validate_value(value, label="value")
        ratio = self.conversion_ratio(to_unit, from_unit)
        return value * ratio

    @property
    def length_units(self) -> tuple[str, ...]:
        """Return the canonical length units sorted alphabetically."""

        return tuple(sorted(self._length_factors))


UNIT_REGISTRY = UnitRegistry()

__all__ = ["UnitRegistry", "UNIT_REGISTRY"]
