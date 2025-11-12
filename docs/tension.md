# Yarn Tension Profile Utilities

The `wove.tension` module provides lookup helpers and interpolation tools for managing yarn tension across different yarn weights. These utilities help builders calibrate tensioners, translate hall-effect sensor readings, and estimate feed rates for yarns that fall between documented catalog entries.

## Overview

Phase 3 of the mechanical roadmap ships a catalog of tension profiles covering lace through super bulky yarn weights. Each profile captures:

- **Wraps-per-inch range**: The yarn weight's WPI span
- **Target pull force**: Recommended tension in grams
- **Feed rate**: Suggested yarn feed rate in millimeters per second
- **Pull variation**: Measured variation during 60-second feed trials
- **Trial duration**: Duration of the bench test (default 60.0 seconds)

The module supports three primary workflows:

1. **Lookup**: Retrieve documented profiles by yarn weight or WPI measurement
2. **Interpolation**: Estimate tension and feed rates for in-between yarns
3. **Sensor calibration**: Translate hall-effect sensor readings to grams

## Quick Start

### Retrieve a Known Profile

```python
from wove import get_tension_profile

# Look up a documented yarn weight (case-insensitive)
worsted = get_tension_profile("Worsted")
print(f"Target force: {worsted.target_force_grams} grams")
print(f"Feed rate: {worsted.feed_rate_mm_s} mm/s")
print(f"WPI range: {worsted.wraps_per_inch[0]}-{worsted.wraps_per_inch[1]}")
print(f"Variation: {worsted.pull_variation_percent}%")
```

### Estimate Tension for a Measurement

```python
from wove import estimate_tension_for_wpi

# Estimate target tension for a wraps-per-inch measurement
wpi = 17.5  # Falls between fingering and sport
target_grams = estimate_tension_for_wpi(wpi)
print(f"Recommended tension: {target_grams:.1f} grams")
```

### Find the Nearest Catalog Entry

```python
from wove import find_tension_profile_for_wpi

# Find the documented profile that spans a WPI measurement
profile = find_tension_profile_for_wpi(18.0)
if profile:
    print(f"Matched yarn weight: {profile.weight}")
else:
    print("No exact catalog match—use interpolation helpers")
```

## Catalog Lookup

### List All Profiles

```python
from wove import list_tension_profiles

# Returns profiles ordered from lightest to heaviest
for profile in list_tension_profiles():
    low, high = profile.wraps_per_inch
    print(f"{profile.weight}: {low}-{high} WPI, {profile.target_force_grams}g")
```

### Match by Wraps-Per-Inch

```python
from wove import match_tension_profile_for_wpi

# Find the closest catalog entry and report the WPI difference
match = match_tension_profile_for_wpi(24.0)
print(f"Nearest: {match.profile.weight}")
print(f"WPI difference: {match.difference_wpi:.1f}")
```

### Match by Pull Force

```python
from wove import find_tension_profile_for_force

# Find the closest catalog entry by measured pull force
match = find_tension_profile_for_force(68.0)
print(f"Nearest: {match.profile.weight}")
print(f"Force difference: {match.difference_grams:.1f} grams")
```

## Interpolation

### Estimate Profile from WPI

```python
from wove import estimate_profile_for_wpi

# Interpolate feed rate and variation for a yarn between catalog entries
profile = estimate_profile_for_wpi(17.5)
print(f"Target force: {profile.target_force_grams:.1f} grams")
print(f"Feed rate: {profile.feed_rate_mm_s:.1f} mm/s")
print(f"Variation: {profile.pull_variation_percent:.1f}%")
print(f"Bounds: {profile.lighter_weight} to {profile.heavier_weight}")
print(f"Trial duration: {profile.trial_duration_seconds} seconds")
```

### Estimate Profile from Pull Force

```python
from wove import estimate_profile_for_force

# Interpolate from a measured pull force instead of WPI
profile = estimate_profile_for_force(68.0)
print(f"Estimated WPI: {profile.wraps_per_inch:.1f}")
print(f"Feed rate: {profile.feed_rate_mm_s:.1f} mm/s")
print(f"Bounding weights: {profile.lighter_weight}, {profile.heavier_weight}")
```

### Clamp Tension to Catalog Bounds

```python
from wove import estimate_tension_for_force

# Clamp a measured pull force to the catalog's lightest/heaviest entries
clamped_tension = estimate_tension_for_force(110.0)
print(f"Clamped to: {clamped_tension} grams")  # -> 95.0 (super bulky max)
```

## Hall-Effect Sensor Calibration

The module includes calibration helpers for hall-effect yarn tension sensors. Calibrate the sensor with a few known loads, then translate real-time readings into grams and match them to documented yarn weights.

### Create a Calibration

```python
from wove import HallSensorCalibration, CalibrationPoint

# Define calibration pairs: (sensor_reading, grams)
calibration = HallSensorCalibration.from_pairs([
    (102.0, 20.0),
    (168.5, 55.0),
    (220.0, 85.0),
])
```

### Translate Sensor Readings

```python
from wove import estimate_tension_for_sensor_reading

# Convert a sensor reading to grams of tension
reading = 185.0
grams = estimate_tension_for_sensor_reading(reading, calibration)
print(f"Sensor {reading} → {grams:.1f} grams")
```

### Match Sensor Reading to Catalog

```python
from wove import match_tension_profile_for_sensor_reading

# Find the nearest catalog entry for a sensor reading
match = match_tension_profile_for_sensor_reading(185.0, calibration)
print(f"Yarn weight: {match.profile.weight}")
print(f"Force difference: {match.difference_grams:.1f} grams")
```

### Interpolate Profile from Sensor Reading

```python
from wove import estimate_profile_for_sensor_reading

# Get interpolated feed rate and variation from a sensor reading
profile = estimate_profile_for_sensor_reading(185.0, calibration)
print(f"Feed rate: {profile.feed_rate_mm_s:.1f} mm/s")
print(f"Variation: {profile.pull_variation_percent:.1f}%")
print(f"Bounds: {profile.lighter_weight} to {profile.heavier_weight}")
```

### Compute Target Sensor Reading

```python
from wove import estimate_sensor_reading_for_tension

# Determine the sensor reading for a desired tension
target_grams = 65.0  # Worsted target
target_reading = estimate_sensor_reading_for_tension(target_grams, calibration)
print(f"Target reading for {target_grams}g: {target_reading:.1f}")
```

### Clamping Behavior

By default, sensor interpolation clamps readings outside the calibration range to the nearest measured value:

```python
from wove import estimate_tension_for_sensor_reading

# Readings outside the calibration range are clamped
clamped = estimate_tension_for_sensor_reading(250.0, calibration, clamp=True)
print(f"Clamped to: {clamped:.1f} grams")  # -> 85.0 (highest calibration point)

# Pass clamp=False to raise ValueError instead
try:
    unclamped = estimate_tension_for_sensor_reading(250.0, calibration, clamp=False)
except ValueError as e:
    print(f"Error: {e}")  # -> "Reading 250.0 above calibration range"
```

## Data Classes

### TensionProfile

Represents a documented yarn weight with bench-test results:

```python
from wove import TensionProfile

profile = TensionProfile(
    weight="worsted",
    wraps_per_inch=(9, 12),
    target_force_grams=65.0,
    feed_rate_mm_s=33.0,
    pull_variation_percent=3.0,
    trial_duration_seconds=60.0,
)
print(profile.midpoint_wpi)  # -> 10.5
```

### EstimatedTension

Holds interpolated tension data with bounding yarn weights:

```python
from wove import estimate_profile_for_wpi

estimated = estimate_profile_for_wpi(17.5)
print(estimated.target_force_grams)  # Interpolated tension
print(estimated.lighter_weight)       # Bounding lighter yarn
print(estimated.heavier_weight)       # Bounding heavier yarn
```

### ForceMatch and WpiMatch

Returned by `find_tension_profile_for_force` and `match_tension_profile_for_wpi`:

```python
from wove import find_tension_profile_for_force, match_tension_profile_for_wpi

force_match = find_tension_profile_for_force(68.0)
print(force_match.profile.weight)     # Nearest yarn weight
print(force_match.difference_grams)   # Absolute difference in grams

wpi_match = match_tension_profile_for_wpi(24.0)
print(wpi_match.profile.weight)       # Nearest yarn weight
print(wpi_match.difference_wpi)       # Absolute WPI difference
```

### CalibrationPoint and HallSensorCalibration

Define sensor calibration data:

```python
from wove import CalibrationPoint, HallSensorCalibration

# Manual construction
points = (
    CalibrationPoint(reading=102.0, grams=20.0),
    CalibrationPoint(reading=168.5, grams=55.0),
    CalibrationPoint(reading=220.0, grams=85.0),
)
calibration = HallSensorCalibration(points=points)

# Or use the convenience constructor
calibration = HallSensorCalibration.from_pairs([
    (102.0, 20.0),
    (168.5, 55.0),
    (220.0, 85.0),
])

# Access calibration bounds
print(calibration.points[0].grams)   # Lightest calibration point
print(calibration.points[-1].grams)  # Heaviest calibration point
```

## Catalog Reference

The module ships with these documented tension profiles (ordered lightest to heaviest):

| Yarn Weight  | WPI Range | Target Force (g) | Feed Rate (mm/s) | Variation (%) | Trial Duration (s) |
|--------------|-----------|------------------|------------------|---------------|--------------------|
| Lace         | 28-32     | 20.0             | 45.0             | 6.0           | 60.0               |
| Fingering    | 18-22     | 35.0             | 40.0             | 4.5           | 60.0               |
| Sport        | 15-18     | 45.0             | 38.0             | 4.0           | 60.0               |
| DK           | 12-15     | 55.0             | 35.0             | 3.5           | 60.0               |
| Worsted      | 9-12      | 65.0             | 33.0             | 3.0           | 60.0               |
| Bulky        | 7-9       | 80.0             | 30.0             | 2.5           | 60.0               |
| Super Bulky  | 5-7       | 95.0             | 28.0             | 2.0           | 60.0               |

Access the catalog directly:

```python
from wove import TENSION_PROFILES

# Dictionary keyed by yarn weight (lowercase)
for weight_name, profile in TENSION_PROFILES.items():
    print(f"{weight_name}: {profile.target_force_grams}g")
```

## Usage in Calibration Scripts

### Workflow 1: Measure WPI, Estimate Tension

```python
from wove import estimate_profile_for_wpi

# Builder wraps yarn around a gauge and counts
measured_wpi = 13.5

# Get interpolated tension target and feed rate
profile = estimate_profile_for_wpi(measured_wpi)
print(f"Set tensioner to: {profile.target_force_grams:.1f} grams")
print(f"Use feed rate: {profile.feed_rate_mm_s:.1f} mm/s")
print(f"Expect {profile.pull_variation_percent:.1f}% variation over {profile.trial_duration_seconds}s trial")
print(f"Yarn falls between {profile.lighter_weight} and {profile.heavier_weight}")
```

### Workflow 2: Measure Pull Force, Match to Catalog

```python
from wove import find_tension_profile_for_force

# Builder uses a load cell to measure actual tension
measured_force = 62.0

# Find the nearest documented profile
match = find_tension_profile_for_force(measured_force)
print(f"Closest match: {match.profile.weight}")
print(f"Catalog target: {match.profile.target_force_grams}g")
print(f"Your measurement: {measured_force}g")
print(f"Difference: {match.difference_grams:.1f}g")
```

### Workflow 3: Hall-Effect Sensor Integration

```python
from wove import (
    HallSensorCalibration,
    estimate_tension_for_sensor_reading,
    estimate_profile_for_sensor_reading,
)

# Calibrate sensor with three known loads
calibration = HallSensorCalibration.from_pairs([
    (102.0, 20.0),   # Sensor reads 102.0 under 20g load
    (168.5, 55.0),   # Sensor reads 168.5 under 55g load
    (220.0, 85.0),   # Sensor reads 220.0 under 85g load
])

# During a run, read live sensor data
live_reading = 185.0
current_tension = estimate_tension_for_sensor_reading(live_reading, calibration)
print(f"Current tension: {current_tension:.1f} grams")

# Get feed-rate guidance for the current reading
profile = estimate_profile_for_sensor_reading(live_reading, calibration)
print(f"Recommended feed rate: {profile.feed_rate_mm_s:.1f} mm/s")
```

## Error Handling

All functions validate inputs and raise `ValueError` for invalid arguments:

```python
from wove import estimate_tension_for_wpi, get_tension_profile

# Negative or zero WPI
try:
    estimate_tension_for_wpi(-5.0)
except ValueError as e:
    print(f"Error: {e}")  # -> "wraps_per_inch must be positive"

# Unknown yarn weight
try:
    get_tension_profile("unknown_weight")
except ValueError as e:
    print(f"Error: {e}")  # -> "Unknown yarn weight 'unknown_weight'"

# Invalid sensor reading
from wove import HallSensorCalibration, estimate_tension_for_sensor_reading
import math

calibration = HallSensorCalibration.from_pairs([(100.0, 20.0), (200.0, 80.0)])
try:
    estimate_tension_for_sensor_reading(math.nan, calibration)
except ValueError as e:
    print(f"Error: {e}")  # -> "Sensor reading must be a finite value"
```

## Integration with Design Roadmap

The tension profiles documented here align with the [v1c mechanical design roadmap](wove-v1c-design.md#yarn-handling). The roadmap describes:

- Dual-post tensioner design with replaceable felt pads
- Hall-effect sensor mounting for tension feedback
- Feed rate recommendations for each yarn weight
- Expected variation during 60-second feed trials

Use these utilities to:

1. **Calibrate passive tensioners**: Match measured pull force to catalog targets
2. **Configure active tensioners**: Drive servo adjusters using sensor feedback
3. **Validate feed rates**: Compare planner output against documented recommendations
4. **Log calibration data**: Record WPI, force, and sensor readings for traceability

## See Also

- [Gauge calculators](gauge.md) for stitch and row conversions
- [Machine profiles](machine-profile.md) for axis configuration and homing
- [Mechanical design roadmap](wove-v1c-design.md) for hardware context
- [Pattern CLI](pattern-cli.md) for motion planning integration

## API Reference

### Profile Lookup

- `get_tension_profile(weight: str) -> TensionProfile`: Retrieve profile by yarn weight name
- `list_tension_profiles() -> Iterable[TensionProfile]`: List all profiles, lightest to heaviest
- `find_tension_profile_for_wpi(wraps_per_inch: float) -> TensionProfile | None`: Find profile spanning WPI
- `find_tension_profile_for_force(force_grams: float) -> ForceMatch`: Find nearest profile by pull force
- `match_tension_profile_for_wpi(wraps_per_inch: float) -> WpiMatch`: Find nearest profile by WPI

### Interpolation

- `estimate_tension_for_wpi(wraps_per_inch: float) -> float`: Estimate target tension for WPI
- `estimate_tension_for_force(force_grams: float) -> float`: Clamp pull force to catalog bounds
- `estimate_profile_for_wpi(wraps_per_inch: float) -> EstimatedTension`: Interpolate full profile from WPI
- `estimate_profile_for_force(force_grams: float) -> EstimatedTension`: Interpolate full profile from force

### Sensor Calibration

- `HallSensorCalibration.from_pairs(pairs: Sequence[Tuple[float, float]]) -> HallSensorCalibration`: Create calibration from (reading, grams) pairs
- `estimate_tension_for_sensor_reading(reading: float, calibration: HallSensorCalibration, *, clamp: bool = True) -> float`: Convert sensor reading to grams
- `estimate_sensor_reading_for_tension(grams: float, calibration: HallSensorCalibration, *, clamp: bool = True) -> float`: Convert grams to sensor reading
- `match_tension_profile_for_sensor_reading(reading: float, calibration: HallSensorCalibration, *, clamp: bool = True) -> ForceMatch`: Find nearest profile for sensor reading
- `estimate_profile_for_sensor_reading(reading: float, calibration: HallSensorCalibration, *, clamp: bool = True) -> EstimatedTension`: Interpolate profile from sensor reading

### Constants

- `DEFAULT_TRIAL_DURATION_SECONDS`: Default trial duration (60.0 seconds)
- `TENSION_PROFILES`: Dictionary of documented tension profiles keyed by yarn weight

### Data Classes

- `TensionProfile`: Documented yarn weight with bench-test results
- `EstimatedTension`: Interpolated tension data with bounding yarn weights
- `ForceMatch`: Nearest profile match by pull force with difference in grams
- `WpiMatch`: Nearest profile match by WPI with difference in wraps-per-inch
- `CalibrationPoint`: Single sensor calibration point (reading, grams)
- `HallSensorCalibration`: Calibration helper for hall-effect tension sensors
