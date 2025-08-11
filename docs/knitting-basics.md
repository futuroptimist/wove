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
    cm_to_inches,
    inches_to_cm,
    rows_per_cm,
    rows_per_inch,
    stitches_per_cm,
    stitches_per_inch,
)

stitches_per_inch(20, 4)  # 5.0 stitches per inch
rows_per_inch(30, 4)  # 7.5 rows per inch
stitches_per_cm(20, 10)  # 2.0 stitches per cm
rows_per_cm(30, 10)  # 3.0 rows per cm
inches_to_cm(2)  # 5.08 cm
cm_to_inches(10)  # 3.93700787 inches
```

All gauge helpers require positive stitch and row counts and positive measurements.
Passing non-positive values raises ``ValueError``.
