# Combined Technique Fix: WA-005 (ProxyFix rate-limit regression, PR #6275)
# Meta-Harness + ExtendedThinking + SWE-bench

from typing import TypedDict, Optional


class LevelUpStateError(Exception):
    """Raised when level-up state is invalid."""
    pass


class RewardsBox(TypedDict, total=False):
    """Data shape for rewards_box."""
    synthesized: bool
    xp_gained: int
    level: int
    active: bool


class PlanningBlock(TypedDict, total=False):
    """Data shape for planning_block."""
    active: bool
    level: int
    suggestions: list


class GameState(TypedDict, total=False):
    """Data shape for game state."""
    level_up_complete: bool
    rewards_box: Optional[RewardsBox]
    planning_block: Optional[PlanningBlock]
    level: int


# D&D 5e ASI levels: 4, 8, 12, 14, 16, 19
ASI_LEVELS = frozenset([4, 8, 12, 14, 16, 19])


def _is_asi_level(level: int) -> bool:
    """
    Check if level is a D&D 5e Ability Score Improvement level.

    Args:
        level: Character level to check

    Returns:
        True if level is an ASI level (4, 8, 12, 14, 16, 19)
    """
    return level in ASI_LEVELS


def ensure_level_up_rewards_box(state: GameState) -> GameState:
    """
    Ensure rewards_box exists when level_up_complete=True.

    Args:
        state: Game state dict

    Returns:
        Updated state with rewards_box if needed
    """
    if state.get('level_up_complete') and not state.get('rewards_box'):
        state['rewards_box'] = {
            'synthesized': True,
            'xp_gained': 0,
            'level': state.get('level', 1)
        }
    return state


def ensure_level_up_planning_block(state: GameState) -> GameState:
    """
    Ensure planning_block exists when level_up_complete=True,
    including ASI suggestions at ASI levels.

    Args:
        state: Game state dict

    Returns:
        Updated state with planning_block if needed
    """
    if state.get('level_up_complete') and not state.get('planning_block'):
        level = state.get('level', 1)
        suggestions = []

        # Inject ASI suggestions at D&D 5e ASI levels
        if _is_asi_level(level):
            suggestions = [
                "Consider increasing your primary ability score",
                "Consider increasing a secondary ability score",
                "Consider taking a feat instead of an ability score increase"
            ]

        state['planning_block'] = {
            'active': True,
            'level': level,
            'suggestions': suggestions
        }
    return state


# ============ TESTS ============

def test_ensure_level_up_rewards_box_exists():
    """Test ensure_level_up_rewards_box function exists"""
    assert 'ensure_level_up_rewards_box' in globals()


def test_ensure_level_up_planning_block_exists():
    """Test ensure_level_up_planning_block function exists"""
    assert 'ensure_level_up_planning_block' in globals()


def test_is_asi_level_helper():
    """Test _is_asi_level helper returns correct values for D&D 5e ASI levels"""
    asi_levels = [4, 8, 12, 14, 16, 19]
    non_asi_levels = [1, 2, 3, 5, 6, 7, 10, 20]

    for level in asi_levels:
        assert _is_asi_level(level), f"Level {level} should be ASI level"

    for level in non_asi_levels:
        assert not _is_asi_level(level), f"Level {level} should NOT be ASI level"


def test_rewards_box_created_on_level_up_complete():
    """Test that rewards_box is created when level_up_complete=True"""
    state: GameState = {
        'level_up_complete': True,
        'rewards_box': None,
        'level': 5
    }

    result = ensure_level_up_rewards_box(state)
    assert result['rewards_box'] is not None, "rewards_box should be created"
    assert result['rewards_box']['synthesized'] is True


def test_planning_block_created_on_level_up():
    """Test that planning_block is created when level_up_complete=True"""
    state: GameState = {
        'level_up_complete': True,
        'planning_block': None,
        'level': 5
    }

    result = ensure_level_up_planning_block(state)
    assert result['planning_block'] is not None, "planning_block should be created"


def test_asi_suggestions_injected():
    """Test that ASI suggestions are injected at ASI levels"""
    state: GameState = {
        'level_up_complete': True,
        'planning_block': None,
        'level': 8  # ASI level
    }

    result = ensure_level_up_planning_block(state)
    assert result['planning_block']['suggestions'], \
        "ASI suggestions should be present at level 8"


if __name__ == "__main__":
    test_ensure_level_up_rewards_box_exists()
    test_ensure_level_up_planning_block_exists()
    test_is_asi_level_helper()
    test_rewards_box_created_on_level_up_complete()
    test_planning_block_created_on_level_up()
    test_asi_suggestions_injected()
    print("✓ All WA-005 fix tests passed")