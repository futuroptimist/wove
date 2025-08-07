from __future__ import annotations


def stitches_per_inch(stitches: int, inches: float) -> float:
    """Return stitch gauge in stitches per inch.

    Args:
        stitches: Number of stitches across the swatch.
        inches: Width of the swatch in inches. Must be > 0.

    Returns:
        Stitches per inch as a float.

    Raises:
        ValueError: If ``inches`` is not positive.
    """
    if inches <= 0:
        raise ValueError("inches must be positive")
    return stitches / inches
