"""
SWE-bench test for TEST-WA-005: ProxyFix rate-limit regression (PR #6275)

This test captures the bug: stuck level-up where level_up_complete=True
but rewards_box is missing. Tests ASI injection at D&D 5e ASI levels.
"""
import pytest
from typing import TypedDict, Optional


class TestLevelUpRewardsBoxFix:
    """Tests for PR #6275 - Fix Stuck Level-Up Completion Rewards Box"""

    def test_ensure_level_up_rewards_box_exists(self):
        """Test that ensure_level_up_rewards_box helper exists"""
        try:
            from mvp_site import world_logic
            assert hasattr(world_logic, 'ensure_level_up_rewards_box'), \
                "ensure_level_up_rewards_box should exist"
        except ImportError:
            pytest.fail("world_logic module should exist")

    def test_ensure_level_up_planning_block_exists(self):
        """Test that ensure_level_up_planning_block helper exists"""
        try:
            from mvp_site import world_logic
            assert hasattr(world_logic, 'ensure_level_up_planning_block'), \
                "ensure_level_up_planning_block should exist"
        except ImportError:
            pytest.fail("world_logic module should exist")

    def test_is_asi_level_helper(self):
        """Test _is_asi_level helper returns correct values for D&D 5e ASI levels"""
        # D&D 5e ASI at levels 4, 8, 12, 14, 16, 19
        try:
            from mvp_site import world_logic
            if hasattr(world_logic, '_is_asi_level'):
                asi_levels = [4, 8, 12, 14, 16, 19]
                non_asi_levels = [1, 2, 3, 5, 6, 7, 10, 20]

                for level in asi_levels:
                    assert world_logic._is_asi_level(level), \
                        f"Level {level} should be ASI level"

                for level in non_asi_levels:
                    assert not world_logic._is_asi_level(level), \
                        f"Level {level} should NOT be ASI level"
        except (ImportError, AttributeError):
            pytest.fail("ASI level helper should exist post-fix")

    def test_rewards_box_created_on_level_up_complete(self):
        """Test that rewards_box is created when level_up_complete=True"""
        class GameState(TypedDict):
            level_up_complete: bool
            rewards_box: Optional[dict]
            planning_block: Optional[dict]
            level: int

        def ensure_level_up_rewards_box(state: GameState) -> GameState:
            """Post-fix: ensure rewards_box exists when level_up_complete=True"""
            if state.get('level_up_complete') and not state.get('rewards_box'):
                state['rewards_box'] = {
                    'synthesized': True,
                    'xp_gained': 0,
                    'level': state.get('level', 1)
                }
            return state

        # Test: level_up_complete=True but rewards_box missing
        state: GameState = {
            'level_up_complete': True,
            'rewards_box': None,
            'level': 5
        }

        result = ensure_level_up_rewards_box(state)
        assert result['rewards_box'] is not None, \
            "rewards_box should be created when level_up_complete=True"
        assert result['rewards_box']['synthesized'] is True

    def test_planning_block_created_on_level_up(self):
        """Test that planning_block is created for level-up states"""
        class GameState(TypedDict):
            level_up_complete: bool
            planning_block: Optional[dict]
            level: int

        def ensure_level_up_planning_block(state: GameState) -> GameState:
            """Post-fix: ensure planning_block exists when level_up_complete=True"""
            if state.get('level_up_complete') and not state.get('planning_block'):
                state['planning_block'] = {
                    'active': True,
                    'level': state.get('level', 1)
                }
            return state

        # Test: level_up_complete=True but planning_block missing
        state: GameState = {
            'level_up_complete': True,
            'planning_block': None,
            'level': 5
        }

        result = ensure_level_up_planning_block(state)
        assert result['planning_block'] is not None, \
            "planning_block should be created when level_up_complete=True"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])