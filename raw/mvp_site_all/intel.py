"""Intel operations for WorldAI Faction Management.

Implements exact formulas for:
- Spy deployment and detection
- Intel success tiers
- Intel buffs and bonuses

All formulas are reverse-engineered from the WorldAI Faction Management ruleset.
"""

from __future__ import annotations

import random
from enum import Enum
from typing import TypedDict


class IntelTier(Enum):
    """Intel operation success tiers."""

    FAILURE = 0
    PARTIAL = 1
    SUCCESS = 2
    CRITICAL = 3


class IntelResult(TypedDict):
    """Result of an intel operation."""

    tier: str
    detected: bool
    intel_gathered: int
    message: str


# =============================================================================
# Detection Risk
# =============================================================================


def calculate_detection_risk(
    spies_deployed: int,
    target_shadow_networks: int,
    target_wards: int,
    spymaster_mod: int = 0,
    lineage_intrigue: int = 0,
) -> float:
    """Calculate detection risk for spy operations.

    Formula:
        Base Risk = 30%
        + (target_shadow_networks * 2%)  # Counter-intel
        + (target_wards * 5%)            # Magical detection
        - (spies_deployed * 1%)          # More spies = distraction
        - (spymaster_mod * 2%)           # Council bonus
        - (intrigue_level * 3%)          # Lineage bonus

    Risk is clamped between 5% and 90%.

    Args:
        spies_deployed: Number of spies on this operation
        target_shadow_networks: Target's shadow network count
        target_wards: Target's ward count
        spymaster_mod: Spymaster council member ability modifier
        lineage_intrigue: Intrigue lineage track level (0-5)

    Returns:
        Detection risk as decimal (0.0-1.0)
    """
    base_risk = 0.30

    # Target defenses increase risk
    network_penalty = target_shadow_networks * 0.02
    ward_penalty = target_wards * 0.05

    # Attacker bonuses reduce risk
    spy_bonus = min(spies_deployed * 0.01, 0.15)  # Cap at 15%
    spymaster_bonus = spymaster_mod * 0.02
    intrigue_bonus = lineage_intrigue * 0.03

    risk = (
        base_risk
        + network_penalty
        + ward_penalty
        - spy_bonus
        - spymaster_bonus
        - intrigue_bonus
    )

    # Clamp between 5% and 90%
    return max(0.05, min(0.90, risk))


def is_detected(detection_risk: float) -> bool:
    """Roll to determine if spies are detected.

    Args:
        detection_risk: Detection risk as decimal (0.0-1.0)

    Returns:
        True if detected
    """
    return random.random() < detection_risk


# =============================================================================
# Intel Success
# =============================================================================


def calculate_intel_success(
    spies_deployed: int,
    target_shadow_networks: int,
    spymaster_mod: int = 0,
    lineage_intrigue: int = 0,
    target_difficulty: str = "medium",
) -> IntelTier:
    """Calculate intel operation success tier.

    Success is based on spy strength vs target defenses.

    Formula:
        Spy Strength = spies * (1 + spymaster_mod * 0.1 + intrigue * 0.15)
        Defense = shadow_networks * difficulty_mult

    Difficulty multipliers:
        easy: 0.5
        medium: 1.0
        hard: 1.5
        legendary: 2.0

    Tiers:
        Strength < Defense * 0.5: FAILURE
        Strength < Defense: PARTIAL
        Strength < Defense * 1.5: SUCCESS
        Strength >= Defense * 1.5: CRITICAL

    Args:
        spies_deployed: Number of spies on operation
        target_shadow_networks: Target's counter-intel capability
        spymaster_mod: Spymaster ability modifier
        lineage_intrigue: Intrigue lineage level
        target_difficulty: Target faction difficulty (easy/medium/hard/legendary)

    Returns:
        Intel success tier
    """
    difficulty_mults = {
        "easy": 0.5,
        "medium": 1.0,
        "hard": 1.5,
        "legendary": 2.0,
    }
    diff_mult = difficulty_mults.get(target_difficulty.lower(), 1.0)

    # Calculate spy strength
    spy_strength = spies_deployed * (
        1.0 + spymaster_mod * 0.1 + lineage_intrigue * 0.15
    )

    # Calculate defense
    defense = max(1, target_shadow_networks) * diff_mult

    # Add some randomness
    roll = random.uniform(0.8, 1.2)
    effective_strength = spy_strength * roll

    # Determine tier
    if effective_strength < defense * 0.5:
        return IntelTier.FAILURE
    if effective_strength < defense:
        return IntelTier.PARTIAL
    if effective_strength < defense * 1.5:
        return IntelTier.SUCCESS
    return IntelTier.CRITICAL


def calculate_intel_success_deterministic(
    spies_deployed: int,
    target_shadow_networks: int,
    spymaster_mod: int = 0,
    lineage_intrigue: int = 0,
    target_difficulty: str = "medium",
    roll: float = 1.0,
) -> IntelTier:
    """Calculate intel success with deterministic roll for testing.

    Same as calculate_intel_success but with fixed roll value.

    Args:
        spies_deployed: Number of spies on operation
        target_shadow_networks: Target's counter-intel capability
        spymaster_mod: Spymaster ability modifier
        lineage_intrigue: Intrigue lineage level
        target_difficulty: Target faction difficulty
        roll: Fixed roll value (default 1.0 = average)

    Returns:
        Intel success tier
    """
    difficulty_mults = {
        "easy": 0.5,
        "medium": 1.0,
        "hard": 1.5,
        "legendary": 2.0,
    }
    diff_mult = difficulty_mults.get(target_difficulty.lower(), 1.0)

    spy_strength = spies_deployed * (
        1.0 + spymaster_mod * 0.1 + lineage_intrigue * 0.15
    )
    defense = max(1, target_shadow_networks) * diff_mult
    effective_strength = spy_strength * roll

    if effective_strength < defense * 0.5:
        return IntelTier.FAILURE
    if effective_strength < defense:
        return IntelTier.PARTIAL
    if effective_strength < defense * 1.5:
        return IntelTier.SUCCESS
    return IntelTier.CRITICAL


# =============================================================================
# Intel Buffs
# =============================================================================

INTEL_BUFFS = {
    IntelTier.FAILURE: {
        "combat_bonus": 0.0,
        "accuracy_bonus": 0.0,
        "vision_range": 0,
        "duration_turns": 0,
    },
    IntelTier.PARTIAL: {
        "combat_bonus": 0.05,
        "accuracy_bonus": 0.05,
        "vision_range": 1,
        "duration_turns": 3,
    },
    IntelTier.SUCCESS: {
        "combat_bonus": 0.10,
        "accuracy_bonus": 0.10,
        "vision_range": 2,
        "duration_turns": 5,
    },
    IntelTier.CRITICAL: {
        "combat_bonus": 0.20,
        "accuracy_bonus": 0.15,
        "vision_range": 3,
        "duration_turns": 8,
    },
}


def get_intel_buff(tier: IntelTier) -> dict:
    """Get combat and strategic buffs for intel tier.

    Buffs:
        FAILURE: No buffs
        PARTIAL: +5% combat, +5% accuracy, 1 vision, 3 turns
        SUCCESS: +10% combat, +10% accuracy, 2 vision, 5 turns
        CRITICAL: +20% combat, +15% accuracy, 3 vision, 8 turns

    Args:
        tier: Intel operation success tier

    Returns:
        Dict with combat_bonus, accuracy_bonus, vision_range, duration_turns
    """
    return INTEL_BUFFS.get(tier, INTEL_BUFFS[IntelTier.FAILURE])


# =============================================================================
# Full Intel Operation
# =============================================================================


def execute_intel_operation(
    spies_deployed: int,
    target_shadow_networks: int,
    target_wards: int,
    spymaster_mod: int = 0,
    lineage_intrigue: int = 0,
    target_difficulty: str = "medium",
) -> IntelResult:
    """Execute a full intel operation with detection roll and success tier.

    Args:
        spies_deployed: Number of spies assigned
        target_shadow_networks: Target's shadow network count
        target_wards: Target's ward count
        spymaster_mod: Spymaster ability modifier
        lineage_intrigue: Intrigue lineage level
        target_difficulty: Target faction difficulty

    Returns:
        IntelResult with tier, detected status, intel gathered, and message
    """
    # Calculate detection
    detection_risk = calculate_detection_risk(
        spies_deployed,
        target_shadow_networks,
        target_wards,
        spymaster_mod,
        lineage_intrigue,
    )
    detected = is_detected(detection_risk)

    # Calculate success (even if detected, may have gathered some intel)
    tier = calculate_intel_success(
        spies_deployed,
        target_shadow_networks,
        spymaster_mod,
        lineage_intrigue,
        target_difficulty,
    )

    # If detected, reduce tier by one level
    if detected and tier != IntelTier.FAILURE:
        tier_order = [
            IntelTier.FAILURE,
            IntelTier.PARTIAL,
            IntelTier.SUCCESS,
            IntelTier.CRITICAL,
        ]
        current_idx = tier_order.index(tier)
        tier = tier_order[max(0, current_idx - 1)]

    # Calculate intel points gathered
    intel_points = {
        IntelTier.FAILURE: 0,
        IntelTier.PARTIAL: 25,
        IntelTier.SUCCESS: 75,
        IntelTier.CRITICAL: 150,
    }

    buffs = get_intel_buff(tier)

    # Generate message
    messages = {
        IntelTier.FAILURE: "Operation failed. No useful intelligence gathered.",
        IntelTier.PARTIAL: f"Partial success. Gained basic intel (+{buffs['combat_bonus'] * 100:.0f}% combat for {buffs['duration_turns']} turns).",
        IntelTier.SUCCESS: f"Success! Detailed intelligence acquired (+{buffs['combat_bonus'] * 100:.0f}% combat for {buffs['duration_turns']} turns).",
        IntelTier.CRITICAL: f"Critical success! Complete intelligence dossier obtained (+{buffs['combat_bonus'] * 100:.0f}% combat for {buffs['duration_turns']} turns).",
    }

    if detected:
        messages[tier] = f"[DETECTED] {messages[tier]} Your spies were spotted."

    return IntelResult(
        tier=tier.name,
        detected=detected,
        intel_gathered=intel_points[tier],
        message=messages[tier],
    )


# =============================================================================
# Cooldown Management
# =============================================================================


def get_operation_cooldown(tier: IntelTier, detected: bool) -> int:
    """Get cooldown turns before next operation against same target.

    Cooldowns:
        FAILURE: 5 turns (+ 3 if detected)
        PARTIAL: 4 turns (+ 3 if detected)
        SUCCESS: 6 turns (+ 3 if detected)
        CRITICAL: 8 turns (+ 3 if detected)

    Higher tiers have longer cooldowns because the target is now alert.

    Args:
        tier: Result tier of operation
        detected: Whether spies were detected

    Returns:
        Number of turns before next operation allowed
    """
    base_cooldowns = {
        IntelTier.FAILURE: 5,
        IntelTier.PARTIAL: 4,
        IntelTier.SUCCESS: 6,
        IntelTier.CRITICAL: 8,
    }

    cooldown = base_cooldowns.get(tier, 5)
    if detected:
        cooldown += 3

    return cooldown
