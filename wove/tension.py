"""Lookup helpers for yarn tension profiles documented in design roadmaps."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple


@dataclass(frozen=True)
class TensionProfile:
    """Summarize test results for a yarn weight handled by the tensioner."""

    weight: str
    wraps_per_inch: Tuple[int, int]
    target_force_grams: float
    feed_rate_mm_s: float
    pull_variation_percent: float

    @property
    def midpoint_wpi(self) -> float:
        """Return the midpoint wraps-per-inch value for interpolation."""

        low, high = self.wraps_per_inch
        return (low + high) / 2.0


@dataclass(frozen=True)
class EstimatedTension:
    """Interpolated tension target for a wraps-per-inch value."""

    wraps_per_inch: float
    target_force_grams: float
    feed_rate_mm_s: float
    pull_variation_percent: float
    heavier_weight: str
    lighter_weight: str


def _profiles() -> Dict[str, TensionProfile]:
    """Return the static catalog of yarn tension profiles."""

    return {
        "lace": TensionProfile(
            weight="lace",
            wraps_per_inch=(28, 32),
            target_force_grams=20.0,
            feed_rate_mm_s=45.0,
            pull_variation_percent=6.0,
        ),
        "fingering": TensionProfile(
            weight="fingering",
            wraps_per_inch=(18, 22),
            target_force_grams=35.0,
            feed_rate_mm_s=40.0,
            pull_variation_percent=4.5,
        ),
        "sport": TensionProfile(
            weight="sport",
            wraps_per_inch=(15, 18),
            target_force_grams=45.0,
            feed_rate_mm_s=38.0,
            pull_variation_percent=4.0,
        ),
        "dk": TensionProfile(
            weight="dk",
            wraps_per_inch=(12, 15),
            target_force_grams=55.0,
            feed_rate_mm_s=35.0,
            pull_variation_percent=3.5,
        ),
        "worsted": TensionProfile(
            weight="worsted",
            wraps_per_inch=(9, 12),
            target_force_grams=65.0,
            feed_rate_mm_s=33.0,
            pull_variation_percent=3.0,
        ),
        "bulky": TensionProfile(
            weight="bulky",
            wraps_per_inch=(7, 9),
            target_force_grams=80.0,
            feed_rate_mm_s=30.0,
            pull_variation_percent=2.5,
        ),
        "super bulky": TensionProfile(
            weight="super bulky",
            wraps_per_inch=(5, 7),
            target_force_grams=95.0,
            feed_rate_mm_s=28.0,
            pull_variation_percent=2.0,
        ),
    }


TENSION_PROFILES: Dict[str, TensionProfile] = _profiles()


def _normalize_weight(weight: str) -> str:
    normalized = weight.strip().lower()
    return normalized


def list_tension_profiles() -> Iterable[TensionProfile]:
    """Return known tension profiles ordered from lightest to heaviest."""

    return [
        TENSION_PROFILES[key]
        for key in sorted(
            TENSION_PROFILES,
            key=lambda name: TENSION_PROFILES[name].midpoint_wpi,
            reverse=True,
        )
    ]


def get_tension_profile(weight: str) -> TensionProfile:
    """Return the profile associated with ``weight`` (case-insensitive)."""

    normalized = _normalize_weight(weight)
    try:
        return TENSION_PROFILES[normalized]
    except KeyError as error:
        message = f"Unknown yarn weight '{weight}'"
        raise ValueError(message) from error


def estimate_tension_for_wpi(wraps_per_inch: float) -> float:
    """Estimate the target tension (grams) for a wraps-per-inch value."""

    if wraps_per_inch <= 0:
        raise ValueError("wraps_per_inch must be positive")

    ordered = sorted(
        list_tension_profiles(),
        key=lambda profile: profile.midpoint_wpi,
    )
    if wraps_per_inch <= ordered[0].midpoint_wpi:
        return ordered[0].target_force_grams
    if wraps_per_inch >= ordered[-1].midpoint_wpi:
        return ordered[-1].target_force_grams

    for lower, upper in zip(ordered, ordered[1:]):
        if lower.midpoint_wpi <= wraps_per_inch <= upper.midpoint_wpi:
            span = upper.midpoint_wpi - lower.midpoint_wpi
            if span == 0:
                return lower.target_force_grams
            ratio = (wraps_per_inch - lower.midpoint_wpi) / span
            adjustment = upper.target_force_grams - lower.target_force_grams
            return lower.target_force_grams + ratio * adjustment

    return ordered[-1].target_force_grams


def _interpolate(
    lower: float,
    upper: float,
    ratio: float,
) -> float:
    return lower + ratio * (upper - lower)


def estimate_profile_for_wpi(wraps_per_inch: float) -> EstimatedTension:
    """Interpolate a tension profile for ``wraps_per_inch``.

    The design roadmap highlights target pull force, feed rate, and
    pull-variation data for each cataloged yarn weight. This helper extends the
    existing interpolation to estimate all recorded values, returning the
    bounding weights so calibration scripts can report their source range.
    """

    if wraps_per_inch <= 0:
        raise ValueError("wraps_per_inch must be positive")

    ordered = sorted(
        list_tension_profiles(),
        key=lambda profile: profile.midpoint_wpi,
    )
    for profile in ordered:
        if math.isclose(wraps_per_inch, profile.midpoint_wpi):
            return EstimatedTension(
                wraps_per_inch=wraps_per_inch,
                target_force_grams=profile.target_force_grams,
                feed_rate_mm_s=profile.feed_rate_mm_s,
                pull_variation_percent=profile.pull_variation_percent,
                heavier_weight=profile.weight,
                lighter_weight=profile.weight,
            )
    first = ordered[0]
    last = ordered[-1]
    if wraps_per_inch <= first.midpoint_wpi:
        return EstimatedTension(
            wraps_per_inch=wraps_per_inch,
            target_force_grams=first.target_force_grams,
            feed_rate_mm_s=first.feed_rate_mm_s,
            pull_variation_percent=first.pull_variation_percent,
            heavier_weight=first.weight,
            lighter_weight=first.weight,
        )
    if wraps_per_inch >= last.midpoint_wpi:
        return EstimatedTension(
            wraps_per_inch=wraps_per_inch,
            target_force_grams=last.target_force_grams,
            feed_rate_mm_s=last.feed_rate_mm_s,
            pull_variation_percent=last.pull_variation_percent,
            heavier_weight=last.weight,
            lighter_weight=last.weight,
        )

    for lower_profile, upper_profile in zip(ordered, ordered[1:]):
        lower_mid = lower_profile.midpoint_wpi
        upper_mid = upper_profile.midpoint_wpi
        if lower_mid <= wraps_per_inch <= upper_mid:
            span = upper_mid - lower_mid
            if span == 0:
                variation = lower_profile.pull_variation_percent
                return EstimatedTension(
                    wraps_per_inch=wraps_per_inch,
                    target_force_grams=lower_profile.target_force_grams,
                    feed_rate_mm_s=lower_profile.feed_rate_mm_s,
                    pull_variation_percent=variation,
                    heavier_weight=lower_profile.weight,
                    lighter_weight=upper_profile.weight,
                )
            ratio = (wraps_per_inch - lower_mid) / span
            return EstimatedTension(
                wraps_per_inch=wraps_per_inch,
                target_force_grams=_interpolate(
                    lower_profile.target_force_grams,
                    upper_profile.target_force_grams,
                    ratio,
                ),
                feed_rate_mm_s=_interpolate(
                    lower_profile.feed_rate_mm_s,
                    upper_profile.feed_rate_mm_s,
                    ratio,
                ),
                pull_variation_percent=_interpolate(
                    lower_profile.pull_variation_percent,
                    upper_profile.pull_variation_percent,
                    ratio,
                ),
                heavier_weight=lower_profile.weight,
                lighter_weight=upper_profile.weight,
            )
    return EstimatedTension(
        wraps_per_inch=wraps_per_inch,
        target_force_grams=last.target_force_grams,
        feed_rate_mm_s=last.feed_rate_mm_s,
        pull_variation_percent=last.pull_variation_percent,
        heavier_weight=last.weight,
        lighter_weight=last.weight,
    )


def find_tension_profile_for_wpi(
    wraps_per_inch: float,
) -> TensionProfile | None:
    """Return the recorded profile that spans ``wraps_per_inch``.

    The v1c mechanical roadmap catalogs each yarn weight with an inclusive
    wraps-per-inch range.  Builders measuring an unknown yarn can use this
    helper to map that measurement back to the closest documented profile
    before falling back to interpolation.

    Args:
        wraps_per_inch: Measured wraps per inch. Must be positive.

    Returns:
        The matching :class:`TensionProfile` when the measurement falls inside
        a documented range; ``None`` when it lies outside all cataloged ranges.

    Raises:
        ValueError: If ``wraps_per_inch`` is not positive or is NaN.
    """

    if math.isnan(wraps_per_inch) or wraps_per_inch <= 0:
        raise ValueError("wraps_per_inch must be a positive number")
    for profile in list_tension_profiles():
        lower, upper = profile.wraps_per_inch
        if lower <= wraps_per_inch <= upper:
            return profile
    return None


__all__ = [
    "TensionProfile",
    "EstimatedTension",
    "TENSION_PROFILES",
    "estimate_tension_for_wpi",
    "estimate_profile_for_wpi",
    "find_tension_profile_for_wpi",
    "get_tension_profile",
    "list_tension_profiles",
]
