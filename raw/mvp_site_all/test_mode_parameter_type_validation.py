"""
Test Mode Parameter Type Validation

Regression test for bug where mode parameter sent as dict/list/int instead
of string caused AttributeError: 'dict' object has no attribute 'lower'.

Bug details: .beads/mode-parameter-type-validation-bug.md
Occurred: 2026-01-23 04:43:11 UTC
Campaign: JXXNfJpdqNtH60HN942q
"""

import asyncio

from mvp_site.world_logic import process_action_unified


class TestModeParameterTypeValidation:
    """Ensure mode parameter handles invalid types gracefully without crashing."""

    def test_mode_as_dict_defaults_to_character_mode(self):
        """
        Mode sent as dict should be rejected and default to MODE_CHARACTER.

        Regression test for: 'dict' object has no attribute 'lower'
        """
        request = {
            "user_id": "test_user",
            "campaign_id": "test_campaign_type_validation",
            "user_input": "test action with invalid mode type",
            "mode": {"type": "character"},  # Invalid: dict instead of string
        }

        result = asyncio.run(process_action_unified(request))

        # Should NOT crash with AttributeError
        # Should return error or process with default mode
        assert isinstance(result, dict), "Should return dict response"

        # Should not have AttributeError in error message
        error_msg = str(result.get("error", ""))
        assert "'dict' object has no attribute" not in error_msg, (
            "Should not crash with AttributeError on dict mode"
        )
        assert "'dict' object has no attribute 'lower'" not in error_msg, (
            "Should not crash with .lower() call on dict"
        )

    def test_mode_as_int_defaults_to_character_mode(self):
        """Mode sent as int should be rejected and default to MODE_CHARACTER."""
        request = {
            "user_id": "test_user",
            "campaign_id": "test_campaign_type_validation",
            "user_input": "test action",
            "mode": 1,  # Invalid: int instead of string
        }

        result = asyncio.run(process_action_unified(request))

        assert isinstance(result, dict), "Should return dict response"
        error_msg = str(result.get("error", ""))
        assert "'int' object has no attribute" not in error_msg, (
            "Should not crash with AttributeError on int mode"
        )

    def test_mode_as_list_defaults_to_character_mode(self):
        """Mode sent as list should be rejected and default to MODE_CHARACTER."""
        request = {
            "user_id": "test_user",
            "campaign_id": "test_campaign_type_validation",
            "user_input": "test action",
            "mode": ["character"],  # Invalid: list instead of string
        }

        result = asyncio.run(process_action_unified(request))

        assert isinstance(result, dict), "Should return dict response"
        error_msg = str(result.get("error", ""))
        assert "'list' object has no attribute" not in error_msg, (
            "Should not crash with AttributeError on list mode"
        )

    def test_mode_as_none_defaults_to_character_mode(self):
        """Mode sent as None should default to MODE_CHARACTER."""
        request = {
            "user_id": "test_user",
            "campaign_id": "test_campaign_type_validation",
            "user_input": "test action",
            "mode": None,  # Invalid: None instead of string
        }

        result = asyncio.run(process_action_unified(request))

        assert isinstance(result, dict), "Should return dict response"
        error_msg = str(result.get("error", ""))
        assert "'NoneType' object has no attribute" not in error_msg, (
            "Should not crash with AttributeError on None mode"
        )

    def test_mode_missing_uses_default(self):
        """Mode omitted from request should default to MODE_CHARACTER."""
        request = {
            "user_id": "test_user",
            "campaign_id": "test_campaign_type_validation",
            "user_input": "test action",
            # mode field intentionally omitted
        }

        result = asyncio.run(process_action_unified(request))

        # This should work fine (mode defaults to MODE_CHARACTER)
        assert isinstance(result, dict), "Should return dict response"

    def test_valid_string_mode_works_correctly(self):
        """Valid string mode values should work as expected."""
        for mode_value in ["character", "god", "narrator"]:
            request = {
                "user_id": "test_user",
                "campaign_id": f"test_campaign_{mode_value}",
                "user_input": f"test action in {mode_value} mode",
                "mode": mode_value,  # Valid: string
            }

            result = asyncio.run(process_action_unified(request))

            # Should process normally (may return error for other reasons, but not mode type)
            assert isinstance(result, dict), f"Should return dict for mode={mode_value}"
            error_msg = str(result.get("error", ""))
            assert "object has no attribute 'lower'" not in error_msg, (
                f"Should not crash with AttributeError for valid mode={mode_value}"
            )
