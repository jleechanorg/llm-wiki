"""
TDD Test for REV-0g1y: Inconsistent level-up active-state logic

Issue: get_agent_for_input and _inject_modal_finish_choice_if_needed
use different logic to determine if level-up is active.

Expected: Both should use same logic, including stale flag guards.
"""

import unittest

from mvp_site import world_logic


class TestREV0g1yInconsistentDetection(unittest.TestCase):
    """Test level-up active detection consistency."""

    def test_injection_respects_stale_in_progress_false_flag(self):
        """
        REV-0g1y: _inject_modal_finish_choice_if_needed should respect
        level_up_in_progress=False stale guard like get_agent_for_input does.

        When level_up_in_progress=False explicitly, finish choice should NOT inject
        even if rewards_pending.level_up_available=True.
        """
        game_state_dict = {
            "custom_campaign_state": {
                "level_up_in_progress": False,  # Explicitly False (stale guard)
            },
            "rewards_pending": {
                "level_up_available": True,  # Leftover stale flag
            }
        }

        # Mock planning block
        planning_block = {
            "thinking": "Test thinking",
            "choices": {
                "explore": {
                    "text": "Explore the forest",
                    "description": "Go exploring"
                }
            }
        }

        result = world_logic._inject_modal_finish_choice_if_needed(
            planning_block,
            game_state_dict
        )

        # Should NOT inject finish choice because level_up_in_progress=False
        # BUT current implementation doesn't check this - it will inject!
        # This is the bug.
        if result is not None:
            self.assertNotIn(
                "finish_level_up_return_to_game",
                result.get("choices", {}),
                "_inject_modal_finish_choice_if_needed must respect level_up_in_progress=False "
                "stale guard, just like get_agent_for_input does. "
                "INCONSISTENCY: Routing won't activate modal but injection will add finish choice!"
            )

    def test_injection_respects_stale_pending_false_flag(self):
        """
        REV-0g1y: _inject_modal_finish_choice_if_needed should respect
        level_up_pending=False stale guard.

        When level_up_pending=False and level_up_in_progress not True,
        finish choice should NOT inject.
        """
        game_state_dict = {
            "custom_campaign_state": {
                "level_up_pending": False,  # Explicitly False
                # level_up_in_progress not set (None)
            },
            "rewards_pending": {
                "level_up_available": True,  # Leftover stale flag
            }
        }

        planning_block = {
            "thinking": "Test thinking",
            "choices": {
                "explore": {
                    "text": "Explore",
                    "description": "Explore"
                }
            }
        }

        result = world_logic._inject_modal_finish_choice_if_needed(
            planning_block,
            game_state_dict
        )

        # Should NOT inject finish choice
        if result is not None:
            self.assertNotIn(
                "finish_level_up_return_to_game",
                result.get("choices", {}),
                "_inject_modal_finish_choice_if_needed must respect level_up_pending=False "
                "stale guard when level_up_in_progress is not True"
            )


if __name__ == '__main__':
    unittest.main()
