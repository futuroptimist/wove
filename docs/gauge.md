# Gauge utilities

The `wove.gauge` module provides helpers for calculating stitch and row gauge and
converting measurements between inches and centimeters.

```python
from wove import stitches_per_inch, per_cm_to_per_inch

stitches_per_inch(20, 4)  # 5.0
per_cm_to_per_inch(2.0)  # 5.08
```

Each function checks that its inputs are positive and raises `ValueError` when
an invalid value is supplied.

