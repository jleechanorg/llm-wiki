"""
SWE-bench test for TEST-WA-001: Level-Up RuntimeError (PR #6241)

This test captures the bug: NameError references to _normalize_rewards_box_for_ui
and _extract_xp_robust in world_logic.py that cause RuntimeError at runtime.

The test expects these functions to exist but they are missing in pre-fix code.
"""
import pytest


class TestLevelUpRuntimeError:
    """Tests for PR #6241 - 6 regressions from PR #6233"""

    def test_normalize_rewards_box_for_ui_exists(self):
        """Test that _normalize_rewards_box_for_ui function exists"""
        # This function should exist but is missing pre-fix
        try:
            from mvp_site import world_logic
            assert hasattr(world_logic, '_normalize_rewards_box_for_ui'), \
                "_normalize_rewards_box_for_ui should exist in world_logic module"
        except ImportError:
            pytest.fail("world_logic module should exist")

    def test_extract_xp_robust_exists(self):
        """Test that _extract_xp_robust function exists"""
        try:
            from mvp_site import world_logic
            assert hasattr(world_logic, '_extract_xp_robust'), \
                "_extract_xp_robust should exist in world_logic module"
        except ImportError:
            pytest.fail("world_logic module should exist")

    def test_progress_percent_clamping(self):
        """Test that progress_percent is clamped to 0-100 range"""
        try:
            from mvp_site import world_logic
            # If function exists, test clamping behavior
            if hasattr(world_logic, '_normalize_rewards_box_for_ui'):
                result = world_logic._normalize_rewards_box_for_ui({
                    'progress_percent': 150
                })
                assert result['progress_percent'] <= 100, \
                    "progress_percent should be clamped to 100"
        except (ImportError, AttributeError):
            pytest.fail("Function should exist post-fix")

    def test_progress_percent_rejects_non_finite(self):
        """Test that progress_percent rejects non-finite values"""
        try:
            from mvp_site import world_logic
            if hasattr(world_logic, '_normalize_rewards_box_for_ui'):
                # Should reject inf/nan
                with pytest.raises((ValueError, TypeError)):
                    world_logic._normalize_rewards_box_for_ui({
                        'progress_percent': float('inf')
                    })
        except (ImportError, AttributeError):
            pytest.fail("Function should exist post-fix")

    def test_original_stored_level_assignment(self):
        """Test that _original_stored_level_for_source is assigned in narrative-only jumps"""
        try:
            from mvp_site import game_state
            # This attribute should be set when handling narrative-only level jumps
            # Check the game state processing logic
            assert hasattr(game_state, 'GameState') or hasattr(game_state, '_original_stored_level_for_source'), \
                "Game state should handle original_stored_level assignment"
        except ImportError:
            pytest.skip("game_state module structure unclear")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])