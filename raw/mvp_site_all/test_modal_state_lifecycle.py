"""
State lifecycle tests for modal management.

Tests state transitions for all three modals:
- Character Creation
- Level-Up
- Campaign Upgrade

Verifies:
- Flag clearing on new modal availability
- Proper state transitions (activate → in_progress → complete/cancel)
- Stale flag removal (not just setting to False)
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mvp_site.tests.test_modal_base import ModalTestBase, ModalTestScenario
from mvp_site import world_logic


class TestLevelUpStateLifecycle(ModalTestBase):
    """Test level-up modal state transitions."""

    def test_new_level_up_clears_stale_level_up_in_progress_false(self):
        """
        BUG FIX TEST (9c9f93d4a): When new level-up becomes available,
        stale level_up_in_progress=False should be REMOVED (not just kept as False).
        """
        scenario = ModalTestScenario(
            name="new_level_up_clears_stale_in_progress",
            initial_state=self.create_base_state(
                character_level=1,
                character_xp=300,  # Enough for level 2
                custom_campaign_state={
                    "level_up_complete": True,
                    "level_up_in_progress": False,  # Stale from previous level-up
                }
            ),
            action=lambda state: world_logic._check_and_set_level_up_pending(state, {
                "player_character_data": {"level": 1, "xp": 0}  # Original state before XP gain
            }),
            expected_flags={
                "level_up_complete": False,
                "level_up_in_progress": None,  # Should be removed, not False
            },
            expected_rewards={"level_up_available": True},
            description="Stale level_up_in_progress=False blocks routing - must be removed"
        )
        self.run_scenario(scenario)

        # Additional check: verify stale flags are REMOVED not just set False
        result_state = scenario.action(scenario.initial_state)
        self.assert_stale_flags_cleared(result_state, "level_up")

    def test_new_level_up_clears_level_up_complete(self):
        """When new level-up available, level_up_complete flag should be cleared."""
        scenario = ModalTestScenario(
            name="new_level_up_clears_complete_flag",
            initial_state=self.create_base_state(
                character_level=2,
                character_xp=900,  # Enough for level 3
                custom_campaign_state={
                    "level_up_complete": True,  # From previous level-up
                }
            ),
            action=lambda state: world_logic._check_and_set_level_up_pending(state, {
                "player_character_data": {"level": 2, "xp": 300}  # Before gaining more XP
            }),
            expected_flags={
                "level_up_complete": False,
            },
            expected_rewards={"level_up_available": True}
        )
        self.run_scenario(scenario)

    def test_new_level_up_clears_level_up_cancelled(self):
        """When new level-up available, level_up_cancelled flag should be cleared."""
        scenario = ModalTestScenario(
            name="new_level_up_clears_cancelled_flag",
            initial_state=self.create_base_state(
                character_level=1,
                character_xp=300,
                custom_campaign_state={
                    "level_up_cancelled": True,  # User cancelled previous level-up
                }
            ),
            action=lambda state: world_logic._check_and_set_level_up_pending(state, {
                "player_character_data": {"level": 1, "xp": 0}
            }),
            expected_flags={
                "level_up_cancelled": False,
            },
            expected_rewards={"level_up_available": True}
        )
        self.run_scenario(scenario)

    def test_level_up_exit_sets_complete_flag(self):
        """Exiting level-up via finish choice should set level_up_complete=True."""
        scenario = ModalTestScenario(
            name="level_up_exit_sets_complete",
            initial_state=self.create_base_state(
                character_level=2,
                character_xp=300,
                custom_campaign_state={
                    "level_up_in_progress": True,
                }
            ),
            action="CHOICE:finish_level_up_return_to_game",
            expected_flags={
                "level_up_complete": True,
                "level_up_in_progress": False,
            }
        )
        self.run_scenario(scenario)

    def test_level_up_no_activation_when_insufficient_xp(self):
        """Level-up should NOT activate when XP is insufficient for next level."""
        initial_state = self.create_base_state(
            character_level=1,
            character_xp=100,  # Not enough for level 2 (needs 300)
            custom_campaign_state={}
        )

        result_state = world_logic._check_and_set_level_up_pending(initial_state, {
            "player_character_data": {"level": 1, "xp": 100}
        })

        # Should NOT set level_up_available
        rewards = result_state.get("rewards_pending", {})
        self.assertNotIn("level_up_available", rewards)


class TestCharacterCreationStateLifecycle(ModalTestBase):
    """Test character creation modal state transitions."""

    def test_character_creation_exit_clears_in_progress(self):
        """Exiting character creation should clear in_progress flag."""
        scenario = ModalTestScenario(
            name="char_creation_exit_clears_in_progress",
            initial_state=self.create_base_state(
                custom_campaign_state={
                    "character_creation_in_progress": True,
                    "character_creation_stage": "review",
                }
            ),
            action="CHOICE:finish_character_creation_start_game",
            expected_flags={
                "character_creation_in_progress": False,
                "character_creation_completed": True,
            }
        )
        self.run_scenario(scenario)

    def test_character_creation_cancel_sets_completed_flag(self):
        """Cancelling character creation should mark it as completed (exit logic)."""
        scenario = ModalTestScenario(
            name="char_creation_cancel",
            initial_state=self.create_base_state(
                custom_campaign_state={
                    "character_creation_in_progress": True,
                    "character_creation_stage": "concept",  # Need stage for modal lock to activate
                }
            ),
            action="CHOICE:cancel_creation",
            expected_flags={
                "character_creation_in_progress": False,
                "character_creation_completed": True,  # Cancel sets completed, not cancelled
            }
        )
        self.run_scenario(scenario)


class TestCampaignUpgradeStateLifecycle(ModalTestBase):
    """Test campaign upgrade modal state transitions."""

    def test_campaign_upgrade_activation(self):
        """Campaign upgrade modal should activate when upgrade available."""
        # TODO: Implement once campaign upgrade activation logic is identified
        # This test will verify proper flag setting when upgrade becomes available
        pass

    def test_campaign_upgrade_exit_clears_flags(self):
        """Exiting campaign upgrade should clear in_progress flag."""
        # TODO: Implement once campaign upgrade exit logic is identified
        # This will test similar pattern to character creation and level-up exits
        pass


class TestMultipleModalStateTransitions(ModalTestBase):
    """Test sequential modal activations and proper state cleanup."""

    def test_sequential_level_ups_clear_previous_flags(self):
        """Multiple level-ups in sequence should properly clear flags each time."""
        # Level 1 → Level 2
        state = self.create_base_state(character_level=1, character_xp=300)
        state = world_logic._check_and_set_level_up_pending(state, {
            "player_character_data": {"level": 1, "xp": 0}
        })
        self.assertEqual(state["rewards_pending"]["level_up_available"], True)

        # Complete level-up
        state["custom_campaign_state"]["level_up_complete"] = True
        state["custom_campaign_state"]["level_up_in_progress"] = False
        state["player_character_data"]["level"] = 2

        # Level 2 → Level 3
        state["player_character_data"]["xp"] = 900  # Enough for level 3
        state = world_logic._check_and_set_level_up_pending(state, {
            "player_character_data": {"level": 2, "xp": 300}
        })

        # Should clear stale flags from previous level-up
        self.assert_stale_flags_cleared(state, "level_up")
        self.assertEqual(state["custom_campaign_state"].get("level_up_complete"), False)

    def test_character_creation_then_level_up_isolation(self):
        """Completing character creation, then getting level-up should keep flags isolated."""
        # Complete character creation
        state = self.create_base_state(
            character_level=1,
            character_xp=0,
            custom_campaign_state={
                "character_creation_completed": True,
                "character_creation_in_progress": False,
            }
        )

        # Gain XP for level-up
        state["player_character_data"]["xp"] = 300
        state = world_logic._check_and_set_level_up_pending(state, {
            "player_character_data": {"level": 1, "xp": 0}
        })

        # Level-up should activate without character creation flags interfering
        self.assertEqual(state["rewards_pending"]["level_up_available"], True)
        self.assertEqual(state["custom_campaign_state"]["character_creation_completed"], True)


if __name__ == "__main__":
    import unittest
    unittest.main()
