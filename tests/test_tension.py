from __future__ import annotations

import math

import pytest

from wove import tension


def test_get_tension_profile_is_case_insensitive() -> None:
    profile = tension.get_tension_profile("Worsted")
    assert isinstance(profile, tension.TensionProfile)
    assert profile.weight == "worsted"


def test_get_tension_profile_unknown_weight() -> None:
    with pytest.raises(ValueError):
        tension.get_tension_profile("thread")


def test_list_tension_profiles_orders_light_to_heavy() -> None:
    ordered = list(tension.list_tension_profiles())
    midpoints = [profile.midpoint_wpi for profile in ordered]
    assert midpoints == sorted(midpoints, reverse=True)


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


def test_estimate_tension_handles_zero_span_intervals(monkeypatch: pytest.MonkeyPatch) -> None:
    lower = tension.TensionProfile(
        weight="custom-low",
        wraps_per_inch=(12, 12),
        target_force_grams=50.0,
        feed_rate_mm_s=30.0,
        pull_variation_percent=3.0,
    )
    upper = tension.TensionProfile(
        weight="custom-high",
        wraps_per_inch=(12, 12),
        target_force_grams=60.0,
        feed_rate_mm_s=30.0,
        pull_variation_percent=3.0,
    )

    monkeypatch.setattr(tension, "list_tension_profiles", lambda: [lower, upper])

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
    )
    light = tension.TensionProfile(
        weight="light",
        wraps_per_inch=(20, 20),
        target_force_grams=35.0,
        feed_rate_mm_s=40.0,
        pull_variation_percent=4.0,
    )

    monkeypatch.setattr(tension, "list_tension_profiles", lambda: [heavy, light])

    result = tension.estimate_tension_for_wpi(float("nan"))

    assert result == light.target_force_grams
