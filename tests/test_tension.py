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
