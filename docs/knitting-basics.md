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

## Gauge
Gauge ensures your finished piece matches the intended dimensions. Knit a small
swatch before starting larger projects.

1. Cast on at least 20 stitches.
2. Knit a square about 4 inches (10 cm) across.
3. Measure stitches and rows; adjust needle size if needed.

```python
from wove import (
    rows_per_cm,
    rows_per_inch,
    stitches_per_cm,
    stitches_per_inch,
)

stitches_per_inch(20, 4)  # 5.0 stitches per inch
rows_per_inch(30, 4)  # 7.5 rows per inch
stitches_per_cm(20, 10)  # 2.0 stitches per cm
rows_per_cm(30, 10)  # 3.0 rows per cm
```

All gauge helpers require positive stitch and row counts and positive
measurements. Passing non-positive values raises ``ValueError``.
