"""
Campaign Settings Tests - Consolidated

Consolidated tests for campaign setting handling in agent_prompts.py:
1. test_campaign_setting_duplication.py - Campaign setting appears only once
2. test_campaign_setting_type_guards.py - Type guards for malformed game_state
3. test_god_mode_setting_in_system_instruction.py - god_mode.setting in system instructions

Bug fixes verified:
- Campaign setting not duplicated in system instructions
- Type guards prevent AttributeError on malformed game_state
- god_mode.setting properly flows to system instructions
"""

import unittest
from unittest.mock import Mock

from mvp_site.agent_prompts import PromptBuilder
from mvp_site.game_state import GameState


class TestCampaignSettingDuplication(unittest.TestCase):
    """Test that campaign setting is not duplicated in system instructions.

    Consolidated from test_campaign_setting_duplication.py.
    """

    def test_campaign_setting_appears_only_once_after_finalize(self):
        """
        Test campaign setting appears exactly once when finalize_instructions() is called.

        This test verifies the duplication fix: _append_campaign_setting_if_present()
        should only be called in finalize_instructions(), not in build_god_mode_instructions().

        Production path: build_from_order() → finalize_instructions()
        Legacy path: build_god_mode_instructions() (doesn't add campaign setting)
        """
        # Create mock game_state with campaign setting
        game_state = Mock()
        game_state.custom_campaign_state = {
            "god_mode": {
                "setting": "This is a unique test setting for campaign world lore."
            }
        }

        # Build prompt parts (simulating production path)
        builder = PromptBuilder(game_state)

        # Mock the helper methods to return empty strings (avoid Mock injection)
        builder.build_character_identity_block = Mock(return_value="")
        builder.build_god_mode_directives_block = Mock(return_value="")

        parts = ["# Master Directive"]  # Start with minimal parts

        # Call finalize_instructions (this should add campaign setting ONCE)
        final_instruction = builder.finalize_instructions(
            parts, use_default_world=False
        )

        # Count occurrences of the unique campaign setting text
        setting_text = "This is a unique test setting for campaign world lore."
        occurrences = final_instruction.count(setting_text)

        # ASSERTION: Campaign setting should appear exactly once
        self.assertEqual(
            occurrences,
            1,
            f"Campaign setting should appear exactly 1 time, found {occurrences} times",
        )

    def test_no_campaign_setting_when_missing(self):
        """
        Verify no campaign setting is added when god_mode.setting is absent.
        """
        game_state = Mock()
        game_state.custom_campaign_state = {}  # No god_mode

        builder = PromptBuilder(game_state)
        system_parts = builder.build_god_mode_instructions()
        system_instruction = "\n".join(system_parts)

        # ASSERTION: Should not contain campaign setting header
        self.assertNotIn("# Campaign Setting (Custom World Lore)", system_instruction)


class TestCampaignSettingTypeGuards(unittest.TestCase):
    """Test type guards for malformed game_state in campaign setting extraction.

    Consolidated from test_campaign_setting_type_guards.py.
    """

    def test_custom_campaign_state_is_none_no_crash(self):
        """
        RED TEST Issue 1: custom_campaign_state=None should not crash.

        hasattr() returns True if attribute exists even if it's None.
        The code must check isinstance(dict) before calling .get().
        """
        # Create mock with custom_campaign_state = None (not missing, but None)
        game_state = Mock()
        game_state.custom_campaign_state = None  # Will crash without isinstance check

        builder = PromptBuilder(game_state)
        parts = []

        # ASSERTION: Should not raise AttributeError
        try:
            builder._append_campaign_setting_if_present(parts)
        except AttributeError as e:
            self.fail(f"Should handle None custom_campaign_state gracefully, got: {e}")

        # Verify no campaign setting was added
        self.assertEqual(len(parts), 0)

    def test_custom_campaign_state_is_string_no_crash(self):
        """
        RED TEST Issue 1: custom_campaign_state as non-dict should not crash.
        """
        game_state = Mock()
        game_state.custom_campaign_state = "malformed string data"  # Not a dict

        builder = PromptBuilder(game_state)
        parts = []

        # ASSERTION: Should not raise AttributeError
        try:
            builder._append_campaign_setting_if_present(parts)
        except AttributeError as e:
            self.fail(
                f"Should handle non-dict custom_campaign_state gracefully, got: {e}"
            )

        # Verify no campaign setting was added
        self.assertEqual(len(parts), 0)

    def test_dict_custom_campaign_state_is_string_no_crash(self):
        """
        RED TEST Issue 2: Dict path - custom_campaign_state value is string, not dict.
        """
        # Dict-format game_state (not Mock object)
        game_state = {
            "custom_campaign_state": "malformed data"  # Should be dict
        }

        builder = PromptBuilder(game_state)
        parts = []

        # ASSERTION: Should not raise AttributeError
        try:
            builder._append_campaign_setting_if_present(parts)
        except AttributeError as e:
            self.fail(
                f"Should handle non-dict custom_campaign_state in dict path, got: {e}"
            )

        # Verify no campaign setting was added
        self.assertEqual(len(parts), 0)

    def test_empty_string_setting_is_rejected(self):
        """
        Test that empty string setting (after strip) is properly rejected.

        Note: This test verifies current behavior (falsy check).
        Per CLAUDE.md guidelines, empty strings should be valid until explicitly
        stripped and evaluated. The current code uses `if not setting:` which
        is technically acceptable here since we .strip() first.
        """
        game_state = Mock()
        game_state.custom_campaign_state = {
            "god_mode": {
                "setting": "   "  # Empty after strip
            }
        }

        builder = PromptBuilder(game_state)
        parts = []

        builder._append_campaign_setting_if_present(parts)

        # ASSERTION: Empty string setting should be rejected
        self.assertEqual(len(parts), 0)

    def test_valid_setting_is_added(self):
        """
        Verify valid campaign setting is successfully added.
        """
        game_state = Mock()
        game_state.custom_campaign_state = {
            "god_mode": {"setting": "Valid campaign world lore"}
        }

        builder = PromptBuilder(game_state)
        parts = []

        builder._append_campaign_setting_if_present(parts)

        # ASSERTION: Campaign setting should be added
        self.assertEqual(len(parts), 1)
        self.assertIn("Valid campaign world lore", parts[0])


class TestGodModeSettingInSystemInstruction:
    """Test that god_mode.setting is included in system instructions.

    Consolidated from test_god_mode_setting_in_system_instruction.py.
    """

    def test_god_mode_setting_included_in_system_instruction(self):
        """
        RED TEST: Verify god_mode.setting appears in system instruction.

        Expected behavior:
        - Campaign has god_mode.setting = "Custom world lore..."
        - System instruction should contain this setting text
        - Setting should NOT be truncated or ignored
        """
        # Arrange: Create game state with god_mode setting
        custom_setting = "# MY CUSTOM WORLD\n\nThis is a unique fantasy realm with specific rules and lore."

        game_state = Mock(spec=GameState)
        game_state.campaign_id = "test-campaign"
        # god_mode is stored in custom_campaign_state["god_mode"], not as a direct attribute
        game_state.custom_campaign_state = {
            "god_mode": {
                "character": {"name": "Test Hero"},
                "setting": custom_setting,
                "description": "A test campaign",
            }
        }
        game_state.debug_info = {}

        # Act: Build system instructions
        builder = PromptBuilder(game_state=game_state)
        god_mode_instructions = builder.build_god_mode_instructions()
        builder.build_character_identity_block = Mock(return_value="")
        builder.build_god_mode_directives_block = Mock(return_value="")

        # Finalize to insert campaign setting
        system_instruction = builder.finalize_instructions(
            god_mode_instructions,
            use_default_world=False,
        )

        # Assert: Custom setting MUST appear in system instruction
        assert custom_setting in system_instruction, (
            f"god_mode.setting not found in system instruction!\n"
            f"Setting: {custom_setting[:100]}...\n"
            f"System instruction length: {len(system_instruction)} chars\n"
            f"System instruction preview: {system_instruction[:500]}..."
        )

    def test_large_god_mode_setting_not_truncated_prematurely(self):
        """
        RED TEST: Large god_mode.setting should NOT be truncated before budget allocation.

        The budget allocator should receive the FULL setting and decide whether
        to compact it. Pre-truncation prevents budget warnings from triggering.
        """
        # Arrange: Create game state with LARGE setting (100k tokens)
        large_setting = "# MASSIVE WORLD ENCYCLOPEDIA\n\n" + "\n\n".join(
            [
                f"## Region {i}: Detailed lore about this region including history, "
                f"geography, politics, notable characters, and cultural practices. "
                * 20  # Make each region substantial
                for i in range(1, 500)  # 500 regions = ~100k tokens
            ]
        )

        game_state = Mock(spec=GameState)
        game_state.campaign_id = "test-large-setting"
        # god_mode is stored in custom_campaign_state["god_mode"], not as a direct attribute
        game_state.custom_campaign_state = {
            "god_mode": {
                "character": {"name": "Test Hero"},
                "setting": large_setting,
                "description": "Large world test",
            }
        }
        game_state.debug_info = {}

        # Act: Build system instructions
        builder = PromptBuilder(game_state=game_state)
        god_mode_instructions = builder.build_god_mode_instructions()
        builder.build_character_identity_block = Mock(return_value="")
        builder.build_god_mode_directives_block = Mock(return_value="")
        system_instruction = builder.finalize_instructions(
            god_mode_instructions,
            use_default_world=False,
        )

        # Assert: Large setting should appear (not pre-truncated)
        # We check for content from the middle and end to ensure it's not truncated
        assert "Region 250:" in system_instruction, (
            "Large setting was pre-truncated! Region 250 missing."
        )
        assert "Region 499:" in system_instruction, (
            "Large setting was pre-truncated! Region 499 missing."
        )

        # Verify size is reasonable for large setting
        min_expected_chars = (
            200_000  # 100k tokens ≈ 400k chars, but base prompts add more
        )
        assert len(system_instruction) > min_expected_chars, (
            f"System instruction too small: {len(system_instruction)} chars. "
            f"Expected >{min_expected_chars} chars for large setting."
        )

    def test_god_mode_setting_with_special_characters(self):
        """
        RED TEST: god_mode.setting with special characters should be preserved.
        """
        # Arrange: Setting with special markdown, newlines, etc.
        special_setting = """# World of Éthernia

## The Côte d'Azur Region
- Population: 1,000,000+
- Notable quote: "We live by the sword & die by the spell"
- Currency: ₹ (Rupees), € (Euros), ¥ (Yen)

### Factions
1. The Order of the Phoenix
2. The Shadow Guild (est. '1420)
"""

        game_state = Mock(spec=GameState)
        game_state.campaign_id = "test-special-chars"
        # god_mode is stored in custom_campaign_state["god_mode"], not as a direct attribute
        game_state.custom_campaign_state = {
            "god_mode": {
                "setting": special_setting,
            }
        }
        game_state.debug_info = {}

        # Act
        builder = PromptBuilder(game_state=game_state)
        god_mode_instructions = builder.build_god_mode_instructions()
        builder.build_character_identity_block = Mock(return_value="")
        builder.build_god_mode_directives_block = Mock(return_value="")
        system_instruction = builder.finalize_instructions(
            god_mode_instructions,
            use_default_world=False,
        )

        # Assert: Special characters preserved
        assert "Éthernia" in system_instruction
        assert "Côte d'Azur" in system_instruction
        assert "₹" in system_instruction or "Rupees" in system_instruction
        assert "'1420" in system_instruction


if __name__ == "__main__":
    unittest.main()
