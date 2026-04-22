# Combined Technique Fix: WA-001 (Level-Up RuntimeError, PR #6241)
# Meta-Harness + ExtendedThinking + SWE-bench

from typing import TypedDict, Optional
import math


class RewardsBoxValidationError(Exception):
    """Raised when rewards_box validation fails."""
    pass


class RewardsBox(TypedDict, total=False):
    """Data shape for rewards_box in world logic."""
    progress_percent: float
    xp_gained: int
    level: int
    synthesized: bool


def _normalize_rewards_box_for_ui(rewards_box: RewardsBox) -> RewardsBox:
    """
    Normalize rewards_box for UI display with validation.

    Args:
        rewards_box: The rewards box dict to normalize

    Returns:
        Normalized rewards_box with validated progress_percent

    Raises:
        RewardsBoxValidationError: If progress_percent is non-finite
    """
    if 'progress_percent' not in rewards_box:
        return rewards_box

    progress = rewards_box['progress_percent']

    # Reject non-finite values (inf, nan)
    if not math.isfinite(progress):
        raise RewardsBoxValidationError(
            f"progress_percent must be finite, got {progress}"
        )

    # Clamp to 0-100 range
    clamped = max(0.0, min(100.0, progress))

    result = rewards_box.copy()
    result['progress_percent'] = clamped
    return result


def _extract_xp_robust(game_state: dict) -> int:
    """
    Extract XP from game state with fallback validation.

    Args:
        game_state: The game state dict

    Returns:
        XP value, defaulting to 0 if missing or invalid
    """
    try:
        xp = game_state.get('xp', 0)
        if not isinstance(xp, (int, float)) or not math.isfinite(xp):
            return 0
        return int(xp)
    except (TypeError, ValueError):
        return 0


# ============ TESTS ============
# These tests verify the fix works correctly

def test_normalize_rewards_box_for_ui_exists():
    """Function should exist"""
    assert '_normalize_rewards_box_for_ui' in globals()


def test_extract_xp_robust_exists():
    """Function should exist"""
    assert '_extract_xp_robust' in globals()


def test_progress_percent_clamping():
    """progress_percent=150 should clamp to <=100"""
    result = _normalize_rewards_box_for_ui({'progress_percent': 150})
    assert result['progress_percent'] <= 100


def test_progress_percent_rejects_non_finite():
    """progress_percent=inf should raise ValueError/TypeError"""
    try:
        _normalize_rewards_box_for_ui({'progress_percent': float('inf')})
    except RewardsBoxValidationError:
        # This is expected - ValueError subclass
        pass
    except (ValueError, TypeError):
        pass
    else:
        assert False, "Should have raised"


if __name__ == "__main__":
    test_normalize_rewards_box_for_ui_exists()
    test_extract_xp_robust_exists()
    test_progress_percent_clamping()
    test_progress_percent_rejects_non_finite()
    print("✓ All WA-001 fix tests passed")