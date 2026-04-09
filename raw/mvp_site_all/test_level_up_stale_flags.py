"""
Test level-up stale flag issues:
1. level_up_in_progress not cleared when new level-up becomes available
2. character_creation_in_progress not cleared when exiting level-up modal
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from unittest.mock import Mock, patch
from mvp_site import agents, constants, world_logic
from mvp_site.firestore_service import DELETE_TOKEN


class TestLevelUpStaleFlags:
    """Test stale flag clearing on level-up availability and exit."""

    def test_level_up_in_progress_cleared_when_new_level_up_available(self):
        """
        RED TEST: level_up_in_progress should be cleared when new level-up becomes available.

        Bug: mvp_site/world_logic.py:1025 clears level_up_complete/level_up_cancelled
        but NOT level_up_in_progress, causing stale flag to block future level-ups.
        """
        # Setup: Original state at level 1, current state with enough XP for level 2
        original_state_dict = {
            "player_character_data": {
                "name": "TestChar",
                "level": 1,
                "class": "Fighter",
                "xp": 0,
            },
            "custom_campaign_state": {
                "level_up_complete": True,
                "level_up_cancelled": False,
                "level_up_in_progress": False,  # Stale flag from previous level-up
            },
        }

        state_dict = {
            "player_character_data": {
                "name": "TestChar",
                "level": 1,
                "class": "Fighter",
                "xp": 300,  # Enough for level 2 (XP needed: 300)
            },
            "custom_campaign_state": {
                "level_up_complete": True,
                "level_up_cancelled": False,
                "level_up_in_progress": False,  # Stale flag from previous level-up
            },
            "rewards_pending": {}
        }

        # Act: check for level-up
        world_logic._check_and_set_level_up_pending(state_dict, original_state_dict)

        # Assert: level_up_in_progress should be cleared (or not exist)
        custom_state = state_dict.get("custom_campaign_state", {})
        level_up_in_progress = custom_state.get("level_up_in_progress")

        # Should be None (cleared), NOT False (stale)
        assert level_up_in_progress is None, (
            f"level_up_in_progress={level_up_in_progress} should be cleared "
            f"when new level-up becomes available, not left as False to block routing"
        )

    def test_rewards_pending_cleared_on_level_up_exit(self):
        """
        GREEN TEST: rewards_pending should be removed when level-up modal is exited
        if it existed in the current state. This clears the stale signal completely
        rather than just flipping level_up_available, which would leave other keys
        in rewards_pending that _has_rewards_context() treats as active.

        Bug: level-up modal exit set rewards_pending = {level_up_available: False}
        but did not remove rewards_pending when it already existed, causing
        _has_rewards_context() to still treat it as active and retrigger rewards UI.
        """
        # Setup: level-up modal with stale rewards_pending (the real stale case)
        current_game_state_dict = {
            "character": {
                "name": "TestChar",
                "level": 2,
                "class": "Fighter",
            },
            "custom_campaign_state": {
                "level_up_in_progress": True,
            },
            "rewards_pending": {
                "level_up_available": True,  # Stale signal from before level-up completed
                "new_level": 3,
            },
        }
        state_changes = {}  # Empty state changes from LLM
        user_input = "CHOICE:finish_level_up_return_to_game"

        # Act: enforce modal exit
        result_changes = world_logic._enforce_character_creation_modal_lock(
            current_game_state_dict, state_changes, user_input
        )

        # Assert: rewards_pending should be DELETE_TOKEN (removed from state entirely)
        # not a partial dict that leaves stale keys behind
        assert result_changes.get("rewards_pending") == DELETE_TOKEN, (
            "rewards_pending should be DELETE_TOKEN on level-up exit when it "
            "existed in current state, fully removing the stale signal rather "
            "than just flipping level_up_available."
        )

    def test_character_creation_flags_cleared_on_level_up_exit(self):
        """
        RED TEST: character_creation_in_progress should be cleared when exiting level-up modal.

        Bug: mvp_site/world_logic.py:1427 sets level_up_complete/level_up_in_progress
        but does NOT clear character_creation_in_progress, causing character-creation
        lock check (agents.py:2806) to recapture and route to CharacterCreationAgent.
        """
        # Setup: user in level-up modal with stale character-creation flags
        current_game_state_dict = {
            "character": {
                "name": "TestChar",
                "level": 2,
                "class": "Fighter",
            },
            "custom_campaign_state": {
                "character_creation_in_progress": True,  # Stale from previous char creation
                "character_creation_completed": False,
                "level_up_in_progress": True,  # Currently in level-up modal
            },
        }

        state_changes = {}  # Empty state changes from LLM
        user_input = "CHOICE:finish_level_up_return_to_game"

        # Act: enforce modal exit
        result_changes = world_logic._enforce_character_creation_modal_lock(
            current_game_state_dict, state_changes, user_input
        )

        # Assert: character_creation_in_progress should be cleared
        custom_state = result_changes.get("custom_campaign_state", {})
        assert custom_state.get("character_creation_in_progress") is False, (
            "character_creation_in_progress should be cleared when exiting level-up modal "
            "to prevent character-creation lock check from recapturing"
        )

    def test_routing_after_level_up_exit_with_cleared_flags(self):
        """
        GREEN TEST: After level-up exit with cleared flags, routing should NOT go to CharacterCreationAgent.

        This verifies that when character_creation_in_progress is properly cleared
        on level-up exit, the character-creation lock check (agents.py:2806) does not recapture.
        """
        # Setup: game state after level-up exit with CLEARED character-creation flags
        game_state = Mock()
        game_state.get_character.return_value = {
            "name": "TestChar",
            "level": 2,
            "class": "Fighter",
        }
        # Simulate state AFTER our fix is applied
        game_state.campaign = {
            "custom_campaign_state": {
                "level_up_complete": True,  # Just exited level-up
                "level_up_in_progress": False,
                "character_creation_in_progress": False,  # FIXED: Cleared on level-up exit
                "character_creation_completed": True,  # FIXED: Set on level-up exit
            },
            "campaign_version": 2,  # Avoid CampaignUpgradeAgent
        }

        # Act: route to appropriate agent
        agent, metadata = agents.get_agent_for_input("continue", game_state)

        # Assert: Should NOT route to CharacterCreationAgent
        assert metadata["intent"] != constants.MODE_CHARACTER_CREATION, (
            f"Should not route to CharacterCreationAgent after level-up exit with cleared flags. "
            f"Got intent={metadata['intent']}"
        )


class TestRewardBoxLevelUpInjection:
    """
    Test that level-up choices are injected when rewards_box.level_up_available=true
    but game_state.rewards_pending is null (LLM explicitly cleared it via state_updates).

    Root cause: LLM returns rewards_box.level_up_available=true (shows indicator) but also
    sets state_updates.rewards_pending=null. _inject_levelup_choices_if_needed only checked
    rewards_pending, so it skipped injection → planning block had no level-up choices.
    """

    def test_inject_levelup_choices_when_rewards_box_available_but_rewards_pending_null(self):
        """
        RED: rewards_box.level_up_available=true + rewards_pending=null → inject choices.

        Scenario: LLM awarded deferred XP that pushed player over level threshold.
        rewards_box.level_up_available=true (indicator shows) but rewards_pending=null
        (LLM cleared it). Server must still inject level_up_now + continue_adventuring.
        """
        game_state = {
            "player_character_data": {"level": 12, "class": "Rogue"},
            "rewards_pending": None,  # LLM set state_updates.rewards_pending=null
        }
        rewards_box = {
            "level_up_available": True,
            "current_xp": 120550.0,
            "next_level_xp": 120000.0,
            "xp_gained": 1200.0,
            "source": "deferred",
        }
        planning_block = {
            "thinking": "Tactical decision",
            "choices": [
                {"id": "full_lab_wipe", "text": "Execute Total Sanitization"},
                {"id": "tactical_extraction", "text": "Initiate Immediate Extraction"},
            ],
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state, rewards_box=rewards_box
        )

        assert injected is not None, "Should inject planning block when rewards_box.level_up_available=true"
        choices = injected.get("choices", [])
        choice_ids = [c.get("id") for c in choices]
        assert "level_up_now" in choice_ids, (
            f"level_up_now missing from choices: {choice_ids}. "
            "Server must inject level-up choices when rewards_box.level_up_available=true."
        )
        assert "continue_adventuring" in choice_ids, (
            f"continue_adventuring missing from choices: {choice_ids}. "
            "Server must inject level-up choices when rewards_box.level_up_available=true."
        )

    def test_inject_levelup_choices_with_multilevel_target_from_xp(self):
        """
        RED: rewards_box.level_up_available=true should infer new_level from XP progression.

        Scenario: level 1 with 3000 XP should infer Level 4 as target, not Level 2.
        """
        game_state = {
            "player_character_data": {"level": 1, "class": "Rogue", "xp": 3000},
            "rewards_pending": None,
        }
        rewards_box = {
            "level_up_available": True,
            "current_xp": 3000.0,
            "next_level_xp": 2700.0,
            "xp_gained": 3000.0,
            "source": "deferred",
        }
        planning_block = {
            "thinking": "Tactical decision",
            "choices": [
                {"id": "full_lab_wipe", "text": "Execute Total Sanitization"},
            ],
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state, rewards_box=rewards_box
        )

        choices = injected.get("choices", []) if injected is not None else []
        level_up_choice = next(
            (choice for choice in choices if choice.get("id") == "level_up_now"), None
        )
        assert level_up_choice is not None
        assert level_up_choice.get("text") == "Level Up to Level 4"

    def test_inject_levelup_choices_ignored_when_rewards_box_stale(self):
        """
        GREEN: rewards_box.level_up_available=true should not inject when state has no
        canonical level-up signal and server XP is below threshold.
        """
        game_state = {
            "player_character_data": {"level": 12, "class": "Rogue"},
            "rewards_pending": None,
        }
        rewards_box = {
            "level_up_available": True,
            "current_xp": 1200.0,
            "next_level_xp": 120000.0,
            "xp_gained": 1200.0,
            "source": "milestone",
        }
        planning_block = {
            "thinking": "Tactical decision",
            "choices": [{"id": "option_a", "text": "Option A"}],
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state, rewards_box=rewards_box
        )

        choices = injected.get("choices", []) if injected is not None else []
        choice_ids = [c.get("id") for c in choices]
        assert "level_up_now" not in choice_ids
        assert "continue_adventuring" not in choice_ids

    def test_inject_levelup_choices_rewards_box_false_no_injection(self):
        """
        GREEN guard: rewards_box.level_up_available=false + rewards_pending=null → no injection.
        """
        game_state = {
            "player_character_data": {"level": 12, "class": "Rogue"},
            "rewards_pending": None,
        }
        rewards_box = {
            "level_up_available": False,
            "xp_gained": 600.0,
            "source": "milestone",
        }
        planning_block = {
            "thinking": "Tactical decision",
            "choices": [{"id": "option_a", "text": "Option A"}],
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state, rewards_box=rewards_box
        )

        # No injection when level_up_available=false
        if injected is not None:
            choice_ids = [c.get("id") for c in injected.get("choices", [])]
            assert "level_up_now" not in choice_ids, (
                "Should NOT inject level-up choices when rewards_box.level_up_available=false"
            )

    def test_inject_levelup_choices_rewards_box_none_no_injection(self):
        """
        GREEN guard: no rewards_box + rewards_pending=null → no injection (no regression).
        """
        game_state = {
            "player_character_data": {"level": 12, "class": "Rogue"},
            "rewards_pending": None,
        }
        planning_block = {
            "thinking": "Tactical decision",
            "choices": [{"id": "option_a", "text": "Option A"}],
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state, rewards_box=None
        )

        # No injection when no rewards_box provided and rewards_pending=null
        if injected is not None:
            choice_ids = [c.get("id") for c in injected.get("choices", [])]
            assert "level_up_now" not in choice_ids, (
                "Should NOT inject level-up choices when rewards_box=None and rewards_pending=null"
            )

    def test_inject_levelup_choices_both_rewards_pending_and_rewards_box_set(self):
        """
        GREEN guard: both rewards_pending.level_up_available=true AND rewards_box.level_up_available=true.
        Should still inject (no double-injection or conflict).
        """
        game_state = {
            "player_character_data": {"level": 12, "class": "Rogue"},
            "rewards_pending": {"level_up_available": True, "new_level": 13},
        }
        rewards_box = {
            "level_up_available": True,
            "current_xp": 120550.0,
            "next_level_xp": 120000.0,
            "xp_gained": 1200.0,
        }
        planning_block = {
            "thinking": "Tactical decision",
            "choices": [{"id": "full_lab_wipe", "text": "Execute Total Sanitization"}],
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state, rewards_box=rewards_box
        )

        assert injected is not None
        choices = injected.get("choices", [])
        choice_ids = [c.get("id") for c in choices]
        assert "level_up_now" in choice_ids
        assert "continue_adventuring" in choice_ids

    def test_inject_levelup_choices_rewards_box_level_up_with_no_planning_block(self):
        """
        When rewards_box.level_up_available=true and planning_block=None,
        server creates a planning block with level-up choices.
        """
        game_state = {
            "player_character_data": {"level": 12, "class": "Rogue"},
            "rewards_pending": None,
        }
        rewards_box = {
            "level_up_available": True,
            "current_xp": 120550.0,
            "next_level_xp": 120000.0,
            "xp_gained": 1200.0,
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            None, game_state, rewards_box=rewards_box
        )

        assert injected is not None, "Should create planning block when rewards_box.level_up_available=true"
        choices = injected.get("choices", [])
        choice_ids = [c.get("id") for c in choices]
        assert "level_up_now" in choice_ids
        assert "continue_adventuring" in choice_ids


class TestLevelUpChoiceOrdering:
    """
    level_up_now must be the FIRST choice in planning_block
    when rewards_box.level_up_available=true, regardless of whether the LLM put it
    there or the server injected it.
    """

    def test_level_up_now_is_first_when_injected_with_existing_llm_choices(self):
        """
        RED: When server injects level_up_now into a block that has LLM choices,
        level_up_now must appear at index 0 (before other choices).
        """
        game_state = {
            "player_character_data": {"level": 12, "class": "Rogue"},
            "rewards_pending": None,
        }
        rewards_box = {
            "level_up_available": True,
            "current_xp": 120550.0,
            "next_level_xp": 120000.0,
            "xp_gained": 1200.0,
        }
        planning_block = {
            "thinking": "Tactical decision",
            "choices": [
                {"id": "full_lab_wipe", "text": "Execute Total Sanitization"},
                {"id": "tactical_extraction", "text": "Initiate Immediate Extraction"},
            ],
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state, rewards_box=rewards_box
        )

        assert injected is not None
        choices = injected.get("choices", [])
        assert len(choices) >= 3, f"Expected level_up + 2 original choices, got {len(choices)}"
        assert choices[0].get("id") == "level_up_now", (
            f"level_up_now must be FIRST choice when rewards_box.level_up_available=true. "
            f"Got: {[c.get('id') for c in choices]}"
        )

    def test_level_up_now_is_first_when_llm_provided_it_last(self):
        """
        RED: When LLM puts level_up_now at the END, server must reorder it to FIRST.
        """
        game_state = {
            "player_character_data": {"level": 5, "class": "Wizard"},
            "rewards_pending": {"level_up_available": True, "new_level": 6},
        }
        rewards_box = {
            "level_up_available": True,
            "current_xp": 120550.0,
            "next_level_xp": 120000.0,
        }
        planning_block = {
            "thinking": "Tactical decision",
            "choices": [
                {"id": "attack_dragon", "text": "Attack the Dragon"},
                {"id": "continue_adventuring", "text": "Continue Adventuring", "freeze_time": True},
                {"id": "level_up_now", "text": "Level Up to Level 6", "freeze_time": True},
            ],
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state, rewards_box=rewards_box
        )

        assert injected is not None
        choices = injected.get("choices", [])
        assert choices[0].get("id") == "level_up_now", (
            f"level_up_now must be FIRST even when LLM placed it last. "
            f"Got order: {[c.get('id') for c in choices]}"
        )

    def test_level_up_now_is_first_when_planning_block_is_none(self):
        """
        RED: When planning_block=None and server creates block, level_up_now is index 0.
        """
        game_state = {
            "player_character_data": {"level": 3, "class": "Fighter"},
            "rewards_pending": None,
        }
        rewards_box = {
            "level_up_available": True,
            "current_xp": 120550.0,
            "next_level_xp": 120000.0,
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            None, game_state, rewards_box=rewards_box
        )

        assert injected is not None
        choices = injected.get("choices", [])
        assert len(choices) >= 1
        assert choices[0].get("id") == "level_up_now", (
            f"level_up_now must be first when block is created from scratch. "
            f"Got: {[c.get('id') for c in choices]}"
        )

    def test_level_up_now_already_first_no_reorder(self):
        """
        GREEN guard: When level_up_now is already first, no unnecessary reordering.
        """
        game_state = {
            "player_character_data": {"level": 7, "class": "Paladin"},
            "rewards_pending": {"level_up_available": True, "new_level": 8},
        }
        rewards_box = {"level_up_available": True}
        planning_block = {
            "thinking": "Level up decision",
            "choices": [
                {"id": "level_up_now", "text": "Level Up to Level 8", "freeze_time": True},
                {"id": "continue_adventuring", "text": "Continue Adventuring", "freeze_time": True},
                {"id": "explore_dungeon", "text": "Explore the Dungeon"},
            ],
        }

        injected = world_logic._inject_levelup_choices_if_needed(
            planning_block, game_state, rewards_box=rewards_box
        )

        assert injected is not None
        choices = injected.get("choices", [])
        assert choices[0].get("id") == "level_up_now", (
            f"level_up_now should remain first. Got: {[c.get('id') for c in choices]}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
