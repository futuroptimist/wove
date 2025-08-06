import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from math_utils import factorial


def test_factorial_basic():
    assert factorial(5) == 120


def test_factorial_zero():
    assert factorial(0) == 1


@pytest.mark.parametrize("n", [-1, 1.5])
def test_factorial_invalid_inputs(n):
    with pytest.raises(ValueError):
        factorial(n)
