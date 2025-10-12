from __future__ import annotations

import math

import pytest

from wove import tension


def test_get_tension_profile_is_case_insensitive() -> None:
    profile = tension.get_tension_profile("Worsted")
    assert isinstance(profile, tension.TensionProfile)
    assert profile.weight == "worsted"
    assert math.isclose(
        profile.trial_duration_seconds,
        tension.DEFAULT_TRIAL_DURATION_SECONDS,
    )


def test_get_tension_profile_unknown_weight() -> None:
    with pytest.raises(ValueError):
        tension.get_tension_profile("thread")


def test_list_tension_profiles_orders_light_to_heavy() -> None:
    ordered = list(tension.list_tension_profiles())
    midpoints = [profile.midpoint_wpi for profile in ordered]
    assert midpoints == sorted(midpoints, reverse=True)


def test_find_tension_profile_for_wpi_matches_catalog_range() -> None:
    profile = tension.find_tension_profile_for_wpi(10.5)
    assert profile is not None
    assert profile.weight == "worsted"


def test_find_tension_profile_for_wpi_prefers_lighter_boundary() -> None:
    profile = tension.find_tension_profile_for_wpi(18.0)
    assert profile is not None
    assert profile.weight == "fingering"


def test_find_tension_profile_for_wpi_returns_none_when_unmatched() -> None:
    assert tension.find_tension_profile_for_wpi(40.0) is None


def test_find_tension_profile_for_wpi_requires_positive_values() -> None:
    with pytest.raises(ValueError):
        tension.find_tension_profile_for_wpi(0)
    with pytest.raises(ValueError):
        tension.find_tension_profile_for_wpi(float("nan"))


def test_find_tension_profile_for_force_returns_nearest() -> None:
    match = tension.find_tension_profile_for_force(67.0)
    assert match.profile.weight == "worsted"
    assert math.isclose(match.difference_grams, 2.0)


def test_find_tension_profile_for_force_prefers_lower_force_on_tie() -> None:
    match = tension.find_tension_profile_for_force(50.0)
    assert match.profile.weight == "sport"
    assert math.isclose(match.difference_grams, 5.0)


def test_find_tension_profile_for_force_handles_extremes() -> None:
    high = tension.find_tension_profile_for_force(120.0)
    assert high.profile.weight == "super bulky"
    assert high.difference_grams == pytest.approx(25.0)


def test_find_tension_profile_for_force_validates_input() -> None:
    with pytest.raises(ValueError):
        tension.find_tension_profile_for_force(0.0)
    with pytest.raises(ValueError):
        tension.find_tension_profile_for_force(float("nan"))
    with pytest.raises(ValueError):
        tension.find_tension_profile_for_force(float("inf"))


def test_estimate_tension_for_exact_profile() -> None:
    sport = tension.get_tension_profile("sport")
    target = tension.estimate_tension_for_wpi(sport.midpoint_wpi)
    assert math.isclose(target, sport.target_force_grams)


def test_estimate_tension_interpolates_between_weights() -> None:
    fingering = tension.get_tension_profile("fingering")
    sport = tension.get_tension_profile("sport")
    midpoint = (fingering.midpoint_wpi + sport.midpoint_wpi) / 2.0
    estimated = tension.estimate_tension_for_wpi(midpoint)
    assert fingering.target_force_grams < estimated < sport.target_force_grams


def test_estimate_tension_clamps_extremes() -> None:
    lace = tension.get_tension_profile("lace")
    super_bulky = tension.get_tension_profile("super bulky")
    assert (
        tension.estimate_tension_for_wpi(lace.midpoint_wpi * 2)
        == lace.target_force_grams
    )
    assert (
        tension.estimate_tension_for_wpi(super_bulky.midpoint_wpi / 2)
        == super_bulky.target_force_grams
    )


def test_estimate_tension_rejects_non_positive_values() -> None:
    with pytest.raises(ValueError):
        tension.estimate_tension_for_wpi(0)


def test_estimate_profile_for_exact_weight() -> None:
    profile = tension.get_tension_profile("dk")
    estimated = tension.estimate_profile_for_wpi(profile.midpoint_wpi)

    assert estimated.wraps_per_inch == profile.midpoint_wpi
    assert estimated.heavier_weight == profile.weight
    assert estimated.lighter_weight == profile.weight
    assert math.isclose(
        estimated.target_force_grams,
        profile.target_force_grams,
    )
    assert math.isclose(estimated.feed_rate_mm_s, profile.feed_rate_mm_s)
    assert math.isclose(
        estimated.pull_variation_percent,
        profile.pull_variation_percent,
    )
    assert math.isclose(
        estimated.trial_duration_seconds,
        profile.trial_duration_seconds,
    )


def test_estimate_profile_interpolates_between_weights() -> None:
    fingering = tension.get_tension_profile("fingering")
    sport = tension.get_tension_profile("sport")
    midpoint = (fingering.midpoint_wpi + sport.midpoint_wpi) / 2.0

    estimated = tension.estimate_profile_for_wpi(midpoint)

    assert estimated.heavier_weight == sport.weight
    assert estimated.lighter_weight == fingering.weight
    assert (
        min(fingering.target_force_grams, sport.target_force_grams)
        < estimated.target_force_grams
        < max(fingering.target_force_grams, sport.target_force_grams)
    )
    assert (
        min(fingering.feed_rate_mm_s, sport.feed_rate_mm_s)
        < estimated.feed_rate_mm_s
        < max(fingering.feed_rate_mm_s, sport.feed_rate_mm_s)
    )
    assert (
        min(
            fingering.pull_variation_percent,
            sport.pull_variation_percent,
        )
        < estimated.pull_variation_percent
        < max(
            fingering.pull_variation_percent,
            sport.pull_variation_percent,
        )
    )
    expected_duration = (
        fingering.trial_duration_seconds + sport.trial_duration_seconds
    ) / 2.0
    assert math.isclose(
        estimated.trial_duration_seconds,
        expected_duration,
    )


def test_estimate_profile_clamps_to_bounds() -> None:
    lace = tension.get_tension_profile("lace")
    super_bulky = tension.get_tension_profile("super bulky")

    low = tension.estimate_profile_for_wpi(lace.midpoint_wpi * 2)
    high = tension.estimate_profile_for_wpi(super_bulky.midpoint_wpi / 2)

    assert low.heavier_weight == lace.weight
    assert low.lighter_weight == lace.weight
    assert math.isclose(low.target_force_grams, lace.target_force_grams)

    assert high.heavier_weight == super_bulky.weight
    assert high.lighter_weight == super_bulky.weight
    assert math.isclose(
        high.target_force_grams,
        super_bulky.target_force_grams,
    )
    assert math.isclose(
        low.trial_duration_seconds,
        lace.trial_duration_seconds,
    )
    assert math.isclose(
        high.trial_duration_seconds,
        super_bulky.trial_duration_seconds,
    )


def test_estimate_profile_requires_positive_wpi() -> None:
    with pytest.raises(ValueError):
        tension.estimate_profile_for_wpi(0)


def test_estimate_profile_handles_zero_span_intervals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lower = tension.TensionProfile(
        weight="custom-low",
        wraps_per_inch=(12, 12),
        target_force_grams=50.0,
        feed_rate_mm_s=30.0,
        pull_variation_percent=3.0,
        trial_duration_seconds=48.0,
    )
    upper = tension.TensionProfile(
        weight="custom-high",
        wraps_per_inch=(12, 12),
        target_force_grams=55.0,
        feed_rate_mm_s=32.0,
        pull_variation_percent=2.5,
        trial_duration_seconds=52.0,
    )

    monkeypatch.setattr(
        tension,
        "list_tension_profiles",
        lambda: [lower, upper],
    )

    class FakeWpi:
        """Force the zero-span interpolation branch for profile estimation."""

        def __init__(self, value: float) -> None:
            self.value = value
            self._le_calls = 0
            self._ge_calls = 0

        def __float__(self) -> float:
            return self.value

        def __le__(self, other: float) -> bool:  # type: ignore[override]
            self._le_calls += 1
            if self._le_calls in (1, 2):
                return False  # skip the positive check and lower clamp guard
            return self.value <= other

        def __ge__(self, other: float) -> bool:  # type: ignore[override]
            self._ge_calls += 1
            if self._ge_calls == 1:
                return False  # skip the upper clamp guard
            return other <= self.value

    original_isclose = tension.math.isclose
    monkeypatch.setattr(
        tension.math,
        "isclose",
        lambda a, b, *args, **kwargs: (
            False
            if isinstance(a, FakeWpi) or isinstance(b, FakeWpi)
            else original_isclose(a, b, *args, **kwargs)
        ),
        raising=False,
    )

    # Ensure non-spoofed values still delegate to the original ``isclose``.
    assert tension.math.isclose(12.0, 12.0)

    fake_wpi = FakeWpi(lower.midpoint_wpi)
    # Exercise the conversion helper.
    assert float(fake_wpi) == lower.midpoint_wpi

    estimated = tension.estimate_profile_for_wpi(fake_wpi)

    assert estimated.heavier_weight == lower.weight
    assert estimated.lighter_weight == upper.weight
    assert math.isclose(estimated.target_force_grams, lower.target_force_grams)
    assert math.isclose(estimated.feed_rate_mm_s, lower.feed_rate_mm_s)
    assert math.isclose(
        estimated.pull_variation_percent,
        lower.pull_variation_percent,
    )
    assert math.isclose(
        estimated.trial_duration_seconds,
        lower.trial_duration_seconds,
    )


def test_catalog_contains_expected_weights() -> None:
    expected = {
        "lace",
        "fingering",
        "sport",
        "dk",
        "worsted",
        "bulky",
        "super bulky",
    }
    assert expected == set(tension.TENSION_PROFILES)


def test_estimate_tension_handles_zero_span_intervals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lower = tension.TensionProfile(
        weight="custom-low",
        wraps_per_inch=(12, 12),
        target_force_grams=50.0,
        feed_rate_mm_s=30.0,
        pull_variation_percent=3.0,
        trial_duration_seconds=45.0,
    )
    upper = tension.TensionProfile(
        weight="custom-high",
        wraps_per_inch=(12, 12),
        target_force_grams=60.0,
        feed_rate_mm_s=30.0,
        pull_variation_percent=3.0,
        trial_duration_seconds=55.0,
    )

    monkeypatch.setattr(
        tension,
        "list_tension_profiles",
        lambda: [lower, upper],
    )

    class FakeWpi:
        """Mimic a wraps-per-inch value that forces the zero-span branch."""

        def __init__(self, value: float) -> None:
            self.value = value
            self._le_calls = 0
            self._ge_calls = 0

        def __le__(self, other: float) -> bool:  # type: ignore[override]
            self._le_calls += 1
            if self._le_calls == 1:
                return self.value <= other  # initial check against zero
            if self._le_calls == 2:
                return False  # skip the early clamp guard
            return self.value <= other

        def __ge__(self, other: float) -> bool:  # type: ignore[override]
            self._ge_calls += 1
            if self._ge_calls == 1:
                return False  # skip the upper clamp guard
            return other <= self.value

    assert (
        tension.estimate_tension_for_wpi(FakeWpi(lower.midpoint_wpi))
        == lower.target_force_grams
    )


def test_estimate_tension_returns_last_profile_when_comparison_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    heavy = tension.TensionProfile(
        weight="heavy",
        wraps_per_inch=(6, 6),
        target_force_grams=90.0,
        feed_rate_mm_s=28.0,
        pull_variation_percent=2.5,
        trial_duration_seconds=58.0,
    )
    light = tension.TensionProfile(
        weight="light",
        wraps_per_inch=(20, 20),
        target_force_grams=35.0,
        feed_rate_mm_s=40.0,
        pull_variation_percent=4.0,
        trial_duration_seconds=62.0,
    )

    monkeypatch.setattr(
        tension,
        "list_tension_profiles",
        lambda: [heavy, light],
    )

    result = tension.estimate_tension_for_wpi(float("nan"))

    assert result == light.target_force_grams


def test_estimate_profile_returns_last_profile_when_comparison_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    heavy = tension.TensionProfile(
        weight="heavy",
        wraps_per_inch=(6, 6),
        target_force_grams=90.0,
        feed_rate_mm_s=28.0,
        pull_variation_percent=2.5,
        trial_duration_seconds=58.0,
    )
    light = tension.TensionProfile(
        weight="light",
        wraps_per_inch=(20, 20),
        target_force_grams=35.0,
        feed_rate_mm_s=40.0,
        pull_variation_percent=4.0,
        trial_duration_seconds=62.0,
    )

    monkeypatch.setattr(
        tension,
        "list_tension_profiles",
        lambda: [heavy, light],
    )

    estimated = tension.estimate_profile_for_wpi(float("nan"))

    assert estimated.heavier_weight == light.weight
    assert estimated.lighter_weight == light.weight
    assert math.isclose(estimated.target_force_grams, light.target_force_grams)
    assert math.isclose(estimated.feed_rate_mm_s, light.feed_rate_mm_s)
    assert math.isclose(
        estimated.pull_variation_percent,
        light.pull_variation_percent,
    )
    assert math.isclose(
        estimated.trial_duration_seconds,
        light.trial_duration_seconds,
    )


def _sample_calibration() -> tension.HallSensorCalibration:
    return tension.HallSensorCalibration.from_pairs(
        [
            (100.0, 20.0),
            (160.0, 55.0),
            (220.0, 85.0),
        ]
    )


def test_calibration_requires_multiple_points() -> None:
    with pytest.raises(ValueError):
        tension.HallSensorCalibration.from_pairs([(100.0, 20.0)])


def test_calibration_rejects_invalid_points() -> None:
    with pytest.raises(ValueError):
        tension.CalibrationPoint(reading=float("nan"), grams=10.0)
    with pytest.raises(ValueError):
        tension.CalibrationPoint(reading=100.0, grams=-1.0)
    with pytest.raises(ValueError):
        tension.HallSensorCalibration.from_pairs(
            [
                (100.0, 20.0),
                (100.0, 25.0),
            ]
        )


def test_estimate_tension_from_sensor_interpolates() -> None:
    calibration = _sample_calibration()
    grams = tension.estimate_tension_for_sensor_reading(
        190.0,
        calibration,
    )
    assert math.isclose(grams, 70.0)


def test_estimate_tension_from_sensor_clamps_and_validates() -> None:
    calibration = _sample_calibration()
    assert math.isclose(
        tension.estimate_tension_for_sensor_reading(
            50.0,
            calibration,
        ),
        20.0,
    )
    with pytest.raises(ValueError):
        tension.estimate_tension_for_sensor_reading(
            50.0,
            calibration,
            clamp=False,
        )
    with pytest.raises(ValueError):
        tension.estimate_tension_for_sensor_reading(
            float("inf"),
            calibration,
        )


def test_match_tension_profile_for_sensor_reading() -> None:
    calibration = _sample_calibration()
    match = tension.match_tension_profile_for_sensor_reading(
        185.0,
        calibration,
    )
    measured = tension.estimate_tension_for_sensor_reading(
        185.0,
        calibration,
    )
    assert match.profile.weight == "worsted"
    assert math.isclose(
        match.difference_grams,
        abs(match.profile.target_force_grams - measured),
    )
