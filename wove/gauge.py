from __future__ import annotations

CM_PER_INCH = 2.54


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

    Raises:
        ValueError: If ``gauge`` or ``inches`` is not positive.
    """
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    if inches <= 0:
        raise ValueError("inches must be positive")
    return int(round(gauge * inches))


def stitches_for_cm(gauge: float, cm: float) -> int:
    """Return the number of stitches needed for a width in centimeters.

    Args:
        gauge: Stitch gauge in stitches per centimeter. Must be > 0.
        cm: Desired width in centimeters. Must be > 0.

    Returns:
        Required number of stitches rounded to the nearest whole number.

    Raises:
        ValueError: If ``gauge`` or ``cm`` is not positive.
    """
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    if cm <= 0:
        raise ValueError("cm must be positive")
    return int(round(gauge * cm))


def rows_for_inches(gauge: float, inches: float) -> int:
    """Return the number of rows needed for a height in inches.

    Args:
        gauge: Row gauge in rows per inch. Must be > 0.
        inches: Desired height in inches. Must be > 0.

    Returns:
        Required number of rows rounded to the nearest whole number.

    Raises:
        ValueError: If ``gauge`` or ``inches`` is not positive.
    """

    if gauge <= 0:
        raise ValueError("gauge must be positive")
    if inches <= 0:
        raise ValueError("inches must be positive")
    return int(round(gauge * inches))


def rows_for_cm(gauge: float, cm: float) -> int:
    """Return the number of rows needed for a height in centimeters.

    Args:
        gauge: Row gauge in rows per centimeter. Must be > 0.
        cm: Desired height in centimeters. Must be > 0.

    Returns:
        Required number of rows rounded to the nearest whole number.

    Raises:
        ValueError: If ``gauge`` or ``cm`` is not positive.
    """

    if gauge <= 0:
        raise ValueError("gauge must be positive")
    if cm <= 0:
        raise ValueError("cm must be positive")
    return int(round(gauge * cm))
