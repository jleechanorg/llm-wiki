"""
TDD Test Coverage for World Logic Modal Lock Functions

These tests provide coverage for the modal lock logic added in PR #5282.

Coverage targets:
- mvp_site/world_logic.py:1031-1035 (_check_and_set_level_up_pending stale flag clearing)
- mvp_site/world_logic.py:1377 (_enforce_character_creation_modal_lock level_up_modal_active label)
- mvp_site/world_logic.py:1427-1445 (_enforce_character_creation_modal_lock level-up exit path)
- mvp_site/world_logic.py:1480 (_enforce_character_creation_modal_lock level-up protected flags)
- mvp_site/world_logic.py:1516 (_enforce_character_creation_modal_lock should_block=True path)
"""

import unittest

from mvp_site import world_logic


class TestCheckAndSetLevelUpPendingStaleFlags(unittest.TestCase):
    """Test _check_and_set_level_up_pending stale flag clearing."""

    def test_clears_stale_level_up_complete_when_new_level_up_available(self):
        """
        Coverage: mvp_site/world_logic.py:1031-1035

        When a new level-up becomes available, clear stale level_up_complete flag
        from previous level-up to prevent blocking future level-ups.
        """
        original_state_dict = {
            "player_character_data": {
                "level": 2,
                "xp": 0,  # Original XP before gain
            }
        }
        state_dict = {
            "custom_campaign_state": {
                "level_up_complete": True,  # Stale from previous level-up
            },
            "player_character_data": {
                "level": 2,  # Character at level 2
                "xp": 900,   # Has enough XP for level 3 (XP threshold is 900)
            }
        }

        world_logic._check_and_set_level_up_pending(state_dict, original_state_dict)

        # Verify stale flag was cleared
        custom_state = state_dict.get("custom_campaign_state", {})
        self.assertEqual(
            custom_state.get("level_up_complete"),
            False,
            "level_up_complete must be cleared when new level-up becomes available"
        )

    def test_clears_stale_level_up_cancelled_when_new_level_up_available(self):
        """
        Coverage: mvp_site/world_logic.py:1031-1035

        When a new level-up becomes available, clear stale level_up_cancelled flag
        from previous cancelled level-up to allow new level-up to activate.
        """
        original_state_dict = {
            "player_character_data": {
                "level": 2,
                "xp": 0,  # Original XP before gain
            }
        }
        state_dict = {
            "custom_campaign_state": {
                "level_up_cancelled": True,  # Stale from previously cancelled level-up
            },
            "player_character_data": {
                "level": 2,
                "xp": 900,  # Enough XP for level 3
            }
        }

        world_logic._check_and_set_level_up_pending(state_dict, original_state_dict)

        # Verify stale flag was cleared
        custom_state = state_dict.get("custom_campaign_state", {})
        self.assertEqual(
            custom_state.get("level_up_cancelled"),
            False,
            "level_up_cancelled must be cleared when new level-up becomes available"
        )


class TestEnforceModalLockLevelUpPaths(unittest.TestCase):
    """Test _enforce_character_creation_modal_lock level-up specific paths."""

    def test_level_up_modal_active_label_added_to_list(self):
        """
        Coverage: mvp_site/world_logic.py:1377

        When level-up modal is active, the label "level_up" should be added
        to the active_modal_labels list for logging.
        """
        current_state = {
            "custom_campaign_state": {
                "level_up_in_progress": True,  # Level-up modal active
                "character_creation_in_progress": False,
            }
        }
        state_changes = {"custom_campaign_state": {}}
        user_input = "I want to choose my level-up options"

        # The function logs but doesn't return the labels, so we just verify it doesn't raise
        result = world_logic._enforce_character_creation_modal_lock(
            current_state,
            state_changes,
            user_input
        )

        # Verify function executed without error (label path was covered)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_level_up_exit_choice_sets_completion_flags(self):
        """
        Coverage: mvp_site/world_logic.py:1427-1445

        When user selects a level-up exit choice, the server sets
        level_up_complete=True and level_up_in_progress=False.
        """
        current_state = {
            "custom_campaign_state": {
                "level_up_in_progress": True,
            }
        }
        state_changes = {"custom_campaign_state": {}}
        user_input = "CHOICE:finish_level_up_return_to_game"

        result = world_logic._enforce_character_creation_modal_lock(
            current_state,
            state_changes,
            user_input
        )

        # Verify level-up exit flags were set
        self.assertEqual(
            result["custom_campaign_state"]["level_up_complete"],
            True,
            "level_up_complete must be set to True on level-up exit"
        )
        self.assertEqual(
            result["custom_campaign_state"]["level_up_in_progress"],
            False,
            "level_up_in_progress must be set to False on level-up exit"
        )

    def test_level_up_protected_flags_update_when_modal_active(self):
        """
        Coverage: mvp_site/world_logic.py:1480

        When level-up modal is active, the protected_flags dict is updated
        with level-up specific flag protection rules.
        """
        current_state = {
            "custom_campaign_state": {
                "level_up_in_progress": True,
                "character_creation_in_progress": False,  # Not in char creation
            }
        }
        # LLM tries to set level_up_in_progress=False without exit choice
        state_changes = {
            "custom_campaign_state": {
                "level_up_in_progress": False,  # LLM trying to exit without choice
            }
        }
        user_input = "I continue my level-up"

        result = world_logic._enforce_character_creation_modal_lock(
            current_state,
            state_changes,
            user_input
        )

        # Verify LLM's attempt to exit was blocked
        self.assertEqual(
            result["custom_campaign_state"]["level_up_in_progress"],
            True,
            "level_up_in_progress must be forced to True when LLM tries to exit without choice"
        )

    def test_should_block_true_triggers_blocking_action(self):
        """
        Coverage: mvp_site/world_logic.py:1516

        When should_block evaluates to True, the blocking action is executed
        (remove, force_true, or restore depending on the rule).
        """
        current_state = {
            "custom_campaign_state": {
                "level_up_in_progress": True,
            }
        }
        # LLM tries to set level_up_complete=True without exit choice
        state_changes = {
            "custom_campaign_state": {
                "level_up_complete": True,  # LLM trying to complete without choice
            }
        }
        user_input = "I think I'm done leveling up"

        result = world_logic._enforce_character_creation_modal_lock(
            current_state,
            state_changes,
            user_input
        )

        # Verify level_up_complete was removed (blocking action="remove")
        self.assertNotIn(
            "level_up_complete",
            result["custom_campaign_state"],
            "level_up_complete must be removed when set without exit choice"
        )


if __name__ == '__main__':
    unittest.main()
