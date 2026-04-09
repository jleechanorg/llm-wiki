import unittest
from unittest.mock import MagicMock

from mvp_site.agents import DialogAgent
from mvp_site.game_state import GameState


class TestDialogFailureReproduction(unittest.TestCase):
    """Reproduce reported DialogAgent failures."""

    def test_persuasion_action_triggers_dialog_state(self):
        """Test that a recent 'persuasion' action keeps DialogAgent active."""
        mock_game_state = MagicMock(spec=GameState)
        mock_game_state.is_in_combat.return_value = False
        mock_game_state.dialog_context = {"active": False}
        mock_game_state.planning_block = {}

        # User scenario: Just rolled for persuasion
        # Hypothethical last_action_type
        mock_game_state.last_action_type = "persuasion"

        # Expect True, but currently likely False
        self.assertTrue(
            DialogAgent.matches_game_state(mock_game_state),
            "DialogAgent should match game state after persuasion action",
        )


if __name__ == "__main__":
    unittest.main()
