# Knitting Basics

This guide introduces the fundamentals of hand knitting with two standard needles.

## Materials
- A pair of straight knitting needles
- Worsted-weight yarn

## First Steps
1. **Cast on** a row of stitches.
2. Practice the **knit stitch** to create a simple fabric.
3. Learn the **purl stitch** to add texture.
4. **Bind off** to finish your piece.

Continue experimenting with gauge and patterns as you grow more comfortable.

```python
from wove import (
    rows_for_cm,
    rows_for_inches,
    rows_per_cm,
    rows_per_inch,
    stitches_for_cm,
    stitches_for_inches,
    stitches_per_cm,
    stitches_per_inch,
)

stitches_per_inch(20, 4)  # 5.0 stitches per inch
rows_per_inch(30, 4)  # 7.5 rows per inch
stitches_per_cm(20, 10)  # 2.0 stitches per cm
rows_per_cm(30, 10)  # 3.0 rows per cm
stitches_for_inches(4, 5)  # 20 stitches for 4" width at 5 spi
rows_for_inches(4, 7.5)  # 30 rows for 4" height at 7.5 rpi
stitches_for_cm(10, 2)  # 20 stitches for 10 cm width at 2 spc
rows_for_cm(10, 3)  # 30 rows for 10 cm height at 3 rpc
```

All gauge helpers require positive stitch and row counts and positive measurements.
Passing non-positive values raises ``ValueError``.
