import unittest
from unittest.mock import MagicMock, patch

from mvp_site.agent_prompts import PromptBuilder
from mvp_site.agents import DialogAgent


class TestDialogPromptLoading(unittest.TestCase):
    def setUp(self):
        self.mock_game_state = MagicMock()
        self.agent = DialogAgent(self.mock_game_state)

    @patch("mvp_site.agent_prompts.read_file_cached")
    def test_dialog_agent_loads_correct_instruction_file(self, mock_read_file):
        """Verify that building prompts for DialogAgent includes dialog_system_instruction.md."""

        # Setup mock return values for the expected files
        def side_effect(file_path):
            if "dialog_system_instruction.md" in file_path:
                return "CONTENT_FROM_DIALOG_INSTRUCTION"
            if "master_directive.md" in file_path:
                return "CONTENT_FROM_MASTER_DIRECTIVE"
            if "game_state_instruction.md" in file_path:
                return "CONTENT_FROM_GAME_STATE"
            if "planning_protocol.md" in file_path:
                return "CONTENT_FROM_PLANNING"
            if "character_template.md" in file_path:
                return "CONTENT_FROM_CHARACTER_TEMPLATE"
            if "relationship_instruction.md" in file_path:
                return "CONTENT_FROM_RELATIONSHIP"
            return "UNKNOWN_FILE_CONTENT"

        mock_read_file.side_effect = side_effect

        # Build prompts
        builder = PromptBuilder(self.mock_game_state)
        prompts = builder.build_for_agent(self.agent)

        # Combine all parts to check for our specific content
        full_prompt = "\n".join(prompts)

        # Verify the specific content from dialog_system_instruction.md is present
        self.assertIn("CONTENT_FROM_DIALOG_INSTRUCTION", full_prompt)

        # Verify it loaded the file corresponding to PROMPT_TYPE_DIALOG
        # We can also check args if we want to be stricter about which file path was requested,
        # but verifying the content is the ultimate integration test.
