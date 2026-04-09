from datetime import datetime, timezone
import inspect
import unittest
from unittest.mock import MagicMock, patch

from mvp_site import llm_service, constants
from mvp_site.llm_response import LLMResponse


class TestLLMServiceContext(unittest.TestCase):
    """Test context extraction logic in llm_service."""

    @patch("mvp_site.llm_service._call_llm_api_with_llm_request")
    @patch("mvp_site.llm_service.get_agent_for_input")
    def test_continue_story_extracts_last_ai_response(self, mock_get_agent, mock_call_llm):
        """Verify continue_story extracts and passes last AI response correctly."""
        # Setup mocks
        mock_game_state = MagicMock()
        mock_game_state.player_turn = 5 # Set explicit turn number to avoid TypeError
        # Prevent RecursionError by making to_dict() return a simple dict instead of Mock
        mock_game_state.to_dict.return_value = {"player_turn": 5, "campaign_id": "test"}
        # Prevent checkpoint validation from causing issues
        mock_game_state.validate_checkpoint_consistency.return_value = []
        mock_agent = MagicMock()
        mock_get_agent.return_value = (mock_agent, {})

        # Mock the LLM API call to return a proper LLMResponse object
        mock_llm_response = LLMResponse(
            narrative_text="Test response",
            structured_response=None
        )
        mock_call_llm.return_value = mock_llm_response

        # Test data with multiple story entries
        story_context = [
            # Oldest
            {constants.KEY_ACTOR: constants.ACTOR_GEMINI, constants.KEY_TEXT: "Old text"},
            {constants.KEY_ACTOR: constants.ACTOR_USER, constants.KEY_TEXT: "User action"},
            {constants.KEY_ACTOR: constants.ACTOR_GEMINI, constants.KEY_TEXT: "Recent AI response"},
            {constants.KEY_ACTOR: constants.ACTOR_USER, constants.KEY_TEXT: "Current action"},
            # Newest
        ]

        # Call continue_story
        llm_service.continue_story(
            "Current action",
            "test-user",
            story_context=story_context,
            current_game_state=mock_game_state
        )

        # Verify get_agent_for_input was called with the correct context
        # It should find the MOST RECENT entry where actor is gemini
        mock_get_agent.assert_called_with(
            "Current action",
            mock_game_state,
            "test-user", # mode parameter
            last_ai_response="Recent AI response"
        )

    def test_continue_story_streaming_uses_shared_preparation_helper(self):
        """Phase 1 contract: streaming path must share preparation with continue_story."""
        source = inspect.getsource(llm_service.continue_story_streaming)

        assert "prepared = _prepare_story_continuation(" in source, (
            "continue_story_streaming must call _prepare_story_continuation()"
        )
        assert "requires_action_resolution=prepared.agent.requires_action_resolution" in source, (
            "streaming parse path must use prepared agent settings"
        )

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.execute_tool_requests", create=True)
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_emits_tool_and_state_events(
        self,
        mock_prepare,
        mock_stream,
        mock_execute_tools,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """Streaming path should emit tool_start/tool_result/state events when tool requests exist."""
        prepared = MagicMock()
        prepared.model_to_use = "gemini-2.5-flash"
        prepared.provider_selection.provider = constants.LLM_PROVIDER_GEMINI
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = 0.7
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096

        # Phase 1 chunk then phase 2 chunk
        mock_stream.side_effect = [iter(['{"phase":"one"}']), iter(['{"phase":"two"}'])]

        phase1 = MagicMock()
        phase1.tool_requests = [{"tool": "roll_dice", "args": {"notation": "1d20"}}]
        phase1.state_updates = {}
        phase2 = MagicMock()
        phase2.tool_requests = []
        phase2.state_updates = {"hp": {"current": 18}}
        mock_parse.side_effect = [("phase one narrative", phase1), ("phase two narrative", phase2)]

        mock_execute_tools.return_value = [
            {"tool": "roll_dice", "args": {"notation": "1d20"}, "result": {"total": 14}}
        ]

        events = list(
            llm_service.continue_story_streaming(
                user_input="attack",
                mode="character",
                story_context=[],
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        event_types = [e.type for e in events]
        self.assertIn("tool_start", event_types)
        self.assertIn("tool_result", event_types)
        self.assertIn("state", event_types)
        self.assertEqual(event_types[-1], "done")

        tool_start = next(e for e in events if e.type == "tool_start")
        self.assertEqual(tool_start.payload["tool_name"], "roll_dice")

        state_event = next(e for e in events if e.type == "state")
        self.assertEqual(state_event.payload, {"hp": {"current": 18}})

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_uses_json_mode_for_streaming_calls(
        self,
        mock_prepare,
        mock_stream,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """Both phase calls should request JSON mode for structured streaming output."""
        prepared = MagicMock()
        prepared.model_to_use = "gemini-2.5-flash"
        prepared.provider_selection.provider = constants.LLM_PROVIDER_GEMINI
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = 0.7
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096

        mock_stream.return_value = iter(['{"narrative":"ok"}'])
        parsed = MagicMock()
        parsed.tool_requests = []
        parsed.state_updates = {}
        mock_parse.return_value = ("ok", parsed)

        list(
            llm_service.continue_story_streaming(
                user_input="look around",
                mode="character",
                story_context=[],
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        self.assertGreaterEqual(mock_stream.call_count, 1)
        for call in mock_stream.call_args_list:
            self.assertIn("json_mode", call.kwargs)
            self.assertTrue(call.kwargs["json_mode"])

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.execute_tool_requests", create=True)
    @patch("mvp_site.llm_service._get_user_api_key_for_provider")
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_phase2_uses_json_mode_for_character_mode(
        self,
        mock_prepare,
        mock_stream,
        mock_lookup_key,
        mock_execute_tools,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """Phase 2 streaming should continue using JSON mode for character-mode outputs."""
        prepared = MagicMock()
        prepared.model_to_use = "gemini-2.5-flash"
        prepared.provider_selection.provider = constants.LLM_PROVIDER_GEMINI
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = 0.7
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        prepared.agent.MODE = "character"
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        prepared.is_god_mode_command = False  # Required for schema enforcement assertions
        prepared.user_id = "u1"
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096
        mock_lookup_key.return_value = "test-user-key"

        mock_stream.side_effect = [
            iter(['{"narrative":"phase one","tool_requests":[{"tool":"roll_dice","args":{"notation":"1d20"}}]}']),
            iter(['{"narrative":"phase two"}']),
        ]

        phase1 = MagicMock()
        phase1.tool_requests = [{"tool": "roll_dice", "args": {"notation": "1d20"}}]
        phase1.state_updates = {}
        phase2 = MagicMock()
        phase2.tool_requests = []
        phase2.state_updates = {}
        mock_parse.side_effect = [("phase one", phase1), ("phase two", phase2)]
        mock_execute_tools.return_value = [
            {"tool": "roll_dice", "args": {"notation": "1d20"}, "result": {"total": 14}}
        ]

        list(
            llm_service.continue_story_streaming(
                user_input="attack",
                mode="character",
                story_context=[],
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        self.assertEqual(mock_stream.call_count, 2)
        for call in mock_stream.call_args_list:
            self.assertEqual(call.kwargs.get("json_mode"), True)
        self.assertEqual(mock_parse.call_count, 2)

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.gemini_provider.get_client")
    @patch("mvp_site.llm_service.execute_tool_requests", create=True)
    @patch("mvp_site.llm_service._get_user_api_key_for_provider")
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service.get_cache_manager")
    @patch("mvp_site.llm_service._is_mock_services_mode", return_value=False)
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_passes_cache_name_and_suppresses_system_instruction(
        self,
        mock_prepare,
        mock_is_mock,
        mock_get_cache_manager,
        mock_stream,
        mock_lookup_key,
        mock_execute_tools,
        mock_get_client,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """Streaming cache path should pass cache_name and omit system instruction."""
        prepared = MagicMock()
        prepared.model_to_use = "gemini-2.5-flash"
        prepared.provider_selection.provider = constants.LLM_PROVIDER_GEMINI
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = 0.7
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        gemini_request = MagicMock()
        gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        gemini_request.game_state = {"campaign_id": "c1"}
        gemini_request.story_history = [{"sequence_id": 1}, {"sequence_id": 2}]
        gemini_request.to_explicit_cache_parts.return_value = (
            {"story_history": [{"sequence_id": 1}]},
            {"story_history": [{"sequence_id": 2}]},
        )
        prepared.gemini_request = gemini_request
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096
        mock_lookup_key.return_value = "test-user-key"
        mock_get_client.return_value = MagicMock()

        mock_mgr = MagicMock()
        mock_mgr.has_pending_cache.return_value = False
        mock_mgr.should_rebuild.return_value = False
        mock_mgr.get_cache_name.return_value = "cachedContents/stream-cache-1"
        mock_mgr.cached_entry_count = 1
        mock_get_cache_manager.return_value = mock_mgr

        mock_stream.return_value = iter(['{"narrative":"ok"}'])

        phase1 = MagicMock()
        phase1.tool_requests = []
        phase1.state_updates = {}
        mock_parse.return_value = ("ok", phase1)
        mock_execute_tools.return_value = []

        list(
            llm_service.continue_story_streaming(
                user_input="attack",
                mode="character",
                story_context=[],
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        self.assertEqual(mock_lookup_key.call_count, 1)
        self.assertEqual(len(mock_stream.call_args_list), 1)
        stream_call = mock_stream.call_args_list[0]
        self.assertEqual(stream_call.kwargs.get("api_key"), "test-user-key")
        self.assertEqual(
            stream_call.kwargs.get("cache_name"),
            "cachedContents/stream-cache-1",
        )
        self.assertIsNone(stream_call.kwargs.get("system_instruction_text"))
        prompt_blob = stream_call.kwargs["prompt_contents"][0]
        self.assertIn('"sequence_id": 1', prompt_blob)
        self.assertIn('"sequence_id": 2', prompt_blob)

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.execute_tool_requests", create=True)
    @patch("mvp_site.llm_service._get_user_api_key_for_provider")
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service._build_mock_streaming_text")
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_phase2_uses_real_provider_when_not_mocked(
        self,
        mock_prepare,
        mock_build_mock_text,
        mock_stream,
        mock_lookup_key,
        mock_execute_tools,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """Phase 2 should call provider stream in real mode, even after tool execution."""
        prepared = MagicMock()
        prepared.model_to_use = "gemini-2.5-flash"
        prepared.provider_selection.provider = constants.LLM_PROVIDER_GEMINI
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = 0.7
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        prepared.is_god_mode_command = False
        prepared.user_id = "u1"
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096
        mock_lookup_key.return_value = "test-user-key"
        mock_build_mock_text.return_value = "mock text should never be used"

        mock_stream.side_effect = [
            iter([
                '{"narrative":"phase one","tool_requests":[{"tool":"roll_dice",'
                '"args":{"notation":"1d20"}}]}'
            ]),
            iter([
                '{"narrative":"phase two","state_updates":{}}'
            ]),
        ]
        phase1 = MagicMock()
        phase1.tool_requests = [{"tool": "roll_dice", "args": {"notation": "1d20"}}]
        phase1.state_updates = {}
        phase2 = MagicMock()
        phase2.tool_requests = []
        phase2.state_updates = {}
        mock_parse.side_effect = [("phase one", phase1), ("phase two", phase2)]
        mock_execute_tools.return_value = [
            {"tool": "roll_dice", "args": {"notation": "1d20"}, "result": {"total": 14}}
        ]

        with patch.dict(
            "mvp_site.llm_service.os.environ", {"MOCK_SERVICES_MODE": "false"}, clear=False
        ):
            list(
                llm_service.continue_story_streaming(
                    user_input="attack",
                    mode="character",
                    story_context=[],
                    current_game_state=MagicMock(),
                    user_id="u1",
                    campaign_id="c1",
                )
            )

        self.assertEqual(mock_stream.call_count, 2)
        self.assertEqual(mock_build_mock_text.call_count, 0)

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_done_payload_includes_state_updates(
        self,
        mock_prepare,
        mock_stream,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """Done payload should include state_updates for frontend parity with non-streaming."""
        prepared = MagicMock()
        prepared.model_to_use = "gemini-2.5-flash"
        prepared.provider_selection.provider = constants.LLM_PROVIDER_GEMINI
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = 0.7
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096

        mock_stream.return_value = iter(['{"narrative":"ok"}'])
        parsed = MagicMock()
        parsed.tool_requests = []
        parsed.state_updates = {"player_health": 17}
        mock_parse.return_value = ("ok", parsed)

        events = list(
            llm_service.continue_story_streaming(
                user_input="look around",
                mode="character",
                story_context=[],
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        done_event = next(e for e in events if e.type == "done")
        self.assertIn("state_updates", done_event.payload)
        self.assertEqual(done_event.payload["state_updates"], {"player_health": 17})

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_done_payload_includes_user_scene_number(
        self,
        mock_prepare,
        mock_stream,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """Done payload should include user_scene_number for frontend Scene #X rendering parity."""
        prepared = MagicMock()
        prepared.model_to_use = "gemini-2.5-flash"
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = 0.7
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        prepared.agent.MODE = "character"
        prepared.provider_selection.provider = "gemini"
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096

        mock_stream.return_value = iter(['{"narrative":"ok"}'])
        parsed = MagicMock()
        parsed.tool_requests = []
        parsed.state_updates = {}
        mock_parse.return_value = ("ok", parsed)

        story_context = [
            {constants.KEY_ACTOR: constants.ACTOR_GEMINI, constants.KEY_TEXT: "AI 1"},
            {constants.KEY_ACTOR: constants.ACTOR_USER, constants.KEY_TEXT: "User 1"},
            {constants.KEY_ACTOR: constants.ACTOR_GEMINI, constants.KEY_TEXT: "AI 2"},
        ]

        events = list(
            llm_service.continue_story_streaming(
                user_input="look around",
                mode="character",
                story_context=story_context,
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        done_event = next(e for e in events if e.type == "done")
        # Two prior gemini entries => Scene #3 for this response
        self.assertEqual(done_event.payload.get("user_scene_number"), 3)

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_done_payload_includes_structured_response_data(
        self,
        mock_prepare,
        mock_stream,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """Done payload should include structured_response to match non-streaming data richness."""
        prepared = MagicMock()
        prepared.model_to_use = "gemini-2.5-flash"
        prepared.provider_selection.provider = constants.LLM_PROVIDER_GEMINI
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = 0.7
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096

        mock_stream.return_value = iter(['{"narrative":"ok"}'])
        parsed = MagicMock()
        parsed.tool_requests = []
        parsed.state_updates = {"player_health": 17}
        parsed.model_dump.return_value = {
            "narrative": "ok",
            "state_updates": {"player_health": 17},
        }
        mock_parse.return_value = ("ok", parsed)

        events = list(
            llm_service.continue_story_streaming(
                user_input="look around",
                mode="character",
                story_context=[],
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        done_event = next(e for e in events if e.type == "done")
        self.assertIn("structured_response", done_event.payload)
        self.assertEqual(done_event.payload["structured_response"]["narrative"], "ok")
        self.assertEqual(done_event.payload["execution_path"], "streaming")
        self.assertIn("streaming_cache", done_event.payload)
        self.assertEqual(
            done_event.payload["streaming_execution_trace"]["execution_path"],
            "streaming",
        )

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_uses_default_temperature_when_override_missing(
        self,
        mock_prepare,
        mock_stream,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """Streaming calls should use default TEMPERATURE when override is None."""
        prepared = MagicMock()
        prepared.model_to_use = "gemini-2.5-flash"
        prepared.provider_selection.provider = constants.LLM_PROVIDER_GEMINI
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = None
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096

        mock_stream.return_value = iter(['{"narrative":"ok"}'])
        parsed = MagicMock()
        parsed.tool_requests = []
        parsed.state_updates = {}
        mock_parse.return_value = ("ok", parsed)

        list(
            llm_service.continue_story_streaming(
                user_input="look around",
                mode="character",
                story_context=[],
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        self.assertGreaterEqual(mock_stream.call_count, 1)
        for call in mock_stream.call_args_list:
            self.assertEqual(call.kwargs["temperature"], llm_service.TEMPERATURE)

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_done_payload_includes_stream_start_time_and_e2e_latency(
        self,
        mock_prepare,
        mock_stream,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """Done payload must include stream_start_time (UTC ISO) and e2e_latency_seconds (float).

        stream_start_time lets clients display when the stream began.
        e2e_latency_seconds lets clients measure total round-trip duration.
        """
        prepared = MagicMock()
        prepared.model_to_use = "gemini-2.5-flash"
        prepared.provider_selection.provider = constants.LLM_PROVIDER_GEMINI
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = 0.7
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        prepared.agent.MODE = "character"
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096

        mock_stream.return_value = iter(['{"narrative":"ok"}'])
        parsed = MagicMock()
        parsed.tool_requests = []
        parsed.state_updates = {}
        mock_parse.return_value = ("ok", parsed)

        events = list(
            llm_service.continue_story_streaming(
                user_input="look around",
                mode="character",
                story_context=[],
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        done_event = next(e for e in events if e.type == "done")

        # stream_start_time must be a UTC ISO 8601 string
        self.assertIn("stream_start_time", done_event.payload)
        stream_start_time = done_event.payload["stream_start_time"]
        self.assertIsInstance(stream_start_time, str)
        # Must parse as a valid ISO 8601 datetime with UTC offset
        parsed_dt = datetime.fromisoformat(stream_start_time)
        self.assertEqual(parsed_dt.tzinfo, timezone.utc)

        # e2e_latency_seconds must be a non-negative float
        self.assertIn("e2e_latency_seconds", done_event.payload)
        e2e = done_event.payload["e2e_latency_seconds"]
        self.assertIsInstance(e2e, float)
        self.assertGreaterEqual(e2e, 0.0)

    @patch("mvp_site.llm_service._get_safe_output_token_limit")
    @patch("mvp_site.llm_service._calculate_prompt_and_system_tokens")
    @patch("mvp_site.llm_service.parse_structured_response")
    @patch("mvp_site.llm_service.openclaw_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service.gemini_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service.openrouter_provider.generate_content_stream_sync")
    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_routes_openrouter_provider(
        self,
        mock_prepare,
        mock_openrouter_stream,
        mock_gemini_stream,
        mock_openclaw_stream,
        mock_parse,
        mock_calc_tokens,
        mock_safe_limit,
    ):
        """OpenRouter should be accepted by streaming path and routed to OpenRouter provider."""
        prepared = MagicMock()
        prepared.model_to_use = "x-ai/grok-4.1-fast"
        prepared.provider_selection.provider = constants.LLM_PROVIDER_OPENROUTER
        prepared.system_instruction_final = "sys"
        prepared.temperature_override = 0.7
        prepared.agent.requires_action_resolution = True
        prepared.agent.__class__.__name__ = "StoryModeAgent"
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        mock_prepare.return_value = prepared
        mock_calc_tokens.return_value = (0, 0)
        mock_safe_limit.return_value = 4096

        mock_openrouter_stream.return_value = iter(['{"narrative":"ok"}'])
        parsed = MagicMock()
        parsed.tool_requests = []
        parsed.state_updates = {}
        mock_parse.return_value = ("ok", parsed)

        events = list(
            llm_service.continue_story_streaming(
                user_input="look around",
                mode="character",
                story_context=[],
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        self.assertEqual(mock_openrouter_stream.call_count, 1)
        self.assertEqual(mock_gemini_stream.call_count, 0)
        self.assertEqual(mock_openclaw_stream.call_count, 0)
        self.assertTrue(any(event.type == "done" for event in events))
        self.assertTrue(all(event.type != "error" for event in events))

    @patch("mvp_site.llm_service._prepare_story_continuation")
    def test_continue_story_streaming_rejects_unsupported_provider(self, mock_prepare):
        """Providers outside the streaming allowlist should return an unsupported-provider error."""
        prepared = MagicMock()
        prepared.provider_selection.provider = constants.LLM_PROVIDER_CEREBRAS
        prepared.gemini_request.to_json.return_value = {"message_type": "story_continuation"}
        mock_prepare.return_value = prepared

        events = list(
            llm_service.continue_story_streaming(
                user_input="look around",
                mode="character",
                story_context=[],
                current_game_state=MagicMock(),
                user_id="u1",
                campaign_id="c1",
            )
        )

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].type, "error")
        self.assertEqual(
            events[0].payload.get("error_type"), "streaming_unsupported_provider"
        )
        self.assertIn("cerebras", events[0].payload.get("message", ""))


if __name__ == "__main__":
    unittest.main()
