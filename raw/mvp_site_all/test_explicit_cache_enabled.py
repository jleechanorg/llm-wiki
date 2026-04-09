"""
TDD guard for explicit_cache_enabled in llm_service.py.

REV-5ix: explicit_cache_enabled was disabled (False) blocking all Gemini context
cache usage. DICE-s8u fix already adds code_execution tool into the cache itself,
resolving the Gemini API constraint. This test asserts the cache path is active.

Layer 1 unit test — no server required.
"""

from __future__ import annotations

import os
import unittest
from unittest.mock import MagicMock, patch

from mvp_site import constants, llm_service
from mvp_site.llm_request import LLMRequest


def _make_gemini_request_with_campaign() -> LLMRequest:
    """Minimal LLMRequest that satisfies the explicit-cache routing conditions."""
    return LLMRequest(
        user_action="test action",
        game_mode="character",
        user_id="test-user-id",
        game_state={"campaign_id": "test-campaign-123", "player": {"level": 1}},
        story_history=[{"role": "user", "content": "hello"}],
    )


class TestExplicitCacheEnabled(unittest.TestCase):
    """Assert that the explicit cache code path is active (not disabled)."""

    @patch("mvp_site.llm_service._call_llm_api_with_explicit_cache")
    @patch("mvp_site.llm_service._get_user_api_key_for_provider", return_value=None)
    def test_explicit_cache_path_is_entered_for_gemini_with_campaign(
        self, _mock_key, mock_cache_fn
    ):
        """When provider=gemini and game_state has campaign_id + story_history,
        _call_llm_api_with_explicit_cache must be called.

        FAILS when explicit_cache_enabled = False (cache is dead code).
        PASSES when explicit_cache_enabled = True (cache path is live).
        """
        mock_cache_fn.return_value = MagicMock()

        req = _make_gemini_request_with_campaign()
        llm_service._call_llm_api_with_llm_request(
            gemini_request=req,
            model_name="gemini-3-flash-preview",
            provider_name=constants.LLM_PROVIDER_GEMINI,
        )

        self.assertTrue(
            mock_cache_fn.called,
            "explicit_cache_enabled must be True so the cache path is reached. "
            "Check llm_service.py: 'explicit_cache_enabled = True'"
        )
        mock_cache_fn.assert_called_once()


class TestThinkModePassedToCachePath(unittest.TestCase):
    """REV-9r8: is_think_mode must propagate through the explicit cache path."""

    @patch("mvp_site.llm_service._call_llm_api_with_explicit_cache")
    @patch("mvp_site.llm_service._get_user_api_key_for_provider", return_value=None)
    def test_think_mode_forwarded_to_cache_function(self, _mock_key, mock_cache_fn):
        """is_think_mode=True must be passed to _call_llm_api_with_explicit_cache."""
        mock_cache_fn.return_value = MagicMock()

        req = _make_gemini_request_with_campaign()
        llm_service._call_llm_api_with_llm_request(
            gemini_request=req,
            model_name="gemini-3-flash-preview",
            provider_name=constants.LLM_PROVIDER_GEMINI,
            is_think_mode=True,
        )

        mock_cache_fn.assert_called_once()
        call_kwargs = mock_cache_fn.call_args
        self.assertTrue(
            call_kwargs.kwargs.get("is_think_mode", False),
            "is_think_mode=True must be forwarded to cache path"
        )


class TestForceToolModePassedToCachePath(unittest.TestCase):
    """REV-8fh: force_tool_mode must propagate through the explicit cache path."""

    @patch("mvp_site.llm_service._call_llm_api")
    @patch("mvp_site.llm_service.get_cache_manager")
    @patch("mvp_site.llm_service.gemini_provider")
    @patch("mvp_site.llm_service.build_full_content_for_retry", return_value="full")
    @patch("mvp_site.llm_service.apply_code_execution_system_instruction", return_value="sys")
    def test_force_tool_mode_forwarded_on_cache_create_fallback(
        self, _mock_apply, _mock_retry, mock_provider, mock_get_mgr, mock_call_api
    ):
        """When cache creation fails and falls back, force_tool_mode must be preserved."""
        mock_call_api.return_value = MagicMock()

        mock_mgr = MagicMock()
        mock_mgr.has_pending_cache.return_value = False
        mock_mgr.should_rebuild.return_value = True
        mock_mgr.cached_entry_count = 0
        mock_mgr.REBUILD_THRESHOLD = 3
        mock_mgr.create_cache.side_effect = Exception("InvalidArgument: cache failed")
        mock_get_mgr.return_value = mock_mgr

        mock_provider.get_client.return_value = MagicMock()

        req = _make_gemini_request_with_campaign()
        llm_service._call_llm_api_with_explicit_cache(
            gemini_request=req,
            campaign_id="test-campaign-123",
            model_name="gemini-3-flash-preview",
            force_tool_mode="ANY",
        )

        call_kwargs = mock_call_api.call_args
        self.assertEqual(
            call_kwargs.kwargs.get("force_tool_mode"),
            "ANY",
            "force_tool_mode must be forwarded on cache create fallback"
        )


class TestPendingCacheDeletedRemotely(unittest.TestCase):
    """REV-dlt: reset_cache must delete pending cache remotely before clearing."""

    def test_pending_cache_deleted_on_reset(self):
        from mvp_site.gemini_cache_manager import CampaignCacheManager

        mgr = CampaignCacheManager("test-campaign")
        mgr.cache_name = "caches/active-123"
        mgr._pending_cache_name = "caches/pending-456"
        mgr._pending_entry_count = 5
        mgr._pending_has_code_execution = True

        mock_client = MagicMock()
        mgr.reset_cache(client=mock_client)

        delete_calls = mock_client.caches.delete.call_args_list
        deleted_names = [call.kwargs.get("name") or call.args[0] for call in delete_calls]
        self.assertIn(
            "caches/pending-456",
            deleted_names,
            "Pending cache must be deleted remotely during reset"
        )


class TestUserIdPassedOnCacheHappyPath(unittest.TestCase):
    """cursor[bot]: user_id missing from happy-path _call_llm_api calls."""

    @patch("mvp_site.llm_service._call_llm_api")
    @patch("mvp_site.llm_service.get_cache_manager")
    @patch("mvp_site.llm_service.gemini_provider")
    @patch("mvp_site.llm_service.build_full_content_for_retry", return_value="full")
    @patch("mvp_site.llm_service.apply_code_execution_system_instruction", return_value="sys")
    def test_user_id_passed_on_cache_reuse(
        self, _mock_apply, _mock_retry, mock_provider, mock_get_mgr, mock_call_api
    ):
        """user_id must be passed to _call_llm_api on cache REUSE happy path."""
        mock_call_api.return_value = MagicMock()

        mock_mgr = MagicMock()
        mock_mgr.has_pending_cache.return_value = False
        mock_mgr.should_rebuild.return_value = False
        mock_mgr.get_cache_name.return_value = "caches/existing-789"
        mock_mgr.cached_entry_count = 1
        mock_get_mgr.return_value = mock_mgr

        req = _make_gemini_request_with_campaign()
        llm_service._call_llm_api_with_explicit_cache(
            gemini_request=req,
            campaign_id="test-campaign-123",
            model_name="gemini-3-flash-preview",
            user_id="test-user-42",
        )

        call_kwargs = mock_call_api.call_args
        self.assertEqual(
            call_kwargs.kwargs.get("user_id"),
            "test-user-42",
            "user_id must be passed to _call_llm_api on cache reuse happy path"
        )


class TestForcedExplicitCacheMissHook(unittest.TestCase):
    """REV-wt1: FORCE_EXPLICIT_CACHE_MISS return value must be honored by callers."""

    @patch("mvp_site.llm_service._call_llm_api")
    @patch("mvp_site.llm_service.get_cache_manager")
    @patch("mvp_site.llm_service.gemini_provider")
    @patch("mvp_site.llm_service.build_full_content_for_retry", return_value="full-retry")
    def test_forced_cache_miss_retries_without_cache(
        self, _mock_retry, mock_provider, mock_get_mgr, mock_call_api
    ):
        mock_mgr = MagicMock()
        mock_mgr.has_pending_cache.return_value = False
        mock_mgr.should_rebuild.return_value = False
        mock_mgr.get_cache_name.return_value = "caches/existing-789"
        mock_mgr.cached_entry_count = 1
        mock_get_mgr.return_value = mock_mgr
        mock_provider.get_client.return_value = MagicMock()

        cached_response = MagicMock()
        cached_response.usage_metadata.cached_content_token_count = 100
        retry_response = MagicMock()
        mock_call_api.side_effect = [cached_response, retry_response]

        req = _make_gemini_request_with_campaign()
        previous = os.environ.get("FORCE_EXPLICIT_CACHE_MISS")
        os.environ["FORCE_EXPLICIT_CACHE_MISS"] = "true"
        try:
            result = llm_service._call_llm_api_with_explicit_cache(
                gemini_request=req,
                campaign_id="test-campaign-123",
                model_name="gemini-3-flash-preview",
            )
        finally:
            if previous is None:
                os.environ.pop("FORCE_EXPLICIT_CACHE_MISS", None)
            else:
                os.environ["FORCE_EXPLICIT_CACHE_MISS"] = previous

        self.assertIs(result, retry_response)
        self.assertEqual(mock_call_api.call_count, 2)
        first_call = mock_call_api.call_args_list[0].kwargs
        second_call = mock_call_api.call_args_list[1].kwargs
        self.assertEqual(first_call.get("cache_name"), "caches/existing-789")
        self.assertIsNone(second_call.get("cache_name"))


class TestPhase2OrchestrationKeepsSystemInstruction(unittest.TestCase):
    """cursor[bot] HIGH: Phase 2 orchestration must keep dynamic phase2_system_instruction."""

    @patch("mvp_site.llm_service.gemini_provider")
    @patch("mvp_site.llm_service.build_tool_results_prompt", return_value="tool results")
    @patch("mvp_site.llm_service._build_gemini_two_phase_history", return_value=["history"])
    @patch("mvp_site.llm_service.format_tool_results_text", return_value="combined")
    @patch("mvp_site.llm_service.build_domain_tool_request_enforcement", return_value=("", []))
    @patch("mvp_site.llm_service.execute_gemini_code_execution_tool_orchestration")
    @patch("mvp_site.llm_service.extract_json_payload_and_tool_requests", return_value=({}, []))
    @patch("mvp_site.llm_service._get_text_from_response", return_value="phase1 text")
    @patch("mvp_site.llm_service.get_prompt_tool_context")
    @patch("mvp_site.llm_service.update_prompt_contents_with_tool_results", return_value=["updated"])
    def test_phase2_system_instruction_not_suppressed_by_cache(
        self, _mock_update, mock_ctx, _mock_text, _mock_extract, mock_orch,
        _mock_enforce, _mock_fmt, _mock_history, _mock_prompt, mock_provider
    ):
        """phase2_system_instruction must be passed even when cache_name is set."""
        mock_ctx.return_value = {
            "is_enabling": False,
            "allow_domain_tools": False,
            "turn_number": 3,
        }
        mock_orch.return_value = [{"tool": "roll_dice", "result": "15"}]
        mock_response = MagicMock()
        mock_provider.generate_json_mode_content.return_value = mock_response
        mock_provider.apply_code_execution_system_instruction.return_value = "phase2-dynamic-instruction"

        llm_service._orchestrate_gemini_code_execution_tool_requests(
            prompt_contents=["test prompt"],
            response_1=MagicMock(),
            model_name="gemini-3-flash-preview",
            system_instruction_text="original instruction",
            temperature=0.8,
            safety_settings=[],
            json_mode_max_output_tokens=8192,
            cache_name="caches/active-123",
            user_api_key=None,
        )

        call_kwargs = mock_provider.generate_json_mode_content.call_args
        self.assertIsNotNone(
            call_kwargs.kwargs.get("system_instruction_text"),
            "phase2_system_instruction must NOT be suppressed when cache_name is set"
        )


if __name__ == "__main__":
    unittest.main()
