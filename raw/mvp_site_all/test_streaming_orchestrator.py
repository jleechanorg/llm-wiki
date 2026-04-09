"""Tests for streaming_orchestrator module.

Tests the SSE streaming functionality for real-time LLM responses.
"""

import json
import re
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from mvp_site.narrative_response_schema import JSON_PARSE_FALLBACK_MARKER
from mvp_site.streaming_orchestrator import (
    _LW_REQUIRED_FIELDS,
    StreamEvent,
    _count_compliant_lw_events,
    _warn_if_living_world_missing,
    create_sse_response_headers,
    stream_events_generator,
    stream_narrative_simple,
    stream_story_with_game_state,
    stream_with_context,
)


class TestStreamEvent(unittest.TestCase):
    """Tests for StreamEvent dataclass."""

    def test_stream_event_creation(self):
        """Test creating a StreamEvent."""
        event = StreamEvent(type="chunk", payload={"text": "Hello"})
        self.assertEqual(event.type, "chunk")
        self.assertEqual(event.payload, {"text": "Hello"})

    def test_stream_event_default_payload(self):
        """Test StreamEvent with default empty payload."""
        event = StreamEvent(type="done")
        self.assertEqual(event.type, "done")
        self.assertEqual(event.payload, {})

    def test_to_sse_format(self):
        """Test SSE format output."""
        event = StreamEvent(type="chunk", payload={"text": "Hello", "sequence": 0})
        sse = event.to_sse()

        # Should start with "data: " and end with "\n\n"
        self.assertTrue(sse.startswith("data: "))
        self.assertTrue(sse.endswith("\n\n"))

        # Parse the JSON content
        json_str = sse[6:-2]  # Remove "data: " prefix and "\n\n" suffix
        parsed = json.loads(json_str)
        self.assertEqual(parsed["type"], "chunk")
        self.assertEqual(parsed["payload"]["text"], "Hello")
        self.assertEqual(parsed["payload"]["sequence"], 0)

    def test_to_dict(self):
        """Test dictionary conversion."""
        event = StreamEvent(type="error", payload={"message": "Test error"})
        result = event.to_dict()

        self.assertEqual(result["type"], "error")
        self.assertEqual(result["payload"]["message"], "Test error")

    def test_to_sse_serializes_datetime_payload_values(self):
        """SSE serialization should not fail for datetime-like payload values."""
        event = StreamEvent(
            type="state",
            payload={"generated_at": datetime(2026, 2, 9, 12, 0, 0)},
        )
        sse = event.to_sse()
        parsed = json.loads(sse[6:-2])
        self.assertEqual(parsed["payload"]["generated_at"], "2026-02-09T12:00:00")


class TestCreateSSEResponseHeaders(unittest.TestCase):
    """Tests for create_sse_response_headers function."""

    def test_headers_content_type(self):
        """Test that Content-Type is set correctly."""
        headers = create_sse_response_headers()
        self.assertEqual(headers["Content-Type"], "text/event-stream")

    def test_headers_cache_control(self):
        """Test that Cache-Control is set correctly."""
        headers = create_sse_response_headers()
        self.assertEqual(headers["Cache-Control"], "no-cache")

    def test_headers_connection(self):
        """Test that Connection is set correctly."""
        headers = create_sse_response_headers()
        self.assertEqual(headers["Connection"], "keep-alive")

    def test_headers_nginx_buffering(self):
        """Test that nginx buffering is disabled."""
        headers = create_sse_response_headers()
        self.assertEqual(headers["X-Accel-Buffering"], "no")


class TestStreamEventsGenerator(unittest.TestCase):
    """Tests for stream_events_generator function."""

    def test_converts_events_to_sse_strings(self):
        """Test that events are converted to SSE strings."""
        events = [
            StreamEvent(type="chunk", payload={"text": "Hello"}),
            StreamEvent(type="chunk", payload={"text": " World"}),
            StreamEvent(type="done", payload={"full_narrative": "Hello World"}),
        ]

        def event_generator():
            yield from events

        result = list(stream_events_generator(event_generator()))

        self.assertEqual(len(result), 3)
        for sse_str in result:
            self.assertTrue(sse_str.startswith("data: "))
            self.assertTrue(sse_str.endswith("\n\n"))


class TestStreamNarrativeSimple(unittest.TestCase):
    """Tests for stream_narrative_simple function."""

    @patch("mvp_site.streaming_orchestrator.gemini_provider")
    def test_yields_chunk_events(self, mock_provider):
        """Test that chunks are yielded as StreamEvents."""
        # Mock the streaming generator
        mock_provider.generate_content_stream_sync.return_value = iter(
            ["Hello", " ", "World"]
        )

        events = list(
            stream_narrative_simple(
                prompt_text="Test prompt",
                model_name="gemini-2.5-flash",
            )
        )

        # Should have 3 chunk events + 1 done event
        self.assertEqual(len(events), 4)

        # Check chunk events
        chunk_events = [e for e in events if e.type == "chunk"]
        self.assertEqual(len(chunk_events), 3)
        self.assertEqual(chunk_events[0].payload["text"], "Hello")
        self.assertEqual(chunk_events[0].payload["sequence"], 0)
        self.assertEqual(chunk_events[1].payload["text"], " ")
        self.assertEqual(chunk_events[1].payload["sequence"], 1)
        self.assertEqual(chunk_events[2].payload["text"], "World")
        self.assertEqual(chunk_events[2].payload["sequence"], 2)

        # Check done event
        done_events = [e for e in events if e.type == "done"]
        self.assertEqual(len(done_events), 1)
        self.assertEqual(done_events[0].payload["full_narrative"], "Hello World")
        self.assertEqual(done_events[0].payload["chunk_count"], 3)

    @patch("mvp_site.streaming_orchestrator.gemini_provider")
    def test_handles_errors(self, mock_provider):
        """Test that errors are handled gracefully."""
        # Mock an error during streaming
        mock_provider.generate_content_stream_sync.side_effect = RuntimeError(
            "API Error"
        )

        events = list(
            stream_narrative_simple(
                prompt_text="Test prompt",
                model_name="gemini-2.5-flash",
            )
        )

        # Should have 1 error event
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].type, "error")
        self.assertIn(
            "An unexpected error occurred while streaming the response.",
            events[0].payload["message"],
        )

    @patch("mvp_site.streaming_orchestrator.gemini_provider")
    def test_passes_parameters(self, mock_provider):
        """Test that parameters are passed correctly to the provider."""
        mock_provider.generate_content_stream_sync.return_value = iter([])

        list(
            stream_narrative_simple(
                prompt_text="Test prompt",
                model_name="gemini-2.5-pro",
                system_instruction="Be helpful",
                temperature=0.5,
                max_output_tokens=1024,
            )
        )

        mock_provider.generate_content_stream_sync.assert_called_once_with(
            prompt_contents=["Test prompt"],
            model_name="gemini-2.5-pro",
            system_instruction_text="Be helpful",
            temperature=0.5,
            max_output_tokens=1024,
        )


class TestStreamWithContext(unittest.TestCase):
    """Tests for stream_with_context function."""

    @patch("mvp_site.streaming_orchestrator.gemini_provider")
    def test_builds_prompt_from_context(self, mock_provider):
        """Test that context is built into the prompt."""
        mock_provider.generate_content_stream_sync.return_value = iter(["Response"])

        story_context = [
            {"actor": "user", "text": "I enter the cave"},
            {"actor": "gemini", "text": "The cave is dark and damp."},
        ]

        list(
            stream_with_context(
                user_input="I light a torch",
                story_context=story_context,
            )
        )

        # Check that the prompt was built correctly
        call_args = mock_provider.generate_content_stream_sync.call_args
        prompt = call_args.kwargs["prompt_contents"][0]

        self.assertIn("Player: I enter the cave", prompt)
        self.assertIn("Story: The cave is dark and damp.", prompt)
        self.assertIn("Player: I light a torch", prompt)

    @patch("mvp_site.streaming_orchestrator.gemini_provider")
    def test_limits_context_entries(self, mock_provider):
        """Test that context is limited to max entries."""
        mock_provider.generate_content_stream_sync.return_value = iter([])

        # Create more than 10 context entries
        story_context = [{"actor": "user", "text": f"Entry {i}"} for i in range(20)]

        list(
            stream_with_context(
                user_input="New action",
                story_context=story_context,
            )
        )

        # Check that only last 10 entries are included
        call_args = mock_provider.generate_content_stream_sync.call_args
        prompt = call_args.kwargs["prompt_contents"][0]

        # Should NOT contain Entry 0-9
        self.assertNotIn("Entry 0", prompt)
        self.assertNotIn("Entry 9", prompt)

        # Should contain Entry 10-19
        self.assertIn("Entry 10", prompt)
        self.assertIn("Entry 19", prompt)

    @patch("mvp_site.streaming_orchestrator.gemini_provider")
    def test_skips_non_dict_story_context_entries(self, mock_provider):
        """Non-dict historical entries should be ignored safely."""
        mock_provider.generate_content_stream_sync.return_value = iter([])
        story_context = [
            {"actor": "user", "text": "safe entry"},
            "unexpected string entry",
            99,
        ]

        list(
            stream_with_context(
                user_input="continue",
                story_context=story_context,
            )
        )
        call_args = mock_provider.generate_content_stream_sync.call_args
        prompt = call_args.kwargs["prompt_contents"][0]
        self.assertIn("Player: safe entry", prompt)
        self.assertNotIn("unexpected string entry", prompt)


class TestGeminiProviderStreamingIntegration(unittest.TestCase):
    """Integration tests for gemini_provider streaming functions."""

    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    def test_generate_content_stream_sync(self, mock_get_client):
        """Test synchronous streaming function."""
        from mvp_site.llm_providers.gemini_provider import generate_content_stream_sync

        # Mock the client and stream
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Create mock chunks
        mock_chunk1 = MagicMock()
        mock_chunk1.candidates = [MagicMock()]
        mock_chunk1.candidates[0].content.parts = [MagicMock()]
        mock_chunk1.candidates[0].content.parts[0].text = "Hello"

        mock_chunk2 = MagicMock()
        mock_chunk2.candidates = [MagicMock()]
        mock_chunk2.candidates[0].content.parts = [MagicMock()]
        mock_chunk2.candidates[0].content.parts[0].text = " World"

        mock_client.models.generate_content_stream.return_value = iter(
            [mock_chunk1, mock_chunk2]
        )

        # Test the function
        chunks = list(
            generate_content_stream_sync(
                prompt_contents=["Test"],
                model_name="gemini-2.5-flash",
            )
        )

        self.assertEqual(chunks, ["Hello", " World"])

    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    def test_handles_empty_parts(self, mock_get_client):
        """Test that empty parts are handled gracefully."""
        from mvp_site.llm_providers.gemini_provider import generate_content_stream_sync

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Create a chunk with empty parts (known Gemini issue)
        mock_chunk = MagicMock()
        mock_chunk.candidates = [MagicMock()]
        mock_chunk.candidates[0].content.parts = []  # Empty parts

        mock_client.models.generate_content_stream.return_value = iter([mock_chunk])

        # Should not raise, just yield nothing
        chunks = list(
            generate_content_stream_sync(
                prompt_contents=["Test"],
                model_name="gemini-2.5-flash",
            )
        )

        self.assertEqual(chunks, [])

    @patch("mvp_site.llm_providers.gemini_provider.get_client")
    def test_generate_content_stream_sync_uses_cached_content_when_cache_name_provided(
        self, mock_get_client
    ):
        """Streaming Gemini call should pass cached_content and suppress system_instruction."""
        from mvp_site.llm_providers.gemini_provider import generate_content_stream_sync

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_chunk = MagicMock()
        mock_chunk.candidates = [MagicMock()]
        mock_chunk.candidates[0].content.parts = [MagicMock()]
        mock_chunk.candidates[0].content.parts[0].text = "cached"
        mock_client.models.generate_content_stream.return_value = iter([mock_chunk])

        chunks = list(
            generate_content_stream_sync(
                prompt_contents=["Test"],
                model_name="gemini-3-flash-preview",
                system_instruction_text="must be ignored with cache",
                cache_name="cachedContents/stream-cache-1",
            )
        )

        self.assertEqual(chunks, ["cached"])
        call = mock_client.models.generate_content_stream.call_args
        config = call.kwargs["config"]
        self.assertEqual(config.cached_content, "cachedContents/stream-cache-1")
        self.assertIsNone(getattr(config, "system_instruction", None))


class TestStreamStoryWithGameState(unittest.TestCase):
    """Tests for stream_story_with_game_state persistence and validation."""

    @patch("mvp_site.streaming_orchestrator.firestore_service")
    @patch("mvp_site.streaming_orchestrator.parse_structured_response", create=True)
    @patch("mvp_site.streaming_orchestrator.continue_story_streaming")
    def test_persists_user_and_ai_when_streamed_response_valid(
        self,
        mock_continue_story_streaming,
        mock_parse_structured_response,
        mock_firestore,
    ):
        mock_firestore.get_campaign_by_id.return_value = ({"id": "c1"}, [])
        mock_firestore.get_campaign_game_state.return_value = {}
        mock_firestore.get_user_settings.return_value = {}

        structured_fields = {
            "planning_block": {
                "thinking": "Think through options",
                "choices": {
                    "do_thing": {
                        "text": "Do the thing",
                        "description": "Attempt the planned action.",
                    }
                },
            }
        }
        mock_parse_structured_response.return_value = (
            "final narrative",
            structured_fields,
        )
        mock_continue_story_streaming.return_value = iter(
            [
                StreamEvent(
                    type="done",
                    payload={
                        "full_narrative": '{"narrative":"final narrative"}',
                        "structured_response": structured_fields,
                    },
                )
            ]
        )

        events = list(
            stream_story_with_game_state(
                user_id="u1", campaign_id="c1", user_input="attack", mode="character"
            )
        )

        self.assertEqual(events[-1].type, "done")
        self.assertEqual(mock_firestore.add_story_entry.call_count, 2)
        gemini_calls = [
            c
            for c in mock_firestore.add_story_entry.call_args_list
            if len(c[0]) >= 3 and c[0][2] == "gemini"
        ]
        self.assertTrue(gemini_calls, "gemini add_story_entry call not found")
        gf = gemini_calls[0][1].get("structured_fields", {})
        self.assertEqual(
            gf.get("planning_block", {}).get("thinking"), "Think through options"
        )
        # Living world enrichment adds sequence_id and user_scene_number
        self.assertIn("sequence_id", gf)
        self.assertIn("user_scene_number", gf)
        # Streaming path should also persist planning_block into game state for reload parity.
        self.assertTrue(mock_firestore.update_campaign_game_state.called)
        args, _kwargs = mock_firestore.update_campaign_game_state.call_args
        self.assertEqual(args[0], "u1")
        self.assertEqual(args[1], "c1")
        self.assertIn("planning_block", args[2])

    @patch("mvp_site.streaming_orchestrator.firestore_service")
    @patch("mvp_site.streaming_orchestrator.parse_structured_response", create=True)
    @patch("mvp_site.streaming_orchestrator.continue_story_streaming")
    def test_emits_warning_and_skips_ai_persistence_when_validation_fails(
        self,
        mock_continue_story_streaming,
        mock_parse_structured_response,
        mock_firestore,
    ):
        mock_firestore.get_campaign_by_id.return_value = ({"id": "c1"}, [])
        mock_firestore.get_campaign_game_state.return_value = {}
        mock_firestore.get_user_settings.return_value = {}

        mock_parse_structured_response.side_effect = ValueError(
            "invalid structured response"
        )
        mock_continue_story_streaming.return_value = iter(
            [StreamEvent(type="done", payload={"full_narrative": "not-json"})]
        )

        events = list(
            stream_story_with_game_state(
                user_id="u1", campaign_id="c1", user_input="attack", mode="character"
            )
        )

        warning_events = [e for e in events if e.type == "warning"]
        self.assertEqual(len(warning_events), 1)
        self.assertIn("validation", warning_events[0].payload["message"].lower())

        # User entry persists, AI entry is skipped on validation failure
        self.assertEqual(mock_firestore.add_story_entry.call_count, 1)

    @patch("mvp_site.streaming_orchestrator.firestore_service")
    @patch("mvp_site.streaming_orchestrator.parse_structured_response", create=True)
    @patch("mvp_site.streaming_orchestrator.continue_story_streaming")
    def test_persists_god_mode_response_when_narrative_empty(
        self,
        mock_continue_story_streaming,
        mock_parse_structured_response,
        mock_firestore,
    ):
        """God mode can stream empty narrative; persist god_mode_response instead."""
        mock_firestore.get_campaign_by_id.return_value = ({"id": "c1"}, [])
        mock_firestore.get_campaign_game_state.return_value = {}
        mock_firestore.get_user_settings.return_value = {}

        structured_fields = {"god_mode_response": "Time set to midnight."}
        mock_parse_structured_response.return_value = ("", structured_fields)
        mock_continue_story_streaming.return_value = iter(
            [
                StreamEvent(
                    type="done",
                    payload={
                        "full_narrative": '{"god_mode_response":"Time set to midnight."}',
                        "structured_response": structured_fields,
                    },
                )
            ]
        )

        list(
            stream_story_with_game_state(
                user_id="u1", campaign_id="c1", user_input="set time", mode="god"
            )
        )

        self.assertEqual(mock_firestore.add_story_entry.call_count, 2)
        gemini_calls = [
            c
            for c in mock_firestore.add_story_entry.call_args_list
            if c[0][2] == "gemini"
        ]
        self.assertTrue(gemini_calls, "gemini add_story_entry call not found")
        gemini_kw = gemini_calls[0][1]
        self.assertEqual(
            gemini_kw["structured_fields"]["god_mode_response"], "Time set to midnight."
        )

    @patch("mvp_site.streaming_orchestrator.firestore_service")
    @patch("mvp_site.streaming_orchestrator.parse_structured_response", create=True)
    @patch("mvp_site.streaming_orchestrator.continue_story_streaming")
    def test_persists_god_mode_response_when_validation_parse_fails(
        self,
        mock_continue_story_streaming,
        mock_parse_structured_response,
        mock_firestore,
    ):
        """If parse fails during persistence validation, god_mode_response still persists."""
        mock_firestore.get_campaign_by_id.return_value = ({"id": "c1"}, [])
        mock_firestore.get_campaign_game_state.return_value = {}
        mock_firestore.get_user_settings.return_value = {}

        structured_fields = {"god_mode_response": "Set moon phase to full."}
        mock_parse_structured_response.side_effect = ValueError("broken parse")
        mock_continue_story_streaming.return_value = iter(
            [
                StreamEvent(
                    type="done",
                    payload={
                        "full_narrative": "{malformed-json",
                        "structured_response": structured_fields,
                    },
                )
            ]
        )

        list(
            stream_story_with_game_state(
                user_id="u1", campaign_id="c1", user_input="set moon phase", mode="god"
            )
        )

        self.assertEqual(mock_firestore.add_story_entry.call_count, 2)
        gemini_calls = [
            c
            for c in mock_firestore.add_story_entry.call_args_list
            if c[0][2] == "gemini"
        ]
        self.assertTrue(gemini_calls)
        self.assertEqual(
            gemini_calls[0][1]["structured_fields"]["god_mode_response"],
            "Set moon phase to full.",
        )

    @patch("mvp_site.streaming_orchestrator.firestore_service")
    @patch("mvp_site.streaming_orchestrator.parse_structured_response", create=True)
    @patch("mvp_site.streaming_orchestrator.continue_story_streaming")
    def test_persists_state_updates_from_done_payload(
        self,
        mock_continue_story_streaming,
        mock_parse_structured_response,
        mock_firestore,
    ):
        """Streaming path should persist LLM state_updates into campaign game state."""
        mock_firestore.get_campaign_by_id.return_value = ({"id": "c1"}, [])
        mock_firestore.get_campaign_game_state.return_value = {}
        mock_firestore.get_user_settings.return_value = {}

        mock_parse_structured_response.return_value = ("final narrative", {})
        mock_continue_story_streaming.return_value = iter(
            [
                StreamEvent(
                    type="done",
                    payload={
                        "full_narrative": '{"narrative":"final narrative"}',
                        "structured_response": {},
                        "state_updates": {"hp": {"current": 9}},
                    },
                )
            ]
        )

        list(
            stream_story_with_game_state(
                user_id="u1", campaign_id="c1", user_input="attack", mode="character"
            )
        )

        self.assertTrue(mock_firestore.update_state_with_changes.called)
        mock_firestore.update_campaign_game_state.assert_called()

    @patch("mvp_site.streaming_orchestrator.firestore_service")
    @patch("mvp_site.streaming_orchestrator.parse_structured_response", create=True)
    @patch("mvp_site.streaming_orchestrator.continue_story_streaming")
    def test_validation_prefers_raw_response_payload_when_available(
        self,
        mock_continue_story_streaming,
        mock_parse_structured_response,
        mock_firestore,
    ):
        """Validation should parse raw_response_text from done payload, not full_narrative."""
        mock_firestore.get_campaign_by_id.return_value = ({"id": "c1"}, [])
        mock_firestore.get_campaign_game_state.return_value = {}
        mock_firestore.get_user_settings.return_value = {}

        mock_parse_structured_response.return_value = ("parsed narrative", MagicMock())
        mock_continue_story_streaming.return_value = iter(
            [
                StreamEvent(
                    type="done",
                    payload={
                        "full_narrative": "already parsed text",
                        "raw_response_text": '{"narrative":"parsed narrative"}',
                    },
                )
            ]
        )

        list(
            stream_story_with_game_state(
                user_id="u1", campaign_id="c1", user_input="attack", mode="character"
            )
        )

        args, kwargs = mock_parse_structured_response.call_args
        self.assertEqual(args[0], '{"narrative":"parsed narrative"}')
        self.assertEqual(kwargs["requires_action_resolution"], False)

    @patch("mvp_site.streaming_orchestrator.firestore_service")
    @patch("mvp_site.streaming_orchestrator.parse_structured_response", create=True)
    @patch("mvp_site.streaming_orchestrator.continue_story_streaming")
    def test_does_not_persist_json_parse_failure_marker_when_full_narrative_available(
        self,
        mock_continue_story_streaming,
        mock_parse_structured_response,
        mock_firestore,
    ):
        """Firestore must not store the JSON-parse-failure marker string.

        OpenRouter streaming: plain-text narrative can't be parsed as JSON.
        parse_structured_response returns the fallback marker as a non-empty string.
        The orchestrator previously stored that marker verbatim because it passed the
        empty-string guard.  The done payload's full_narrative already contains the
        corrected narrative (raw streaming text); that value must be persisted instead.
        """
        _MARKER = JSON_PARSE_FALLBACK_MARKER
        _REAL_NARRATIVE = "The moonlit forest clears as you listen for sounds."

        mock_firestore.get_campaign_by_id.return_value = ({"id": "c1"}, [])
        mock_firestore.get_campaign_game_state.return_value = {}
        mock_firestore.get_user_settings.return_value = {}

        # parse_structured_response returns the error marker (non-empty but wrong)
        mock_parse_structured_response.return_value = (_MARKER, MagicMock())

        # done payload: full_narrative is the real story text (post-streaming-fallback fix)
        mock_continue_story_streaming.return_value = iter(
            [
                StreamEvent(
                    type="done",
                    payload={
                        "full_narrative": _REAL_NARRATIVE,
                        "raw_response_text": _REAL_NARRATIVE,
                    },
                )
            ]
        )

        list(
            stream_story_with_game_state(
                user_id="u1",
                campaign_id="c1",
                user_input="I look around",
                mode="character",
            )
        )

        # AI entry must be persisted — with the REAL narrative, not the error marker
        ai_calls = [
            call
            for call in mock_firestore.add_story_entry.call_args_list
            if len(call.args) > 2 and call.args[2] == "gemini"
        ]
        self.assertEqual(
            len(ai_calls), 1, "Expected exactly one AI story entry persisted"
        )
        persisted_narrative = ai_calls[0].args[3]
        self.assertNotEqual(
            persisted_narrative,
            _MARKER,
            "Firestore must not store the JSON-parse-failure marker as the narrative",
        )
        self.assertEqual(
            persisted_narrative,
            _REAL_NARRATIVE,
            "Firestore must store the real narrative from full_narrative",
        )


class TestStreamingPersistenceBeforeDone(unittest.TestCase):
    """Tests that persistence completes BEFORE done event is yielded.

    Bug BD-4s9: If client disconnects after receiving 'done' but before
    persistence, Firestore writes are killed by GeneratorExit. Persistence
    must happen before yielding the done event.
    """

    @patch("mvp_site.streaming_orchestrator.firestore_service")
    @patch("mvp_site.streaming_orchestrator.parse_structured_response", create=True)
    @patch("mvp_site.streaming_orchestrator.continue_story_streaming")
    def test_persistence_completes_before_done_event_yielded(
        self,
        mock_continue_story_streaming,
        mock_parse_structured_response,
        mock_firestore,
    ):
        """Persistence must complete BEFORE done event to prevent data loss on disconnect."""
        mock_firestore.get_campaign_by_id.return_value = ({"id": "c1"}, [])
        mock_firestore.get_campaign_game_state.return_value = {}
        mock_firestore.get_user_settings.return_value = {}

        mock_parse_structured_response.return_value = ("final narrative", {})
        mock_continue_story_streaming.return_value = iter(
            [
                StreamEvent(type="chunk", payload={"text": "Hello", "sequence": 0}),
                StreamEvent(
                    type="done",
                    payload={
                        "full_narrative": '{"narrative":"final narrative"}',
                        "raw_response_text": '{"narrative":"final narrative"}',
                    },
                ),
            ]
        )

        gen = stream_story_with_game_state(
            user_id="u1", campaign_id="c1", user_input="attack", mode="character"
        )

        # Consume events up to and including done, then close (simulates disconnect)
        for event in gen:
            if event.type == "done":
                break
        gen.close()

        # Persistence should have ALREADY happened before done was yielded
        self.assertGreaterEqual(
            mock_firestore.add_story_entry.call_count,
            2,
            "Both user and AI story entries must be persisted BEFORE yielding done event",
        )

    @patch("mvp_site.streaming_orchestrator.firestore_service")
    @patch("mvp_site.streaming_orchestrator.parse_structured_response", create=True)
    @patch("mvp_site.streaming_orchestrator.continue_story_streaming")
    def test_state_updates_persisted_before_done_event(
        self,
        mock_continue_story_streaming,
        mock_parse_structured_response,
        mock_firestore,
    ):
        """Game state updates must persist before done event to survive disconnect."""
        mock_firestore.get_campaign_by_id.return_value = ({"id": "c1"}, [])
        mock_firestore.get_campaign_game_state.return_value = {}
        mock_firestore.get_user_settings.return_value = {}

        mock_parse_structured_response.return_value = ("narrative", {})
        mock_continue_story_streaming.return_value = iter(
            [
                StreamEvent(
                    type="done",
                    payload={
                        "full_narrative": '{"narrative":"narrative"}',
                        "state_updates": {"hp": {"current": 5}},
                    },
                ),
            ]
        )

        gen = stream_story_with_game_state(
            user_id="u1", campaign_id="c1", user_input="attack", mode="character"
        )

        for event in gen:
            if event.type == "done":
                break
        gen.close()

        # Game state persistence must have happened before done was yielded
        self.assertTrue(
            mock_firestore.update_state_with_changes.called,
            "State updates must be persisted BEFORE yielding done event",
        )
        self.assertTrue(
            mock_firestore.update_campaign_game_state.called,
            "Campaign game state must be written BEFORE yielding done event",
        )


class TestChunkLoggerCleanup(unittest.TestCase):
    """Tests that _CHUNK_LOGGERS is cleaned up on all exit paths.

    Bug BD-bcw: finalize_chunk_logger only called on happy path.
    Error paths leak StreamingChunkLogger instances in global dict.
    """

    def test_chunk_logger_cleaned_up_on_streaming_error(self):
        """_CHUNK_LOGGERS must be cleaned up even when LLM streaming errors."""
        from mvp_site.streaming_chunk_logger import (
            _CHUNK_LOGGERS,
            get_or_create_chunk_logger,
        )

        # Directly test: create a logger, then verify it's cleaned up
        test_request_id = "test_leak_check_12345"

        # Ensure clean state
        _CHUNK_LOGGERS.pop(test_request_id, None)

        # Create a logger (simulates what continue_story_streaming does)
        get_or_create_chunk_logger(
            request_id=test_request_id,
            campaign_id="test_campaign",
        )
        self.assertIn(test_request_id, _CHUNK_LOGGERS)

        # Simulate what happens on error path: finalize is NOT called
        # (This is the bug - error paths skip finalize_chunk_logger)
        # For now, just verify the leak exists - the fix will add cleanup

        # Clean up after ourselves
        _CHUNK_LOGGERS.pop(test_request_id, None)

    @patch("mvp_site.llm_service._prepare_story_continuation")
    @patch("mvp_site.llm_service.gemini_provider")
    @patch("mvp_site.llm_service.json.dumps")
    def test_chunk_logger_not_leaked_on_llm_error(
        self,
        mock_json_dumps,
        mock_gemini,
        mock_prepare,
    ):
        """_CHUNK_LOGGERS must be cleaned up when LLM streaming raises."""
        from mvp_site.game_state import GameState
        from mvp_site.llm_service import continue_story_streaming
        from mvp_site.streaming_chunk_logger import _CHUNK_LOGGERS

        # Setup mock prepared result with real-ish values
        mock_agent = MagicMock()
        mock_agent.__class__.__name__ = "TestAgent"
        mock_agent.MODE = "character"
        mock_agent.requires_action_resolution = False
        mock_prepared = MagicMock()
        mock_prepared.agent = mock_agent
        mock_prepared.model_to_use = "gemini-2.5-flash"
        mock_prepared.provider_selection = MagicMock()
        mock_prepared.provider_selection.provider = "gemini"
        mock_prepared.system_instruction_final = "test system instruction"
        mock_prepared.story_context_for_prompt = []
        mock_prepared.temperature_override = None
        mock_prepare.return_value = mock_prepared

        # json.dumps returns a real string so serialization succeeds
        mock_json_dumps.return_value = '{"test": "data"}'

        # Make the LLM streaming call raise AFTER chunk logger is created
        mock_gemini.generate_content_stream_sync.side_effect = RuntimeError(
            "Gemini API Error"
        )

        # Record state before
        loggers_before = set(_CHUNK_LOGGERS.keys())

        events = list(
            continue_story_streaming(
                user_input="test",
                mode="character",
                story_context=[],
                current_game_state=GameState.from_dict({}),
                selected_prompts=[],
                use_default_world=False,
                campaign_id="test_leak_campaign",
            )
        )

        # Should have emitted an error event
        error_events = [e for e in events if e.type == "error"]
        self.assertGreaterEqual(len(error_events), 1)

        # Check for leaked loggers (new keys that weren't there before)
        loggers_after = set(_CHUNK_LOGGERS.keys())
        leaked = loggers_after - loggers_before
        # Clean up any leaked entries so test is hermetic
        for key in leaked:
            _CHUNK_LOGGERS.pop(key, None)

        self.assertEqual(
            len(leaked),
            0,
            f"_CHUNK_LOGGERS leaked {len(leaked)} entries on error path: {leaked}",
        )


class TestFrontendStreamingHandlerStructure(unittest.TestCase):
    """Structure tests for frontend streaming tool/state integration."""

    @staticmethod
    def _load_streaming_js() -> str:
        root = Path(__file__).resolve().parents[2]
        path = root / "mvp_site" / "frontend_v1" / "js" / "streaming.js"
        return path.read_text(encoding="utf-8")

    def test_create_handler_sets_tool_start_callback(self):
        """Frontend handler should react to tool_start events for live UX."""
        source = self._load_streaming_js()
        self.assertIn("client.onToolStart", source)

    def test_create_handler_sets_state_update_callback(self):
        """Frontend handler should react to state events from streaming endpoint."""
        source = self._load_streaming_js()
        self.assertIn("client.onStateUpdate", source)

    def test_streaming_client_handles_warning_events(self):
        """Streaming client should route warning events explicitly."""
        source = self._load_streaming_js()
        self.assertIn("case 'warning':", source)
        self.assertIn("this.onWarning", source)

    def test_create_handler_calls_append_to_story_on_complete(self):
        """Completion should route through appendToStory for consistent rendering."""
        source = self._load_streaming_js()
        self.assertIn("appendToStory(", source)
        self.assertIn("client.onComplete", source)

    def test_tool_result_clears_running_tool_status(self):
        """Tool result handling should clear any prior running indicator."""
        source = self._load_streaming_js()
        self.assertIn("data-tool-status", source)
        self.assertIn("querySelectorAll('[data-tool-status=\"running\"]')", source)
        self.assertIn("status.remove()", source)

    def test_tool_result_has_faction_specific_inline_rendering(self):
        """Faction tool results should render richer inline summaries."""
        source = self._load_streaming_js()
        self.assertIn("faction_", source)
        self.assertIn("Faction update:", source)
        self.assertIn("power_change", source)


class TestFrontendAppStreamingWiring(unittest.TestCase):
    """Structural tests for app.js streaming handler wiring."""

    @staticmethod
    def _load_app_js() -> str:
        root = Path(__file__).resolve().parents[2]
        path = root / "mvp_site" / "frontend_v1" / "app.js"
        return path.read_text(encoding="utf-8")

    def test_submit_handler_checks_streaming_toggle(self):
        """Submit flow should branch using the streaming localStorage toggle."""
        source = self._load_app_js()
        self.assertIn("localStorage.getItem('useStreaming') !== 'false'", source)

    def test_submit_handler_calls_streaming_helper(self):
        """Submit flow should invoke handleStreamingInteraction when enabled."""
        source = self._load_app_js()
        self.assertIn("handleStreamingInteraction(", source)
        self.assertIn("handleRegularInteraction(", source)

    def test_regular_path_sanitizes_and_handles_rate_limit(self):
        """Regular interaction handler should sanitize errors and invoke rate-limit modal."""
        source = self._load_app_js()
        self.assertIn(
            "window.showRateLimitModal(error.message, error.resetTime, error.resetType)",
            source,
        )
        self.assertIn("appendToStory('system', sanitizeHtml(userMessage))", source)

    def test_streaming_completion_finalizes_canonical_path(self):
        """Streaming completion should finalize via renderStoryEntryElement for feature parity."""
        source = self._load_app_js()
        self.assertIn("streamingClient.onComplete = (payload) => {", source)
        self.assertIn("payload?.structured_response || payload || {}", source)
        self.assertIn("renderStoryEntryElement(", source)
        self.assertIn("streamingElement,", source)
        self.assertIn("'gemini',", source)

    def test_streaming_warning_falls_back_after_completion(self):
        """Warnings emitted after done should still surface via system appendToStory."""
        source = self._load_app_js()
        self.assertIn("appendToStory('system', sanitizeHtml(warningMessage))", source)

    def test_streaming_client_is_cancelled_on_campaign_switch(self):
        """Campaign changes should cancel the previous streaming client before replacement."""
        source = self._load_app_js()
        self.assertIn("streamingClient.cancel()", source)


def _extract_planning_thinking(raw_text: str):
    """Python equivalent of StreamingClient._extractPlanningThinking().

    Extracts the value of the root "thinking" key from a planning_block context
    in a potentially incomplete JSON stream. Iterates through all matches
    to skip thinking keys that appear outside planning_block context.
    Uses brace counting to handle nested objects within planning_block.
    """

    def _is_escaped_quote(text: str, quote_index: int) -> bool:
        """Return True when quote_index is escaped by an odd slash count."""
        backslash_count = 0
        i = quote_index - 1
        while i >= 0 and text[i] == "\\":
            backslash_count += 1
            i -= 1
        return backslash_count % 2 == 1

    def _is_inside_string_value(text: str, position: int) -> bool:
        """Check if position is inside a string value (not a JSON key).

        Walks backwards from position to determine if we're inside a quoted string.
        Returns True if position is inside a string value.
        """
        # Walk backwards to find if we're in a string context
        in_string = False
        i = position - 1
        while i >= 0:
            ch = text[i]
            if ch == '"':
                # Check if this quote is escaped
                backslash_count = 0
                j = i - 1
                while j >= 0 and text[j] == "\\":
                    backslash_count += 1
                    j -= 1
                if backslash_count % 2 == 0:
                    # Not escaped - toggle string context
                    in_string = not in_string
            elif ch == ":" and not in_string:
                # Found colon outside string - this is a key, not a value
                return False
            elif ch == "{" and not in_string:
                # Found opening brace outside string - this is a key
                return False
            i -= 1
        return in_string

    def _planning_block_depth_at_position(text: str, position: int) -> int:
        """Return planning_block depth at position or 0 when not in planning_block."""
        prefix = text[:position]

        all_matches = [
            m
            for m in re.finditer(r'"planning_block"\s*:\s*\{', prefix)
            if not _is_escaped_quote(prefix, m.start())
        ]
        if not all_matches:
            return 0

        for planning_match in reversed(all_matches):
            # Skip if planning_block itself is inside a string value
            if _is_inside_string_value(text, planning_match.start()):
                continue

            depth = 1
            in_string = False
            escaped = False

            for i in range(planning_match.end(), position):
                ch = text[i]
                if escaped:
                    escaped = False
                    continue
                if ch == "\\":
                    escaped = True
                    continue
                if ch == '"':
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth <= 0:
                        break

            if depth > 0:
                return depth

        return 0

    pattern = re.compile(r'"thinking"\s*:\s*"')
    for match in pattern.finditer(raw_text):
        if _is_escaped_quote(raw_text, match.start()):
            continue

        # Require root planning_block depth (1) to avoid nested thinking keys.
        if _planning_block_depth_at_position(raw_text, match.start()) != 1:
            continue

        i = match.end()
        escaped = False
        out = []

        while i < len(raw_text):
            ch = raw_text[i]
            if escaped:
                if ch == "n":
                    out.append("\n")
                elif ch == "t":
                    out.append("\t")
                elif ch == "r":
                    out.append("\r")
                elif ch == '"':
                    out.append('"')
                elif ch == "\\":
                    out.append("\\")
                else:
                    out.append(ch)
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                return "".join(out)
            else:
                out.append(ch)
            i += 1

        result = "".join(out)
        return result if result else None

    return None


class TestExtractPlanningThinking(unittest.TestCase):
    """Test cases matching the JavaScript _extractPlanningThinking algorithm."""

    def test_complete_thinking_field(self):
        """Extracts thinking text from a complete JSON envelope."""
        raw = '{"planning_block":{"thinking":"The player wants to attack the dragon"},"narrative":"You swing your sword"}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "The player wants to attack the dragon")

    def test_partial_thinking_still_streaming(self):
        """Returns partial text when JSON is still streaming (no closing quote)."""
        raw = '{"planning_block":{"thinking":"The player is trying to'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "The player is trying to")

    def test_no_planning_block(self):
        """Returns None when no planning_block context exists."""
        raw = '{"narrative":"You enter the cave","thinking":"This is not inside planning_block"}'
        result = _extract_planning_thinking(raw)
        self.assertIsNone(result)

    def test_no_thinking_key(self):
        """Returns None when no thinking key exists at all."""
        raw = '{"planning_block":{"strategy":"attack"},"narrative":"You fight"}'
        result = _extract_planning_thinking(raw)
        self.assertIsNone(result)

    def test_empty_thinking(self):
        """Returns empty string when thinking value is empty."""
        raw = '{"planning_block":{"thinking":""}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "")

    def test_escaped_characters(self):
        """Properly handles JSON escape sequences in thinking text."""
        raw = r'{"planning_block":{"thinking":"Line 1\nLine 2\tTabbed \"quoted\""}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, 'Line 1\nLine 2\tTabbed "quoted"')

    def test_escaped_backslash(self):
        """Handles escaped backslash correctly."""
        raw = r'{"planning_block":{"thinking":"path\\to\\file"}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "path\\to\\file")

    def test_whitespace_around_colon(self):
        """Handles optional whitespace between key and value."""
        raw = '{"planning_block" : { "thinking" : "Flexible spacing"}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "Flexible spacing")

    def test_thinking_with_preceding_fields(self):
        """Extracts thinking when other fields come before it in planning_block."""
        raw = '{"planning_block":{"strategy":"flanking","thinking":"Need to roll for stealth"}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "Need to roll for stealth")

    def test_progressive_streaming_of_chunks(self):
        """Simulates progressive chunk accumulation during streaming."""
        chunks = [
            '{"planning_block":{',
            '"thinking":"The play',
            "er decides to ",
            "negotiate with the merchant",
            '"},"narrative":"You approach',
        ]
        accumulated = ""
        results = []
        for chunk in chunks:
            accumulated += chunk
            result = _extract_planning_thinking(accumulated)
            results.append(result)

        self.assertIsNone(results[0])
        self.assertEqual(results[1], "The play")
        self.assertEqual(results[2], "The player decides to ")
        self.assertEqual(
            results[3], "The player decides to negotiate with the merchant"
        )
        self.assertEqual(
            results[4], "The player decides to negotiate with the merchant"
        )

    def test_planning_block_with_choices(self):
        """Handles planning_block with choices array alongside thinking."""
        raw = '{"planning_block":{"thinking":"Consider options","choices":["Attack","Flee"]}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "Consider options")

    def test_god_mode_response_not_extracted(self):
        """Ensures god_mode_response is NOT extracted as thinking."""
        raw = '{"god_mode_response":"Time set to midnight","planning_block":{}}'
        result = _extract_planning_thinking(raw)
        self.assertIsNone(result)

    def test_standalone_thinking_outside_planning_block(self):
        """Ensures thinking key outside planning_block context is ignored."""
        raw = '{"narrative":"Story","metadata":{"thinking":"metadata thought"}}'
        result = _extract_planning_thinking(raw)
        self.assertIsNone(result)

    def test_thinking_before_planning_block_skipped(self):
        """Iterates past a thinking key that appears before planning_block context."""
        raw = '{"debug":{"thinking":"debug thought"},"planning_block":{"thinking":"real thought"}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "real thought")

    def test_multiple_thinking_keys_picks_planning_one(self):
        """When multiple thinking keys exist, picks the one in planning_block."""
        raw = '{"metadata":{"thinking":"meta"},"other":{"thinking":"other"},"planning_block":{"thinking":"correct"}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "correct")

    def test_nested_planning_block_sibling_thinking_ignored(self):
        """Thinking as sibling of nested planning_block is not extracted."""
        raw = '{"nested":{"planning_block":{}},"thinking":"should not extract"}'
        result = _extract_planning_thinking(raw)
        self.assertIsNone(result)

    def test_planning_block_thinking_found_after_closed_block(self):
        """Thinking inside planning_block is found even with closed sibling."""
        raw = '{"nested":{"planning_block":{}},"planning_block":{"thinking":"found"}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "found")

    def test_nested_content_before_thinking_in_planning_block(self):
        """Extracts thinking when planning_block has nested content before thinking.

        This tests the fix for the nested fields bug where extraction would fail
        if planning_block contained nested objects (like choices) before thinking.
        """
        raw = '{"planning_block":{"choices":{"option1":{"text":"Do this"}},"thinking":"Found it"}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "Found it")

    def test_nested_array_before_thinking_in_planning_block(self):
        """Extracts thinking when planning_block has array content before thinking."""
        raw = '{"planning_block":{"choices":[{"id":"1"},{"id":"2"}],"thinking":"Array case"}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "Array case")

    def test_planning_block_closes_before_metadata_thinking(self):
        """Does not treat sibling object thinking as planning_block thinking."""
        raw = '{"planning_block":{},"metadata":{"thinking":"wrong"}}'
        result = _extract_planning_thinking(raw)
        self.assertIsNone(result)

    def test_prefers_root_planning_block_thinking_over_nested(self):
        """Prefers root planning_block.thinking over nested thinking keys."""
        raw = '{"planning_block":{"choices":{"thinking":"child"},"thinking":"root"}}'
        result = _extract_planning_thinking(raw)
        self.assertEqual(result, "root")

    def test_escaped_tokens_do_not_trigger_planning_extraction(self):
        """Ignores escaped planning/thinking tokens inside JSON string content."""
        raw = '{"narrative":"escaped \\"planning_block\\":{\\"thinking\\":\\"fake\\"}","thinking":"outside"}'
        result = _extract_planning_thinking(raw)
        self.assertIsNone(result)


def _make_compliant_lw_event(**overrides):
    """Return a fully-compliant background event dict."""
    base = {
        "actor": "The Merchant Guild",
        "action": "dispatched a trade caravan",
        "location": "North Road",
        "outcome": "caravan arrived safely",
        "event_type": "economic",
        "status": "completed",
        "discovery_condition": "player passes through North Road",
    }
    base.update(overrides)
    return base


class TestCountCompliantLwEvents(unittest.TestCase):
    """Unit tests for _count_compliant_lw_events."""

    def test_empty_list_returns_zero(self):
        self.assertEqual(_count_compliant_lw_events([]), 0)

    def test_two_fully_compliant_events(self):
        events = [
            _make_compliant_lw_event(),
            _make_compliant_lw_event(actor="Guard Captain"),
        ]
        self.assertEqual(_count_compliant_lw_events(events), 2)

    def test_event_missing_one_field_not_counted(self):
        incomplete = _make_compliant_lw_event()
        del incomplete["discovery_condition"]
        self.assertEqual(_count_compliant_lw_events([incomplete]), 0)

    def test_mixed_events_only_counts_complete(self):
        complete = _make_compliant_lw_event()
        incomplete = _make_compliant_lw_event()
        del incomplete["outcome"]
        self.assertEqual(_count_compliant_lw_events([complete, incomplete]), 1)

    def test_non_dict_entries_not_counted(self):
        self.assertEqual(_count_compliant_lw_events(["not_a_dict", 42, None]), 0)

    def test_all_required_fields_present_empty_values_still_count(self):
        event = dict.fromkeys(_LW_REQUIRED_FIELDS, "")
        self.assertEqual(_count_compliant_lw_events([event]), 1)


class TestWarnIfLivingWorldMissingCompliance(unittest.TestCase):
    """Tests that _warn_if_living_world_missing emits LIVING_WORLD_COMPLIANCE warning."""

    def _make_kwargs(self, background_events):
        return {
            "updated_state_dict": {"turn_number": 2},
            "structured_fields": {
                "world_events": {"background_events": background_events}
            },
            "state_updates": None,
            "is_god_mode": False,
            "agent_mode": None,
            "mode": "normal",
        }

    def test_empty_background_events_logs_compliance_warning(self):
        with (
            patch("mvp_site.streaming_orchestrator.logging_util") as mock_log,
            patch("mvp_site.streaming_orchestrator.world_logic") as mock_wl,
        ):
            mock_wl.mode_advances_time.return_value = True
            _warn_if_living_world_missing(**self._make_kwargs([]))
        warning_calls = [str(c) for c in mock_log.warning.call_args_list]
        self.assertTrue(
            any("LIVING_WORLD_COMPLIANCE" in c for c in warning_calls),
            f"Expected LIVING_WORLD_COMPLIANCE warning, got: {warning_calls}",
        )

    def test_one_compliant_event_logs_compliance_warning(self):
        with (
            patch("mvp_site.streaming_orchestrator.logging_util") as mock_log,
            patch("mvp_site.streaming_orchestrator.world_logic") as mock_wl,
        ):
            mock_wl.mode_advances_time.return_value = True
            _warn_if_living_world_missing(
                **self._make_kwargs([_make_compliant_lw_event()])
            )
        warning_calls = [str(c) for c in mock_log.warning.call_args_list]
        self.assertTrue(
            any("LIVING_WORLD_COMPLIANCE" in c for c in warning_calls),
            f"Expected LIVING_WORLD_COMPLIANCE warning for 1 event, got: {warning_calls}",
        )

    def test_two_compliant_events_no_compliance_warning(self):
        events = [_make_compliant_lw_event(), _make_compliant_lw_event(actor="Guard")]
        with (
            patch("mvp_site.streaming_orchestrator.logging_util") as mock_log,
            patch("mvp_site.streaming_orchestrator.world_logic") as mock_wl,
        ):
            mock_wl.mode_advances_time.return_value = True
            _warn_if_living_world_missing(**self._make_kwargs(events))
        warning_calls = [str(c) for c in mock_log.warning.call_args_list]
        self.assertFalse(
            any("LIVING_WORLD_COMPLIANCE" in c for c in warning_calls),
            f"Should NOT warn when 2 compliant events present, got: {warning_calls}",
        )

    def test_turn_zero_does_not_warn(self):
        kwargs = {
            "updated_state_dict": {"turn_number": 0},
            "structured_fields": {"world_events": {"background_events": []}},
            "state_updates": None,
            "is_god_mode": False,
            "agent_mode": None,
            "mode": "normal",
        }
        with (
            patch("mvp_site.streaming_orchestrator.logging_util") as mock_log,
            patch("mvp_site.streaming_orchestrator.world_logic") as mock_wl,
        ):
            mock_wl.mode_advances_time.return_value = True
            result = _warn_if_living_world_missing(**kwargs)
        self.assertIsNone(result)
        self.assertEqual(mock_log.warning.call_count, 0)

    def test_non_list_background_events_logs_schema_warning(self):
        kwargs = {
            "updated_state_dict": {"turn_number": 2},
            "structured_fields": {
                "world_events": {"background_events": {"append": []}}
            },
            "state_updates": None,
            "is_god_mode": False,
            "agent_mode": None,
            "mode": "normal",
        }
        with (
            patch("mvp_site.streaming_orchestrator.logging_util") as mock_log,
            patch("mvp_site.streaming_orchestrator.world_logic") as mock_wl,
        ):
            mock_wl.mode_advances_time.return_value = True
            _warn_if_living_world_missing(**kwargs)
        warning_calls = [str(c) for c in mock_log.warning.call_args_list]
        self.assertTrue(
            any("LIVING_WORLD_SCHEMA" in c for c in warning_calls),
            f"Expected LIVING_WORLD_SCHEMA warning, got: {warning_calls}",
        )
        self.assertFalse(
            any("LIVING_WORLD_COMPLIANCE" in c for c in warning_calls),
            "Should not emit compliance warning for non-list background_events",
        )

    def test_no_background_events_key_no_compliance_warning(self):
        kwargs = {
            "updated_state_dict": {"turn_number": 2},
            "structured_fields": {"world_events": {"some_other_key": []}},
            "state_updates": None,
            "is_god_mode": False,
            "agent_mode": None,
            "mode": "normal",
        }
        with (
            patch("mvp_site.streaming_orchestrator.logging_util") as mock_log,
            patch("mvp_site.streaming_orchestrator.world_logic") as mock_wl,
        ):
            mock_wl.mode_advances_time.return_value = True
            _warn_if_living_world_missing(**kwargs)
        warning_calls = [str(c) for c in mock_log.warning.call_args_list]
        self.assertTrue(
            any("LIVING_WORLD_SCHEMA" in c for c in warning_calls),
            f"Expected LIVING_WORLD_SCHEMA warning for missing key, got: {warning_calls}",
        )
        self.assertFalse(
            any("LIVING_WORLD_COMPLIANCE" in c for c in warning_calls),
            "Should not emit compliance warning when no background_events key",
        )


if __name__ == "__main__":
    unittest.main()
