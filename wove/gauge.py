from __future__ import annotations


def _validate_positive(value: float | int, name: str) -> None:
    """Raise ``ValueError`` if *value* is not positive."""
    if value <= 0:
        raise ValueError(f"{name} must be positive")


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
    _validate_positive(stitches, "stitches")
    _validate_positive(inches, "inches")
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
    _validate_positive(rows, "rows")
    _validate_positive(inches, "inches")
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
    _validate_positive(stitches, "stitches")
    _validate_positive(cm, "cm")
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
    _validate_positive(rows, "rows")
    _validate_positive(cm, "cm")
    return rows / cm
