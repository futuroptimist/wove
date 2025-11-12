"""Test code examples from docs/tension.md remain valid."""

from wove import (
    DEFAULT_TRIAL_DURATION_SECONDS,
    TENSION_PROFILES,
    CalibrationPoint,
    EstimatedTension,
    ForceMatch,
    HallSensorCalibration,
    TensionProfile,
    WpiMatch,
    estimate_profile_for_force,
    estimate_profile_for_sensor_reading,
    estimate_profile_for_wpi,
    estimate_sensor_reading_for_tension,
    estimate_tension_for_force,
    estimate_tension_for_sensor_reading,
    estimate_tension_for_wpi,
    find_tension_profile_for_force,
    find_tension_profile_for_wpi,
    get_tension_profile,
    list_tension_profiles,
    match_tension_profile_for_sensor_reading,
    match_tension_profile_for_wpi,
)


def test_retrieve_known_profile():
    """Validate the 'Retrieve a Known Profile' doc example."""
    worsted = get_tension_profile("Worsted")
    assert worsted.target_force_grams == 65.0
    assert worsted.feed_rate_mm_s == 33.0
    assert worsted.wraps_per_inch == (9, 12)
    assert worsted.pull_variation_percent == 3.0
    assert worsted.trial_duration_seconds == DEFAULT_TRIAL_DURATION_SECONDS


def test_estimate_tension_for_measurement():
    """Validate the 'Estimate Tension for a Measurement' doc example."""
    wpi = 17.5
    target_grams = estimate_tension_for_wpi(wpi)
    # Should interpolate between fingering (35g) and sport (45g)
    assert 35.0 < target_grams < 45.0
    assert abs(target_grams - 42.14) < 0.5


def test_find_nearest_catalog_entry():
    """Validate the 'Find the Nearest Catalog Entry' doc example."""
    profile = find_tension_profile_for_wpi(18.0)
    assert profile is not None
    # 18.0 falls in the fingering range (18-22)
    assert profile.weight == "fingering"


def test_list_all_profiles():
    """Validate the 'List All Profiles' doc example."""
    profiles = list(list_tension_profiles())
    # Should return 7 profiles ordered lightest to heaviest
    assert len(profiles) == 7
    assert profiles[0].weight == "lace"
    assert profiles[-1].weight == "super bulky"
    # Verify lightest to heaviest ordering by midpoint WPI (descending)
    midpoints = [p.midpoint_wpi for p in profiles]
    assert midpoints == sorted(midpoints, reverse=True)


def test_match_by_wraps_per_inch():
    """Validate the 'Match by Wraps-Per-Inch' doc example."""
    match = match_tension_profile_for_wpi(24.0)
    # 24.0 is closest to fingering (18-22) with difference of 2.0
    assert match.profile.weight == "fingering"
    assert match.difference_wpi == 2.0


def test_match_by_pull_force():
    """Validate the 'Match by Pull Force' doc example."""
    match = find_tension_profile_for_force(68.0)
    # 68.0 is closest to worsted (65.0g) with difference of 3.0
    assert match.profile.weight == "worsted"
    assert abs(match.difference_grams - 3.0) < 0.01


def test_estimate_profile_from_wpi():
    """Validate the 'Estimate Profile from WPI' doc example."""
    profile = estimate_profile_for_wpi(17.5)
    # Should interpolate between fingering and sport
    assert isinstance(profile, EstimatedTension)
    assert 35.0 < profile.target_force_grams < 45.0
    assert 38.0 < profile.feed_rate_mm_s < 40.0
    assert 4.0 < profile.pull_variation_percent < 4.5
    assert profile.lighter_weight == "fingering"
    assert profile.heavier_weight == "sport"
    assert profile.trial_duration_seconds == DEFAULT_TRIAL_DURATION_SECONDS


def test_estimate_profile_from_pull_force():
    """Validate the 'Estimate Profile from Pull Force' doc example."""
    profile = estimate_profile_for_force(68.0)
    # Should interpolate near worsted/bulky boundary
    assert isinstance(profile, EstimatedTension)
    assert profile.wraps_per_inch > 9.0  # Above worsted midpoint
    assert 30.0 < profile.feed_rate_mm_s < 34.0


def test_clamp_tension_to_catalog_bounds():
    """Validate the 'Clamp Tension to Catalog Bounds' doc example."""
    clamped_tension = estimate_tension_for_force(110.0)
    # Should clamp to super bulky max (95.0g)
    assert clamped_tension == 95.0


def test_create_calibration():
    """Validate the 'Create a Calibration' doc example."""
    calibration = HallSensorCalibration.from_pairs([
        (102.0, 20.0),
        (168.5, 55.0),
        (220.0, 85.0),
    ])
    assert isinstance(calibration, HallSensorCalibration)
    assert len(calibration.points) == 3
    assert calibration.points[0].reading == 102.0
    assert calibration.points[0].grams == 20.0


def test_translate_sensor_readings():
    """Validate the 'Translate Sensor Readings' doc example."""
    calibration = HallSensorCalibration.from_pairs([
        (102.0, 20.0),
        (168.5, 55.0),
        (220.0, 85.0),
    ])
    reading = 185.0
    grams = estimate_tension_for_sensor_reading(reading, calibration)
    # Should interpolate between 168.5->55g and 220.0->85g
    assert 55.0 < grams < 85.0
    assert abs(grams - 64.61) < 1.0


def test_match_sensor_reading_to_catalog():
    """Validate the 'Match Sensor Reading to Catalog' doc example."""
    calibration = HallSensorCalibration.from_pairs([
        (102.0, 20.0),
        (168.5, 55.0),
        (220.0, 85.0),
    ])
    match = match_tension_profile_for_sensor_reading(185.0, calibration)
    assert isinstance(match, ForceMatch)
    # Reading 185.0 -> ~61g, closest to dk (55g)
    assert match.profile.weight in ("dk", "worsted")


def test_interpolate_profile_from_sensor_reading():
    """Validate the 'Interpolate Profile from Sensor Reading' doc example."""
    calibration = HallSensorCalibration.from_pairs([
        (102.0, 20.0),
        (168.5, 55.0),
        (220.0, 85.0),
    ])
    profile = estimate_profile_for_sensor_reading(185.0, calibration)
    assert isinstance(profile, EstimatedTension)
    assert 30.0 < profile.feed_rate_mm_s < 40.0
    assert profile.lighter_weight in ("dk", "worsted", "bulky")


def test_compute_target_sensor_reading():
    """Validate the 'Compute Target Sensor Reading' doc example."""
    calibration = HallSensorCalibration.from_pairs([
        (102.0, 20.0),
        (168.5, 55.0),
        (220.0, 85.0),
    ])
    target_grams = 65.0
    target_reading = estimate_sensor_reading_for_tension(target_grams, calibration)
    # 65g falls between 55g->168.5 and 85g->220.0
    assert 168.5 < target_reading < 220.0
    assert abs(target_reading - 185.73) < 1.0


def test_clamping_behavior_clamp_true():
    """Validate the 'Clamping Behavior' doc example with clamp=True."""
    calibration = HallSensorCalibration.from_pairs([
        (102.0, 20.0),
        (168.5, 55.0),
        (220.0, 85.0),
    ])
    clamped = estimate_tension_for_sensor_reading(250.0, calibration, clamp=True)
    # Should clamp to highest calibration point
    assert clamped == 85.0


def test_clamping_behavior_clamp_false():
    """Validate the 'Clamping Behavior' doc example with clamp=False."""
    calibration = HallSensorCalibration.from_pairs([
        (102.0, 20.0),
        (168.5, 55.0),
        (220.0, 85.0),
    ])
    try:
        estimate_tension_for_sensor_reading(250.0, calibration, clamp=False)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "above calibration range" in str(e)


def test_tension_profile_data_class():
    """Validate the 'TensionProfile' doc example."""
    profile = TensionProfile(
        weight="worsted",
        wraps_per_inch=(9, 12),
        target_force_grams=65.0,
        feed_rate_mm_s=33.0,
        pull_variation_percent=3.0,
        trial_duration_seconds=60.0,
    )
    assert profile.midpoint_wpi == 10.5


def test_estimated_tension_data_class():
    """Validate the 'EstimatedTension' doc example."""
    estimated = estimate_profile_for_wpi(17.5)
    assert isinstance(estimated, EstimatedTension)
    assert hasattr(estimated, "target_force_grams")
    assert hasattr(estimated, "lighter_weight")
    assert hasattr(estimated, "heavier_weight")
    assert estimated.lighter_weight == "fingering"
    assert estimated.heavier_weight == "sport"


def test_force_match_and_wpi_match_data_classes():
    """Validate the 'ForceMatch and WpiMatch' doc example."""
    force_match = find_tension_profile_for_force(68.0)
    assert isinstance(force_match, ForceMatch)
    assert force_match.profile.weight == "worsted"
    assert abs(force_match.difference_grams - 3.0) < 0.01

    wpi_match = match_tension_profile_for_wpi(24.0)
    assert isinstance(wpi_match, WpiMatch)
    assert wpi_match.profile.weight == "fingering"
    assert wpi_match.difference_wpi == 2.0


def test_calibration_point_and_hall_sensor_calibration():
    """Validate the 'CalibrationPoint and HallSensorCalibration' doc example."""
    # Manual construction
    points = (
        CalibrationPoint(reading=102.0, grams=20.0),
        CalibrationPoint(reading=168.5, grams=55.0),
        CalibrationPoint(reading=220.0, grams=85.0),
    )
    calibration = HallSensorCalibration(points=points)
    assert len(calibration.points) == 3

    # Convenience constructor
    calibration2 = HallSensorCalibration.from_pairs([
        (102.0, 20.0),
        (168.5, 55.0),
        (220.0, 85.0),
    ])
    assert calibration2.points[0].grams == 20.0
    assert calibration2.points[-1].grams == 85.0


def test_catalog_reference_table():
    """Validate the catalog reference table in the docs."""
    expected_catalog = [
        ("lace", (28, 32), 20.0, 45.0, 6.0),
        ("fingering", (18, 22), 35.0, 40.0, 4.5),
        ("sport", (15, 18), 45.0, 38.0, 4.0),
        ("dk", (12, 15), 55.0, 35.0, 3.5),
        ("worsted", (9, 12), 65.0, 33.0, 3.0),
        ("bulky", (7, 9), 80.0, 30.0, 2.5),
        ("super bulky", (5, 7), 95.0, 28.0, 2.0),
    ]

    for weight_name, wpi_range, force, feed_rate, variation in expected_catalog:
        profile = TENSION_PROFILES[weight_name]
        assert profile.wraps_per_inch == wpi_range
        assert profile.target_force_grams == force
        assert profile.feed_rate_mm_s == feed_rate
        assert profile.pull_variation_percent == variation
        assert profile.trial_duration_seconds == DEFAULT_TRIAL_DURATION_SECONDS


def test_error_handling_negative_wpi():
    """Validate the error handling example for negative WPI."""
    try:
        estimate_tension_for_wpi(-5.0)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "wraps_per_inch must be positive" in str(e)


def test_error_handling_unknown_yarn_weight():
    """Validate the error handling example for unknown yarn weight."""
    try:
        get_tension_profile("unknown_weight")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unknown yarn weight" in str(e)


def test_error_handling_invalid_sensor_reading():
    """Validate the error handling example for invalid sensor reading."""
    import math

    calibration = HallSensorCalibration.from_pairs([(100.0, 20.0), (200.0, 80.0)])
    try:
        estimate_tension_for_sensor_reading(math.nan, calibration)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Sensor reading must be a finite value" in str(e)


def test_workflow_1_measure_wpi_estimate_tension():
    """Validate Workflow 1: Measure WPI, Estimate Tension."""
    measured_wpi = 13.5
    profile = estimate_profile_for_wpi(measured_wpi)

    # 13.5 matches the midpoint of DK (12-15), so both bounds are DK
    assert isinstance(profile, EstimatedTension)
    assert profile.target_force_grams == 55.0
    assert profile.feed_rate_mm_s == 35.0
    assert profile.pull_variation_percent == 3.5
    assert profile.lighter_weight == "dk"
    assert profile.heavier_weight == "dk"
    assert profile.trial_duration_seconds == DEFAULT_TRIAL_DURATION_SECONDS


def test_workflow_2_measure_pull_force_match_catalog():
    """Validate Workflow 2: Measure Pull Force, Match to Catalog."""
    measured_force = 62.0
    match = find_tension_profile_for_force(measured_force)

    assert isinstance(match, ForceMatch)
    assert match.profile.weight == "worsted"
    assert match.profile.target_force_grams == 65.0
    assert abs(match.difference_grams - 3.0) < 0.01


def test_workflow_3_hall_effect_sensor_integration():
    """Validate Workflow 3: Hall-Effect Sensor Integration."""
    calibration = HallSensorCalibration.from_pairs([
        (102.0, 20.0),
        (168.5, 55.0),
        (220.0, 85.0),
    ])

    live_reading = 185.0
    current_tension = estimate_tension_for_sensor_reading(live_reading, calibration)
    assert 55.0 < current_tension < 85.0

    profile = estimate_profile_for_sensor_reading(live_reading, calibration)
    assert isinstance(profile, EstimatedTension)
    assert 30.0 < profile.feed_rate_mm_s < 40.0
