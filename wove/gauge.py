from __future__ import annotations

CM_PER_INCH = 2.54


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
