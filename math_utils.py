"""Utility math functions used across the project."""

from __future__ import annotations


def factorial(n: int) -> int:
    """Return the factorial of ``n``.

    Parameters
    ----------
    n: int
        Non-negative integer whose factorial to compute.

    Returns
    -------
    int
        The factorial of ``n``.

    Raises
    ------
    ValueError
        If ``n`` is negative or not an integer.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
