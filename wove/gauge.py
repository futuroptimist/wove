from __future__ import annotations

import math

CM_PER_INCH = 2.54
CM_PER_METER = 100.0
M_PER_YARD = 0.9144
INCHES_PER_YARD = 36.0
INCHES_PER_METER = CM_PER_METER / CM_PER_INCH


def _round_half_up(value: float) -> int:
    """Round a positive float to the nearest int with halves rounding up."""
    return int(math.floor(value + 0.5))


def inches_to_cm(inches: float) -> float:
    """Convert inches to centimeters.

    Args:
        inches: Length in inches. Must be \u2265 0.

    Returns:
        Equivalent length in centimeters.

    Raises:
        ValueError: If ``inches`` is negative.
    """

    if inches < 0:
        raise ValueError("inches must be non-negative")
    return inches * CM_PER_INCH


def cm_to_inches(cm: float) -> float:
    """Convert centimeters to inches.

    Args:
        cm: Length in centimeters. Must be \u2265 0.

    Returns:
        Equivalent length in inches.

    Raises:
        ValueError: If ``cm`` is negative.
    """

    if cm < 0:
        raise ValueError("cm must be non-negative")
    return cm / CM_PER_INCH


def yards_to_inches(yards: float) -> float:
    """Convert yards to inches.

    Args:
        yards: Length in yards. Must be \u2265 0.

    Returns:
        Equivalent length in inches.

    Raises:
        ValueError: If ``yards`` is negative.
    """

    if yards < 0:
        raise ValueError("yards must be non-negative")
    return yards * INCHES_PER_YARD


def inches_to_yards(inches: float) -> float:
    """Convert inches to yards.

    Args:
        inches: Length in inches. Must be \u2265 0.

    Returns:
        Equivalent length in yards.

    Raises:
        ValueError: If ``inches`` is negative.
    """

    if inches < 0:
        raise ValueError("inches must be non-negative")
    return inches / INCHES_PER_YARD


def yards_to_cm(yards: float) -> float:
    """Convert yards to centimeters.

    Args:
        yards: Length in yards. Must be \u2265 0.

    Returns:
        Equivalent length in centimeters.

    Raises:
        ValueError: If ``yards`` is negative.
    """

    if yards < 0:
        raise ValueError("yards must be non-negative")
    return yards * INCHES_PER_YARD * CM_PER_INCH


def cm_to_yards(cm: float) -> float:
    """Convert centimeters to yards.

    Args:
        cm: Length in centimeters. Must be \u2265 0.

    Returns:
        Equivalent length in yards.

    Raises:
        ValueError: If ``cm`` is negative.
    """

    if cm < 0:
        raise ValueError("cm must be non-negative")
    return cm / (INCHES_PER_YARD * CM_PER_INCH)


def yards_to_meters(yards: float) -> float:
    """Convert yards to meters.

    Args:
        yards: Length in yards. Must be \u2265 0.

    Returns:
        Equivalent length in meters.

    Raises:
        ValueError: If ``yards`` is negative.
    """

    if yards < 0:
        raise ValueError("yards must be non-negative")
    return yards * M_PER_YARD


def meters_to_yards(meters: float) -> float:
    """Convert meters to yards.

    Args:
        meters: Length in meters. Must be \u2265 0.

    Returns:
        Equivalent length in yards.

    Raises:
        ValueError: If ``meters`` is negative.
    """

    if meters < 0:
        raise ValueError("meters must be non-negative")
    return meters / M_PER_YARD


def meters_to_cm(meters: float) -> float:
    """Convert meters to centimeters.

    Args:
        meters: Length in meters. Must be \u2265 0.

    Returns:
        Equivalent length in centimeters.

    Raises:
        ValueError: If ``meters`` is negative.
    """

    if meters < 0:
        raise ValueError("meters must be non-negative")
    return meters * CM_PER_METER


def cm_to_meters(cm: float) -> float:
    """Convert centimeters to meters.

    Args:
        cm: Length in centimeters. Must be \u2265 0.

    Returns:
        Equivalent length in meters.

    Raises:
        ValueError: If ``cm`` is negative.
    """

    if cm < 0:
        raise ValueError("cm must be non-negative")
    return cm / CM_PER_METER


def meters_to_inches(meters: float) -> float:
    """Convert meters to inches.

    Args:
        meters: Length in meters. Must be \u2265 0.

    Returns:
        Equivalent length in inches.

    Raises:
        ValueError: If ``meters`` is negative.
    """

    if meters < 0:
        raise ValueError("meters must be non-negative")
    return meters * INCHES_PER_METER


def inches_to_meters(inches: float) -> float:
    """Convert inches to meters.

    Args:
        inches: Length in inches. Must be \u2265 0.

    Returns:
        Equivalent length in meters.

    Raises:
        ValueError: If ``inches`` is negative.
    """

    if inches < 0:
        raise ValueError("inches must be non-negative")
    return inches / INCHES_PER_METER


def stitches_per_inch(stitches: int, inches: float) -> float:
    """Return stitch gauge in stitches per inch.

    Args:
        stitches: Number of stitches across the swatch. Must be > 0.
        inches: Width of the swatch in inches. Must be > 0.

    Returns:
        Stitches per inch as a float.

    Raises:
        ValueError: If ``stitches`` or ``inches`` is not positive.
    """
    if stitches <= 0:
        raise ValueError("stitches must be positive")
    if inches <= 0:
        raise ValueError("inches must be positive")
    return stitches / inches


def rows_per_inch(rows: int, inches: float) -> float:
    """Return row gauge in rows per inch.

    Args:
        rows: Number of rows across the swatch. Must be > 0.
        inches: Height of the swatch in inches. Must be > 0.

    Returns:
        Rows per inch as a float.

    Raises:
        ValueError: If ``rows`` or ``inches`` is not positive.
    """
    if rows <= 0:
        raise ValueError("rows must be positive")
    if inches <= 0:
        raise ValueError("inches must be positive")
    return rows / inches


def stitches_per_cm(stitches: int, cm: float) -> float:
    """Return stitch gauge in stitches per centimeter.

    Args:
        stitches: Number of stitches across the swatch. Must be > 0.
        cm: Width of the swatch in centimeters. Must be > 0.

    Returns:
        Stitches per centimeter as a float.

    Raises:
        ValueError: If ``stitches`` or ``cm`` is not positive.
    """
    if stitches <= 0:
        raise ValueError("stitches must be positive")
    if cm <= 0:
        raise ValueError("cm must be positive")
    return stitches / cm


def rows_per_cm(rows: int, cm: float) -> float:
    """Return row gauge in rows per centimeter.

    Args:
        rows: Number of rows across the swatch. Must be > 0.
        cm: Height of the swatch in centimeters. Must be > 0.

    Returns:
        Rows per centimeter as a float.

    Raises:
        ValueError: If ``rows`` or ``cm`` is not positive.
    """
    if rows <= 0:
        raise ValueError("rows must be positive")
    if cm <= 0:
        raise ValueError("cm must be positive")
    return rows / cm


def stitches_per_yard(stitches: int, yards: float) -> float:
    """Return stitch gauge in stitches per yard.

    Args:
        stitches: Number of stitches across the swatch. Must be > 0.
        yards: Width of the swatch in yards. Must be > 0.

    Returns:
        Stitches per yard as a float.

    Raises:
        ValueError: If ``stitches`` or ``yards`` is not positive.
    """

    if stitches <= 0:
        raise ValueError("stitches must be positive")
    if yards <= 0:
        raise ValueError("yards must be positive")
    return stitches / yards


def rows_per_yard(rows: int, yards: float) -> float:
    """Return row gauge in rows per yard.

    Args:
        rows: Number of rows across the swatch. Must be > 0.
        yards: Height of the swatch in yards. Must be > 0.

    Returns:
        Rows per yard as a float.

    Raises:
        ValueError: If ``rows`` or ``yards`` is not positive.
    """

    if rows <= 0:
        raise ValueError("rows must be positive")
    if yards <= 0:
        raise ValueError("yards must be positive")
    return rows / yards


def stitches_per_meter(stitches: int, meters: float) -> float:
    """Return stitch gauge in stitches per meter.

    Args:
        stitches: Number of stitches across the swatch. Must be > 0.
        meters: Width of the swatch in meters. Must be > 0.

    Returns:
        Stitches per meter as a float.

    Raises:
        ValueError: If ``stitches`` or ``meters`` is not positive.
    """

    if stitches <= 0:
        raise ValueError("stitches must be positive")
    if meters <= 0:
        raise ValueError("meters must be positive")
    return stitches / meters


def rows_per_meter(rows: int, meters: float) -> float:
    """Return row gauge in rows per meter.

    Args:
        rows: Number of rows across the swatch. Must be > 0.
        meters: Height of the swatch in meters. Must be > 0.

    Returns:
        Rows per meter as a float.

    Raises:
        ValueError: If ``rows`` or ``meters`` is not positive.
    """

    if rows <= 0:
        raise ValueError("rows must be positive")
    if meters <= 0:
        raise ValueError("meters must be positive")
    return rows / meters


def per_inch_to_per_cm(value: float) -> float:
    """Convert a gauge measured per inch to per centimeter.

    Args:
        value: Gauge value per inch. Must be > 0.

    Returns:
        Gauge value per centimeter.

    Raises:
        ValueError: If ``value`` is not positive.
    """
    if value <= 0:
        raise ValueError("value must be positive")
    return value / CM_PER_INCH


def per_cm_to_per_inch(value: float) -> float:
    """Convert a gauge measured per centimeter to per inch.

    Args:
        value: Gauge value per centimeter. Must be > 0.

    Returns:
        Gauge value per inch.

    Raises:
        ValueError: If ``value`` is not positive.
    """
    if value <= 0:
        raise ValueError("value must be positive")
    return value * CM_PER_INCH


def stitches_for_inches(gauge: float, inches: float) -> int:
    """Return the number of stitches needed for a width in inches.

    Args:
        gauge: Stitch gauge in stitches per inch. Must be > 0.
        inches: Desired width in inches. Must be > 0.

    Returns:
        Required number of stitches rounded to the nearest whole number.
        Values ending in .5 are rounded up.

    Raises:
        ValueError: If ``gauge`` or ``inches`` is not positive.
    """
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    if inches <= 0:
        raise ValueError("inches must be positive")
    return _round_half_up(gauge * inches)


def stitches_for_cm(gauge: float, cm: float) -> int:
    """Return the number of stitches needed for a width in centimeters.

    Args:
        gauge: Stitch gauge in stitches per centimeter. Must be > 0.
        cm: Desired width in centimeters. Must be > 0.

    Returns:
        Required number of stitches rounded to the nearest whole number.
        Values ending in .5 are rounded up.

    Raises:
        ValueError: If ``gauge`` or ``cm`` is not positive.
    """
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    if cm <= 0:
        raise ValueError("cm must be positive")
    return _round_half_up(gauge * cm)


def rows_for_inches(gauge: float, inches: float) -> int:
    """Return the number of rows needed for a height in inches.

    Args:
        gauge: Row gauge in rows per inch. Must be > 0.
        inches: Desired height in inches. Must be > 0.

    Returns:
        Required number of rows rounded to the nearest whole number.
        Values ending in .5 are rounded up.

    Raises:
        ValueError: If ``gauge`` or ``inches`` is not positive.
    """
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    if inches <= 0:
        raise ValueError("inches must be positive")
    return _round_half_up(gauge * inches)


def rows_for_cm(gauge: float, cm: float) -> int:
    """Return the number of rows needed for a height in centimeters.

    Args:
        gauge: Row gauge in rows per centimeter. Must be > 0.
        cm: Desired height in centimeters. Must be > 0.

    Returns:
        Required number of rows rounded to the nearest whole number.
        Values ending in .5 are rounded up.

    Raises:
        ValueError: If ``gauge`` or ``cm`` is not positive.
    """
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    if cm <= 0:
        raise ValueError("cm must be positive")
    return _round_half_up(gauge * cm)


def inches_for_rows(rows: int, gauge: float) -> float:
    """Return the height in inches for a given row count.

    Args:
        rows: Number of rows. Must be > 0.
        gauge: Row gauge in rows per inch. Must be > 0.

    Returns:
        Height in inches.

    Raises:
        ValueError: If ``rows`` or ``gauge`` is not positive.
    """

    if rows <= 0:
        raise ValueError("rows must be positive")
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    return rows / gauge


def cm_for_rows(rows: int, gauge: float) -> float:
    """Return the height in centimeters for a given row count.

    Args:
        rows: Number of rows. Must be > 0.
        gauge: Row gauge in rows per centimeter. Must be > 0.

    Returns:
        Height in centimeters.

    Raises:
        ValueError: If ``rows`` or ``gauge`` is not positive.
    """

    if rows <= 0:
        raise ValueError("rows must be positive")
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    return rows / gauge


def inches_for_stitches(stitches: int, gauge: float) -> float:
    """Return the width in inches for a given stitch count.

    Args:
        stitches: Number of stitches. Must be > 0.
        gauge: Stitch gauge in stitches per inch. Must be > 0.

    Returns:
        Width in inches.

    Raises:
        ValueError: If ``stitches`` or ``gauge`` is not positive.
    """

    if stitches <= 0:
        raise ValueError("stitches must be positive")
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    return stitches / gauge


def cm_for_stitches(stitches: int, gauge: float) -> float:
    """Return the width in centimeters for a given stitch count.

    Args:
        stitches: Number of stitches. Must be > 0.
        gauge: Stitch gauge in stitches per centimeter. Must be > 0.

    Returns:
        Width in centimeters.

    Raises:
        ValueError: If ``stitches`` or ``gauge`` is not positive.
    """

    if stitches <= 0:
        raise ValueError("stitches must be positive")
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    return stitches / gauge
