"""Lookup helpers for yarn tension profiles documented in design roadmaps."""

from __future__ import annotations

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


__all__ = [
    "TensionProfile",
    "TENSION_PROFILES",
    "estimate_tension_for_wpi",
    "get_tension_profile",
    "list_tension_profiles",
]
