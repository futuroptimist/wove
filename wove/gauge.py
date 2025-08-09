from __future__ import annotations


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


def stitches_for_inches(inches: float, gauge: float) -> int:
    """Return stitch count for a desired width in inches.

    Args:
        inches: Desired width in inches. Must be > 0.
        gauge: Stitch gauge in stitches per inch. Must be > 0.

    Returns:
        Number of stitches rounded to the nearest integer.

    Raises:
        ValueError: If ``inches`` or ``gauge`` is not positive.
    """
    if inches <= 0:
        raise ValueError("inches must be positive")
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    return round(inches * gauge)


def rows_for_inches(inches: float, gauge: float) -> int:
    """Return row count for a desired height in inches.

    Args:
        inches: Desired height in inches. Must be > 0.
        gauge: Row gauge in rows per inch. Must be > 0.

    Returns:
        Number of rows rounded to the nearest integer.

    Raises:
        ValueError: If ``inches`` or ``gauge`` is not positive.
    """
    if inches <= 0:
        raise ValueError("inches must be positive")
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    return round(inches * gauge)


def stitches_for_cm(cm: float, gauge: float) -> int:
    """Return stitch count for a desired width in centimeters.

    Args:
        cm: Desired width in centimeters. Must be > 0.
        gauge: Stitch gauge in stitches per centimeter. Must be > 0.

    Returns:
        Number of stitches rounded to the nearest integer.

    Raises:
        ValueError: If ``cm`` or ``gauge`` is not positive.
    """
    if cm <= 0:
        raise ValueError("cm must be positive")
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    return round(cm * gauge)


def rows_for_cm(cm: float, gauge: float) -> int:
    """Return row count for a desired height in centimeters.

    Args:
        cm: Desired height in centimeters. Must be > 0.
        gauge: Row gauge in rows per centimeter. Must be > 0.

    Returns:
        Number of rows rounded to the nearest integer.

    Raises:
        ValueError: If ``cm`` or ``gauge`` is not positive.
    """
    if cm <= 0:
        raise ValueError("cm must be positive")
    if gauge <= 0:
        raise ValueError("gauge must be positive")
    return round(cm * gauge)
