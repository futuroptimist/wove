# Gauge utilities

The `wove.gauge` module offers helpers for computing stitch and row gauge and
converting measurements between inches and centimeters. To measure gauge, knit a
swatch, measure its width or height, and pass both the stitch or row count and the
measurement to the appropriate function.

```python
from wove import stitches_per_inch, rows_per_inch, per_cm_to_per_inch

stitches_per_inch(20, 4)  # 5.0 stitches per inch
rows_per_inch(30, 4)      # 7.5 rows per inch
per_cm_to_per_inch(2.0)   # ~5.08 per inch
```

Gauge helpers require positive counts and measurements. Passing zero or negative
values raises ``ValueError``.
