from __future__ import annotations

import logging
import unittest
from unittest.mock import patch

from mvp_site.llm_providers.openai_compatible_provider_core import (
    generate_openai_compatible_content,
)


class TestOpenAICompatibleProviderCore(unittest.TestCase):
    def test_generates_payload_with_response_format_when_no_tools(self):
        seen = {}

        def fake_post(
            *, url, headers, payload, timeout, logger=None, error_log_prefix=""
        ):
            seen["url"] = url
            seen["headers"] = headers
            seen["payload"] = payload
            return {"choices": [{"message": {"content": '{"narrative":"ok"}'}}]}

        with patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.post_chat_completions",
            new=fake_post,
        ):
            text, raw = generate_openai_compatible_content(
                url="http://x",
                headers={"a": "b"},
                model_name="m",
                prompt_contents=["hi"],
                system_instruction_text="sys",
                temperature=0.0,
                max_output_tokens=10,
                stringify_chat_parts_fn=lambda parts: "\n\n".join(parts),
                tools=None,
                response_format={"type": "json_object"},
            )

        self.assertEqual(text, '{"narrative":"ok"}')
        self.assertIn("response_format", seen["payload"])
        self.assertNotIn("tools", seen["payload"])
        self.assertEqual(raw["choices"][0]["message"]["content"], '{"narrative":"ok"}')

    def test_generates_payload_with_tools_and_tool_choice(self):
        seen = {}

        def fake_post(
            *, url, headers, payload, timeout, logger=None, error_log_prefix=""
        ):
            seen["payload"] = payload
            return {
                "choices": [{"message": {"content": None, "tool_calls": [{"id": "1"}]}}]
            }

        with patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.post_chat_completions",
            new=fake_post,
        ):
            text, _raw = generate_openai_compatible_content(
                url="http://x",
                headers={"a": "b"},
                model_name="m",
                prompt_contents=["hi"],
                system_instruction_text=None,
                temperature=0.0,
                max_output_tokens=10,
                stringify_chat_parts_fn=lambda parts: "\n\n".join(parts),
                tools=[{"type": "function", "function": {"name": "roll_dice"}}],
                tool_choice="required",
                response_format={"type": "json_object"},
            )

        # Content can be absent if tool_calls exist
        self.assertEqual(text, "")
        self.assertIn("tools", seen["payload"])
        self.assertIn("tool_choice", seen["payload"])
        self.assertNotIn("response_format", seen["payload"])

    def test_raises_when_no_content_and_no_tool_calls(self):
        def fake_post(
            *, url, headers, payload, timeout, logger=None, error_log_prefix=""
        ):
            return {"choices": [{"message": {"content": None}}]}

        with patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.post_chat_completions",
            new=fake_post,
        ):
            with self.assertRaises(ValueError):
                generate_openai_compatible_content(
                    url="http://x",
                    headers={"a": "b"},
                    model_name="m",
                    prompt_contents=["hi"],
                    system_instruction_text=None,
                    temperature=0.0,
                    max_output_tokens=10,
                    stringify_chat_parts_fn=lambda parts: "\n\n".join(parts),
                    tools=None,
                    response_format={"type": "json_object"},
                )

    def test_custom_validator_can_override_default(self):
        def fake_post(
            *, url, headers, payload, timeout, logger=None, error_log_prefix=""
        ):
            return {
                "choices": [{"message": {"content": None}}],
                "usage": {"prompt_tokens": 1},
            }

        def validator(_data, _message, _raw_text, _tool_calls):
            # Allow missing content (provider will handle it elsewhere)
            return None

        with patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.post_chat_completions",
            new=fake_post,
        ):
            text, _raw = generate_openai_compatible_content(
                url="http://x",
                headers={"a": "b"},
                model_name="m",
                prompt_contents=["hi"],
                system_instruction_text=None,
                temperature=0.0,
                max_output_tokens=10,
                stringify_chat_parts_fn=lambda parts: "\n\n".join(parts),
                tools=None,
                response_format={"type": "json_object"},
                validate_response_fn=validator,
            )
        self.assertEqual(text, "")

    def test_logs_response_body_when_choices_missing(self):
        """TDD: When API returns error body (no choices), log the full response."""
        logged_errors = []

        class FakeLogger:
            def error(self, msg):
                logged_errors.append(msg)

            def info(self, msg):
                pass

        def fake_post(
            *, url, headers, payload, timeout, logger=None, error_log_prefix=""
        ):
            # Simulate OpenRouter returning error in body (200 OK, no choices)
            return {"error": {"message": "Model unavailable", "code": 503}}

        with patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.post_chat_completions",
            new=fake_post,
        ):
            with self.assertRaises(ValueError) as ctx:
                generate_openai_compatible_content(
                    url="http://x",
                    headers={"a": "b"},
                    model_name="test-model",
                    prompt_contents=["hi"],
                    system_instruction_text=None,
                    temperature=0.0,
                    max_output_tokens=10,
                    stringify_chat_parts_fn=lambda parts: "\n\n".join(parts),
                    tools=None,
                    response_format={"type": "json_object"},
                    logger=FakeLogger(),
                    error_log_prefix="TEST",
                )

            # Error should be raised
            self.assertIn("missing choices[0]", str(ctx.exception))

        # Verify the response body is logged for debugging
        self.assertTrue(
            any("Model unavailable" in msg for msg in logged_errors),
            f"Expected response body to be logged. Got: {logged_errors}",
        )
        # Verify log message includes exception details
        self.assertTrue(
            any(
                "API parsing error" in msg and "missing choices[0]" in msg
                for msg in logged_errors
            ),
            f"Expected log to include exception message. Got: {logged_errors}",
        )

    def test_logs_response_body_with_fallback_when_json_dumps_fails(self):
        """When json.dumps fails, fall back to str() for response logging."""
        logged_errors = []

        class FakeLogger:
            def error(self, msg):
                logged_errors.append(msg)

            def info(self, msg):
                pass

        class NonSerializable:
            """Object that can't be JSON serialized but has a str representation."""

            def __str__(self):
                return "NonSerializable(error_info)"

        def fake_post(
            *, url, headers, payload, timeout, logger=None, error_log_prefix=""
        ):
            # Return response with non-serializable value
            return {"bad_key": NonSerializable(), "choices": []}

        with patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.post_chat_completions",
            new=fake_post,
        ):
            with self.assertRaises(ValueError):
                generate_openai_compatible_content(
                    url="http://x",
                    headers={"a": "b"},
                    model_name="test-model",
                    prompt_contents=["hi"],
                    system_instruction_text=None,
                    temperature=0.0,
                    max_output_tokens=10,
                    stringify_chat_parts_fn=lambda parts: "\n\n".join(parts),
                    tools=None,
                    response_format={"type": "json_object"},
                    logger=FakeLogger(),
                    error_log_prefix="TEST",
                )

        # Should have logged using str() fallback
        self.assertTrue(
            len(logged_errors) > 0,
            "Expected error to be logged even when json.dumps fails",
        )

    def test_logging_failure_does_not_mask_original_error(self):
        """If logger.error() raises, original ValueError should still propagate."""

        class BrokenLogger:
            def error(self, msg):
                raise RuntimeError("Logger broken!")

            def info(self, msg):
                pass

        def fake_post(
            *, url, headers, payload, timeout, logger=None, error_log_prefix=""
        ):
            return {"error": {"message": "Model unavailable", "code": 503}}

        with patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.post_chat_completions",
            new=fake_post,
        ):
            # Should raise ValueError, NOT RuntimeError from broken logger
            with self.assertRaises(ValueError) as ctx:
                generate_openai_compatible_content(
                    url="http://x",
                    headers={"a": "b"},
                    model_name="test-model",
                    prompt_contents=["hi"],
                    system_instruction_text=None,
                    temperature=0.0,
                    max_output_tokens=10,
                    stringify_chat_parts_fn=lambda parts: "\n\n".join(parts),
                    tools=None,
                    response_format={"type": "json_object"},
                    logger=BrokenLogger(),
                    error_log_prefix="TEST",
                )

            # Original error should be preserved
            self.assertIn("missing choices[0]", str(ctx.exception))

    def test_logs_finish_reason_and_usage_when_logger_provided(self):
        """Test that finish_reason and token usage are logged via logging_util."""
        logged_info: list[str] = []

        def fake_post(
            *, url, headers, payload, timeout, logger=None, error_log_prefix=""
        ):
            return {
                "choices": [
                    {
                        "message": {"content": '{"narrative":"ok"}'},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 100, "completion_tokens": 50},
            }

        with patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.post_chat_completions",
            new=fake_post,
        ), patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.logging_util"
        ) as mock_lu:
            mock_lu.info.side_effect = lambda msg, **_kw: logged_info.append(msg)
            mock_lu.warning.side_effect = lambda msg, **_kw: logged_info.append(msg)

            text, raw = generate_openai_compatible_content(
                url="http://x",
                headers={"a": "b"},
                model_name="m",
                prompt_contents=["hi"],
                system_instruction_text="sys",
                temperature=0.0,
                max_output_tokens=10,
                stringify_chat_parts_fn=lambda parts: "\n\n".join(parts),
                tools=None,
                response_format={"type": "json_object"},
                logger=logging.getLogger("test"),
            )

        self.assertEqual(text, '{"narrative":"ok"}')
        self.assertTrue(
            any("finish_reason=stop" in msg for msg in logged_info),
            f"Expected finish_reason logged. Got: {logged_info}",
        )
        self.assertTrue(
            any("prompt_tokens=100" in msg for msg in logged_info),
            f"Expected prompt_tokens logged. Got: {logged_info}",
        )
        # finish_reason=stop should NOT trigger the RESPONSE_TRUNCATED warning
        self.assertFalse(
            any("RESPONSE_TRUNCATED" in msg for msg in logged_info),
            f"Unexpected truncation warning. Got: {logged_info}",
        )

    def test_logs_truncation_warning_when_finish_reason_is_length(self):
        """Test that finish_reason=length triggers RESPONSE_TRUNCATED warning."""
        logged_msgs: list[str] = []

        def fake_post(
            *, url, headers, payload, timeout, logger=None, error_log_prefix=""
        ):
            return {
                "choices": [
                    {
                        "message": {"content": '{"narrative":"ok"}'},
                        "finish_reason": "length",
                    }
                ],
                "usage": {"prompt_tokens": 100, "completion_tokens": 4096},
            }

        with patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.post_chat_completions",
            new=fake_post,
        ), patch(
            "mvp_site.llm_providers.openai_compatible_provider_core.logging_util"
        ) as mock_lu:
            mock_lu.info.side_effect = lambda msg, **_kw: logged_msgs.append(msg)
            mock_lu.warning.side_effect = lambda msg, **_kw: logged_msgs.append(msg)

            text, raw = generate_openai_compatible_content(
                url="http://x",
                headers={"a": "b"},
                model_name="m",
                prompt_contents=["hi"],
                system_instruction_text="sys",
                temperature=0.0,
                max_output_tokens=4096,
                stringify_chat_parts_fn=lambda parts: "\n\n".join(parts),
                tools=None,
                response_format={"type": "json_object"},
                logger=logging.getLogger("test"),
                error_log_prefix="GROK",
            )

        self.assertTrue(
            any("RESPONSE_TRUNCATED" in msg and "finish_reason=length" in msg for msg in logged_msgs),
            f"Expected RESPONSE_TRUNCATED warning. Got: {logged_msgs}",
        )
        self.assertTrue(
            any("GROK" in msg for msg in logged_msgs),
            f"Expected error_log_prefix in messages. Got: {logged_msgs}",
        )
