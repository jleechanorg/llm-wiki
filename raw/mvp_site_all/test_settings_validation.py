"""
Unit tests for settings_validation module.

Tests the extracted settings validation helpers using TDD methodology.
These tests are written BEFORE the implementation (RED phase).
"""

import ast
from collections import Counter
from ipaddress import ip_address
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from mvp_site.settings_validation import (
    validate_api_key,
    validate_llm_provider,
    validate_gemini_model,
    validate_openrouter_model,
    validate_cerebras_model,
    validate_openclaw_gateway_url,
    validate_openclaw_gateway_port,
    validate_boolean_setting,
    validate_theme,
    validate_pre_spicy_model,
    validate_pre_spicy_provider,
    validate_model_provider_match,
)


class TestStandardValidatorsRegistry(unittest.TestCase):
    """Tests for the settings validation registry."""

    def test_standard_validators_no_duplicate_keys_in_source(self):
        """Ensure _STANDARD_VALIDATORS dict definition has no duplicate source keys."""
        module_path = Path(__file__).resolve().parents[1] / "settings_validation.py"
        source = module_path.read_text(encoding="utf-8")
        module_ast = ast.parse(source)

        standard_validators_node = None
        for node in module_ast.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "_STANDARD_VALIDATORS":
                        standard_validators_node = node.value
                        break
            if standard_validators_node is not None:
                break

        self.assertIsNotNone(
            standard_validators_node,
            "_STANDARD_VALIDATORS assignment not found in settings_validation.py",
        )
        self.assertIsInstance(
            standard_validators_node,
            ast.Dict,
            "_STANDARD_VALIDATORS must be defined with a dictionary literal",
        )

        raw_keys = []
        for key in standard_validators_node.keys:
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                raw_keys.append(key.value)
            elif isinstance(key, ast.Str):
                raw_keys.append(key.s)

        duplicates = [key for key, count in Counter(raw_keys).items() if count > 1]
        self.assertEqual(
            duplicates,
            [],
            f"Duplicate _STANDARD_VALIDATORS keys detected: {duplicates}",
        )


class TestValidateApiKeys(unittest.TestCase):
    """Tests for BYOK API key validation behavior under TESTING_AUTH_BYPASS."""

    def test_api_key_rejects_short_key_when_auth_bypass_without_explicit_validation_override(self):
        with patch.dict(
            os.environ,
            {"TESTING_AUTH_BYPASS": "true"},
        ):
            result, error = validate_api_key("foorbar", "Gemini")

            self.assertIsNone(result)
            self.assertIsNotNone(error)
            self.assertIn("between 16 and 200", error)

    def test_api_key_bypasses_validation_when_explicitly_disabled(self):
        with patch.dict(
            os.environ,
            {"TESTING_AUTH_BYPASS": "true", "BYOK_ENFORCE_KEY_VALIDATION": "false"},
        ):
            result, error = validate_api_key("foorbar", "Gemini")

            self.assertIsNone(error)
            self.assertEqual(result, "foorbar")

    def test_api_key_enforcement_for_blank_override_value(self):
        with patch.dict(
            os.environ,
            {"TESTING_AUTH_BYPASS": "true", "BYOK_ENFORCE_KEY_VALIDATION": "   "},
        ):
            result, error = validate_api_key("foorbar", "Gemini")

            self.assertIsNone(result)
            self.assertIsNotNone(error)
            self.assertIn("between 16 and 200", error)

    def test_api_key_rejects_short_key_when_enforcement_enabled(self):
        with patch.dict(
            os.environ,
            {"TESTING_AUTH_BYPASS": "true", "BYOK_ENFORCE_KEY_VALIDATION": "true"},
        ):
            result, error = validate_api_key("foorbar", "Gemini")

            self.assertIsNone(result)
            self.assertIsNotNone(error)
            self.assertIn("between 16 and 200", error)


class TestValidateLlmProvider(unittest.TestCase):
    """Tests for validate_llm_provider function."""

    
    def test_valid_gemini_provider(self):
        """Valid 'gemini' provider should return normalized value."""
        result, error = validate_llm_provider("gemini")
        self.assertIsNone(error)
        self.assertEqual(result, "gemini")

    
    def test_valid_openrouter_provider(self):
        """Valid 'openrouter' provider should return normalized value."""
        result, error = validate_llm_provider("openrouter")
        self.assertIsNone(error)
        self.assertEqual(result, "openrouter")

    
    def test_valid_cerebras_provider(self):
        """Valid 'cerebras' provider should return normalized value."""
        result, error = validate_llm_provider("cerebras")
        self.assertIsNone(error)
        self.assertEqual(result, "cerebras")

    def test_valid_openclaw_provider(self):
        """Valid 'openclaw' provider should return normalized value."""
        result, error = validate_llm_provider("openclaw")
        self.assertIsNone(error)
        self.assertEqual(result, "openclaw")

    
    def test_invalid_provider_rejected(self):
        """Invalid provider should return error."""
        result, error = validate_llm_provider("invalid-provider")
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("Invalid", error)

    
    def test_case_insensitive_provider(self):
        """Provider validation should be case-insensitive."""
        result, error = validate_llm_provider("GEMINI")
        self.assertIsNone(error)
        self.assertEqual(result, "gemini")  # Should normalize to lowercase

    
    def test_non_string_provider_rejected(self):
        """Non-string provider value should return error."""
        result, error = validate_llm_provider(12345)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("must be a string", error)


class TestValidateGeminiModel(unittest.TestCase):
    """Tests for validate_gemini_model function."""

    
    def test_valid_gemini_model(self):
        """Valid Gemini model should pass validation."""
        result, error = validate_gemini_model("gemini-3-flash-preview")
        self.assertIsNone(error)
        self.assertEqual(result, "gemini-3-flash-preview")

    
    def test_legacy_gemini_model_mapped(self):
        """Legacy Gemini models should be accepted via mapping."""
        result, error = validate_gemini_model("gemini-2.5-flash")
        self.assertIsNone(error)
        # May return mapped model or original - both acceptable

    
    def test_invalid_gemini_model_rejected(self):
        """Invalid Gemini model should return error."""
        result, error = validate_gemini_model("not-a-real-model")
        self.assertIsNone(result)
        self.assertIsNotNone(error)

    
    def test_non_string_model_rejected(self):
        """Non-string model value should return error."""
        result, error = validate_gemini_model(12345)
        self.assertIsNone(result)
        self.assertIsNotNone(error)

    
    def test_case_insensitive_model(self):
        """Model validation should be case-insensitive."""
        result, error = validate_gemini_model("GEMINI-3-FLASH-PREVIEW")
        self.assertIsNone(error)


class TestValidateOpenRouterModel(unittest.TestCase):
    """Tests for validate_openrouter_model function."""

    
    def test_valid_openrouter_model(self):
        """Valid OpenRouter model should pass validation."""
        result, error = validate_openrouter_model("meta-llama/llama-3.1-70b-instruct")
        self.assertIsNone(error)
        self.assertEqual(result, "meta-llama/llama-3.1-70b-instruct")

    
    def test_invalid_openrouter_model_rejected(self):
        """Invalid OpenRouter model should return error."""
        result, error = validate_openrouter_model("not-a-real-model")
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("Invalid OpenRouter model", error)

    
    def test_non_string_openrouter_model_rejected(self):
        """Non-string OpenRouter model should return error."""
        result, error = validate_openrouter_model(12345)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("must be a string", error)


class TestValidateCerebrasModel(unittest.TestCase):
    """Tests for validate_cerebras_model function."""

    
    def test_valid_cerebras_model(self):
        """Valid Cerebras model should pass validation."""
        result, error = validate_cerebras_model("llama-3.3-70b")
        self.assertIsNone(error)
        self.assertEqual(result, "llama-3.3-70b")

    
    def test_invalid_cerebras_model_rejected(self):
        """Invalid Cerebras model should return error."""
        result, error = validate_cerebras_model("not-a-real-model")
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("Invalid Cerebras model", error)

    
    def test_non_string_cerebras_model_rejected(self):
        """Non-string Cerebras model should return error."""
        result, error = validate_cerebras_model(12345)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("must be a string", error)


class TestValidateBooleanSetting(unittest.TestCase):
    """Tests for validate_boolean_setting function."""

    
    def test_true_value_accepted(self):
        """Boolean True should be accepted."""
        result, error = validate_boolean_setting(True, "debug_mode")
        self.assertIsNone(error)
        self.assertTrue(result)

    
    def test_false_value_accepted(self):
        """Boolean False should be accepted."""
        result, error = validate_boolean_setting(False, "debug_mode")
        self.assertIsNone(error)
        self.assertFalse(result)

    
    def test_string_true_rejected(self):
        """String 'true' should be rejected (not a boolean)."""
        result, error = validate_boolean_setting("true", "debug_mode")
        self.assertIsNone(result)
        self.assertIsNotNone(error)

    
    def test_integer_rejected(self):
        """Integer should be rejected (not a boolean)."""
        result, error = validate_boolean_setting(1, "debug_mode")
        self.assertIsNone(result)
        self.assertIsNotNone(error)


class TestValidateTheme(unittest.TestCase):
    """Tests for validate_theme function."""

    
    def test_valid_theme_accepted(self):
        """Valid theme string should be accepted."""
        result, error = validate_theme("dark")
        self.assertIsNone(error)
        self.assertEqual(result, "dark")

    
    def test_non_string_theme_rejected(self):
        """Non-string theme should be rejected."""
        result, error = validate_theme(123)
        self.assertIsNone(result)
        self.assertIsNotNone(error)

    
    def test_too_long_theme_rejected(self):
        """Theme over 50 characters should be rejected."""
        long_theme = "a" * 51
        result, error = validate_theme(long_theme)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("too long", error.lower())




class TestValidatePreSpicyModel(unittest.TestCase):
    """Tests for validate_pre_spicy_model function."""

    
    def test_valid_model_returns_model_and_provider(self):
        """Valid model should return model, inferred provider, no error."""
        model, provider, error = validate_pre_spicy_model("gemini-3-flash-preview")
        self.assertIsNone(error)
        self.assertEqual(model, "gemini-3-flash-preview")
        self.assertIsNotNone(provider)

    
    def test_valid_openclaw_model_returns_openclaw_provider(self):
        """OpenClaw-prefixed model should infer openclaw provider."""
        model, provider, error = validate_pre_spicy_model(
            "openclaw/gemini-3-flash-preview"
        )
        self.assertIsNone(error)
        self.assertEqual(model, "openclaw/gemini-3-flash-preview")
        self.assertEqual(provider, "openclaw")

    
    def test_invalid_openclaw_model_format_rejected(self):
        """Malformed OpenClaw model should be rejected."""
        model, provider, error = validate_pre_spicy_model("openclaw/")
        self.assertIsNone(model)
        self.assertIsNone(provider)
        self.assertIsNotNone(error)

    
    def test_invalid_model_returns_error(self):
        """Invalid model should return None, None, error."""
        model, provider, error = validate_pre_spicy_model("fake-model")
        self.assertIsNone(model)
        self.assertIsNone(provider)
        self.assertIsNotNone(error)

    
    def test_non_string_pre_spicy_model_rejected(self):
        """Non-string pre_spicy_model should return error."""
        model, provider, error = validate_pre_spicy_model(12345)
        self.assertIsNone(model)
        self.assertIsNone(provider)
        self.assertIsNotNone(error)


class TestValidatePreSpicyProvider(unittest.TestCase):
    """Tests for validate_pre_spicy_provider function."""

    
    def test_valid_provider_normalized(self):
        """Valid provider should be normalized to lowercase."""
        result, error = validate_pre_spicy_provider("GEMINI")
        self.assertIsNone(error)
        self.assertEqual(result, "gemini")

    
    def test_invalid_provider_rejected(self):
        """Invalid provider should return error."""
        result, error = validate_pre_spicy_provider("invalid-provider")
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("Invalid pre-spicy provider", error)

    
    def test_non_string_provider_rejected(self):
        """Non-string provider should return error."""
        result, error = validate_pre_spicy_provider(12345)
        self.assertIsNone(result)
        self.assertIsNotNone(error)


class TestValidateModelProviderMatch(unittest.TestCase):
    """Tests for validate_model_provider_match function."""

    
    def test_matching_model_provider_ok(self):
        """Gemini model with gemini provider should match."""
        error = validate_model_provider_match("gemini-3-flash-preview", "gemini")
        self.assertIsNone(error)

    
    def test_matching_openclaw_model_provider_ok(self):
        """OpenClaw model with openclaw provider should match."""
        error = validate_model_provider_match(
            "openclaw/gemini-3-flash-preview", "openclaw"
        )
        self.assertIsNone(error)

    
    def test_mismatched_model_provider_error(self):
        """Gemini model with openrouter provider should error."""
        error = validate_model_provider_match("gemini-3-flash-preview", "openrouter")
        self.assertIsNotNone(error)
        self.assertIn("belongs to provider", error)

    def test_mismatched_openclaw_model_provider_error(self):
        """OpenClaw model with non-openclaw provider should error."""
        error = validate_model_provider_match(
            "openclaw/gemini-3-flash-preview", "gemini"
        )
        self.assertIsNotNone(error)
        self.assertIn("belongs to provider", error)

    
    def test_unrecognized_model_allows_any_provider(self):
        """Unrecognized model (can't infer provider) should allow any provider."""
        # Custom/unrecognized model that can't be mapped to a provider
        error = validate_model_provider_match("custom-model-xyz", "gemini")
        self.assertIsNone(error)  # Should not error - can't infer provider


class TestValidateSettingsBatch(unittest.TestCase):
    """Tests for validate_settings_batch function."""

    
    def test_batch_validates_multiple_settings(self):
        """Batch validation should validate multiple settings at once."""
        from mvp_site.settings_validation import validate_settings_batch

        settings = {
            "llm_provider": "gemini",
            "debug_mode": True,
            "theme": "dark",
        }
        validated, error = validate_settings_batch(settings)
        self.assertIsNone(error)
        self.assertEqual(validated["llm_provider"], "gemini")
        self.assertEqual(validated["debug_mode"], True)
        self.assertEqual(validated["theme"], "dark")

    
    def test_batch_stops_on_first_error(self):
        """Batch validation should stop and return error on first invalid setting."""
        from mvp_site.settings_validation import validate_settings_batch

        settings = {
            "llm_provider": "invalid-provider",
            "debug_mode": True,
        }
        validated, error = validate_settings_batch(settings)
        self.assertIsNotNone(error)
        self.assertIn("Invalid", error)

    
    def test_batch_handles_boolean_settings(self):
        """Batch validation should handle all boolean settings."""
        from mvp_site.settings_validation import validate_settings_batch

        settings = {
            "debug_mode": False,
            "faction_minigame_enabled": True,
            "spicy_mode": False,
            "auto_save": True,
        }
        validated, error = validate_settings_batch(settings)
        self.assertIsNone(error)
        self.assertEqual(len(validated), 4)

    
    def test_batch_handles_pre_spicy_model(self):
        """Batch validation should handle pre_spicy_model specially."""
        from mvp_site.settings_validation import validate_settings_batch

        settings = {"pre_spicy_model": "gemini-3-flash-preview"}
        validated, error = validate_settings_batch(settings)
        self.assertIsNone(error)
        self.assertEqual(validated["pre_spicy_model"], "gemini-3-flash-preview")

    
    def test_batch_skips_unknown_settings(self):
        """Batch validation should skip unknown settings when some known ones exist."""
        from mvp_site.settings_validation import validate_settings_batch

        settings = {
            "llm_provider": "gemini",
            "unknown_setting": "value",  # Should be skipped
        }
        validated, error = validate_settings_batch(settings)
        self.assertIsNone(error)
        self.assertIn("llm_provider", validated)
        self.assertNotIn("unknown_setting", validated)

    
    def test_batch_errors_when_all_keys_unknown(self):
        """Batch validation should error when ALL keys are unknown (prevents silent no-op)."""
        from mvp_site.settings_validation import validate_settings_batch

        settings = {
            "typo_setting": "value",
            "another_typo": "value2",
        }
        validated, error = validate_settings_batch(settings)
        self.assertIsNotNone(error)
        self.assertIn("No recognized settings", error)
        self.assertIn("typo_setting", error)
        self.assertEqual(validated, {})

    
    def test_batch_error_on_invalid_boolean(self):
        """Batch validation should error on invalid boolean setting."""
        from mvp_site.settings_validation import validate_settings_batch

        settings = {"debug_mode": "not-a-boolean"}
        validated, error = validate_settings_batch(settings)
        self.assertIsNotNone(error)
        self.assertIn("must be a boolean", error)

    
    def test_batch_error_on_invalid_pre_spicy_model(self):
        """Batch validation should error on invalid pre_spicy_model."""
        from mvp_site.settings_validation import validate_settings_batch

        settings = {"pre_spicy_model": "invalid-model-xyz"}
        validated, error = validate_settings_batch(settings)
        self.assertIsNotNone(error)
        self.assertIn("Invalid", error)


class TestValidateSettingsWithCrossValidation(unittest.TestCase):
    """Tests for validate_settings_with_cross_validation function."""

    
    def test_validates_settings_without_model_provider(self):
        """Cross-validation should work for settings without model/provider."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {"debug_mode": True, "theme": "dark"}
        validated, error = validate_settings_with_cross_validation(settings)
        self.assertIsNone(error)
        self.assertEqual(validated["debug_mode"], True)
        self.assertEqual(validated["theme"], "dark")

    
    def test_validates_matching_model_and_provider(self):
        """Cross-validation should pass for matching model and provider."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {
            "pre_spicy_model": "gemini-3-flash-preview",
            "pre_spicy_provider": "gemini",
        }
        validated, error = validate_settings_with_cross_validation(settings)
        self.assertIsNone(error)
        self.assertEqual(validated["pre_spicy_model"], "gemini-3-flash-preview")
        self.assertEqual(validated["pre_spicy_provider"], "gemini")

    
    def test_cross_validation_accepts_openclaw_model_provider(self):
        """Cross-validation should accept matching OpenClaw model and provider."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {
            "pre_spicy_model": "openclaw/gemini-3-flash-preview",
            "pre_spicy_provider": "openclaw",
        }
        validated, error = validate_settings_with_cross_validation(settings)
        self.assertIsNone(error)
        self.assertEqual(
            validated["pre_spicy_model"], "openclaw/gemini-3-flash-preview"
        )
        self.assertEqual(validated["pre_spicy_provider"], "openclaw")

    
    def test_cross_validation_rejects_openclaw_provider_with_wrong_model(self):
        """Cross-validation should reject OpenClaw model/provider mismatch."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {
            "pre_spicy_model": "openclaw/gemini-3-flash-preview",
            "pre_spicy_provider": "openrouter",
        }
        validated, error = validate_settings_with_cross_validation(settings)
        self.assertIsNotNone(error)
        self.assertIn("belongs to provider", error.lower())

    
    def test_rejects_mismatched_model_and_provider(self):
        """Cross-validation should reject mismatched model and provider."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {
            "pre_spicy_model": "gemini-3-flash-preview",  # Gemini model
            "pre_spicy_provider": "openrouter",  # Wrong provider
        }
        validated, error = validate_settings_with_cross_validation(settings)
        self.assertIsNotNone(error)
        self.assertIn("gemini", error.lower())

    
    def test_cross_validates_model_against_existing_provider(self):
        """Cross-validation should check model against existing provider."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {"pre_spicy_model": "gemini-3-flash-preview"}  # Gemini model
        existing = {"pre_spicy_provider": "openrouter"}  # Existing: OpenRouter
        validated, error = validate_settings_with_cross_validation(settings, existing)
        self.assertIsNotNone(error)  # Should fail: Gemini model with OpenRouter provider

    
    def test_cross_validates_provider_against_existing_model(self):
        """Cross-validation should check provider against existing model."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {"pre_spicy_provider": "cerebras"}  # Setting Cerebras
        existing = {"pre_spicy_model": "gemini-3-flash-preview"}  # Existing: Gemini model
        validated, error = validate_settings_with_cross_validation(settings, existing)
        self.assertIsNotNone(error)  # Should fail: Cerebras provider with Gemini model

    
    def test_handles_non_dict_existing_settings(self):
        """Cross-validation should guard against non-dict existing_settings."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {"pre_spicy_model": "gemini-3-flash-preview"}
        # Simulate corrupt Firestore data (non-dict)
        existing = "corrupted_string_value"
        validated, error = validate_settings_with_cross_validation(settings, existing)
        # Should not crash, should pass (no existing provider to validate against)
        self.assertIsNone(error)
        self.assertEqual(validated["pre_spicy_model"], "gemini-3-flash-preview")

    
    def test_handles_none_existing_settings(self):
        """Cross-validation should handle None existing_settings gracefully."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {"pre_spicy_model": "gemini-3-flash-preview"}
        validated, error = validate_settings_with_cross_validation(settings, None)
        self.assertIsNone(error)
        self.assertEqual(validated["pre_spicy_model"], "gemini-3-flash-preview")


    def test_guards_against_non_string_existing_model(self):
        """Cross-validation should ignore non-string existing model values."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {"pre_spicy_provider": "gemini"}
        # Existing model is not a string (corrupt data)
        existing = {"pre_spicy_model": 12345}
        validated, error = validate_settings_with_cross_validation(settings, existing)
        # Should pass - invalid existing model is ignored
        self.assertIsNone(error)


    def test_batch_validation_error_propagates(self):
        """Cross-validation should propagate batch validation errors."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {"pre_spicy_model": "invalid-model-xyz"}
        validated, error = validate_settings_with_cross_validation(settings)
        self.assertIsNotNone(error)
        self.assertIn("Invalid", error)

    def test_cross_validation_bypasses_openclaw_gateway_validation_for_non_openclaw_provider(self):
        """OpenClaw gateway settings should be ignored unless OpenClaw is selected."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {
            "llm_provider": "gemini",
            "openclaw_gateway_url": "https://definitely-not-a-real-host-for-openclaw.example",
            "openclaw_gateway_port": 18789,
            "openclaw_gateway_token": "short",  # Too short when validated directly
        }

        validated, error = validate_settings_with_cross_validation(
            settings,
            target_llm_provider="gemini",
        )
        self.assertIsNone(error)
        self.assertEqual(validated["llm_provider"], "gemini")
        self.assertNotIn("openclaw_gateway_url", validated)
        self.assertNotIn("openclaw_gateway_port", validated)
        self.assertNotIn("openclaw_gateway_token", validated)

    def test_cross_validation_still_validates_openclaw_gateway_for_openclaw_provider(self):
        """OpenClaw provider should still validate per-user OpenClaw gateway fields."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {
            "llm_provider": "openclaw",
            "openclaw_gateway_url": "https://definitely-not-a-real-host-for-openclaw.example",
        }

        validated, error = validate_settings_with_cross_validation(
            settings,
            target_llm_provider="openclaw",
        )
        self.assertIsNotNone(error)
        self.assertIn("openclaw", error.lower())
        self.assertIn("cannot resolve hostname", error.lower())

    def test_cross_validation_with_missing_target_provider_validates_openclaw_gateway_fields(self):
        """Missing target provider should not skip OpenClaw field validation."""
        from mvp_site.settings_validation import validate_settings_with_cross_validation

        settings = {
            "openclaw_gateway_url": "not-a-url",
        }

        validated, error = validate_settings_with_cross_validation(settings)
        self.assertIsNotNone(error)
        self.assertIn("openclaw gateway", error.lower())
        self.assertNotIn("openclaw_gateway_url", validated)


class TestValidateOpenClawGatewayUrl(unittest.TestCase):
    """Tests for OpenClaw remote gateway URL validation."""

    def test_accepts_publicly_resolvable_tailscale_funnel_url(self):
        with patch(
            "mvp_site.settings_validation._resolve_gateway_host_ips",
            return_value=[ip_address("8.8.8.8")],
        ):
            result, error = validate_openclaw_gateway_url(
                "https://my-public-funnel.ts.net"
            )

        self.assertEqual(result, "https://my-public-funnel.ts.net")
        self.assertIsNone(error)

    def test_rejects_unresolvable_tailscale_magicdns_hostname_with_funnel_hint(self):
        with patch(
            "mvp_site.settings_validation._resolve_gateway_host_ips",
            return_value=[],
        ):
            result, error = validate_openclaw_gateway_url(
                "https://my-mac.tail5eb762.ts.net"
            )

        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("public tailscale funnel url", error.lower())
        self.assertIn("tailnet-only", error.lower())
        self.assertIn("tailscale serve hostnames", error.lower())
        self.assertNotIn("`", error)

    def test_rejects_unresolvable_org_tailnet_tsnet_hostname_with_funnel_hint(self):
        with patch(
            "mvp_site.settings_validation._resolve_gateway_host_ips",
            return_value=[],
        ):
            result, error = validate_openclaw_gateway_url(
                "https://machine.mycompany.ts.net"
            )

        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("public tailscale funnel url", error.lower())
        self.assertIn("tailnet-only", error.lower())

    def test_unresolvable_non_tailscale_tsnet_hostname_returns_generic_error(self):
        with patch(
            "mvp_site.settings_validation._resolve_gateway_host_ips",
            return_value=[],
        ):
            result, error = validate_openclaw_gateway_url("https://app.myats.net")

        self.assertIsNone(result)
        self.assertEqual(error, "Invalid OpenClaw gateway URL - cannot resolve hostname")


class TestValidateOpenClawGatewayPort(unittest.TestCase):
    """Tests for validate_openclaw_gateway_port function."""

    def test_valid_integer_port(self):
        result, error = validate_openclaw_gateway_port(18789)

        self.assertEqual(result, 18789)
        self.assertIsNone(error)

    def test_valid_numeric_string_port(self):
        result, error = validate_openclaw_gateway_port("18790")

        self.assertEqual(result, 18790)
        self.assertIsNone(error)

    def test_rejects_out_of_range_port(self):
        result, error = validate_openclaw_gateway_port(70000)

        self.assertIsNone(result)
        self.assertIn("Invalid OpenClaw gateway port", error)

    def test_rejects_non_numeric_port(self):
        result, error = validate_openclaw_gateway_port("abc")

        self.assertIsNone(result)
        self.assertIn("must be numeric", error)


class TestOpenClawUIContract(unittest.TestCase):
    """UI contract checks for OpenClaw settings controls."""

    def test_settings_template_contains_openclaw_gateway_port_input(self):
        template_path = Path("mvp_site/templates/settings.html")
        html = template_path.read_text(encoding="utf-8")

        self.assertIn('id="openclawGatewayPort"', html)
        self.assertIn('name="openclawGatewayPort"', html)
        self.assertIn('max="65535"', html)

    def test_settings_schema_contains_openclaw_gateway_port_key(self):
        settings_js_path = Path("mvp_site/frontend_v1/js/settings.js")
        js = settings_js_path.read_text(encoding="utf-8")

        self.assertIn('key: "openclaw_gateway_port"', js)
        self.assertIn('id: "openclawGatewayPort"', js)


if __name__ == "__main__":
    unittest.main()
