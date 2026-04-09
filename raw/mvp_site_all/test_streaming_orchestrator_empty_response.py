"""Integration test for streaming_orchestrator empty response validation.

Tests the full flow: llm_service → streaming_orchestrator → validation → persistence.
This reproduces the production bug where empty Phase 2 responses cause validation failures.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

os.environ.setdefault("TESTING_AUTH_BYPASS", "true")
os.environ.setdefault("USE_MOCKS", "true")

from mvp_site.game_state import GameState
from mvp_site.streaming_orchestrator import stream_story_with_game_state


@pytest.fixture
def mock_services():
    """Mock all services for integration test."""
    with patch("mvp_site.streaming_orchestrator.firestore_service") as mock_firestore, \
         patch("mvp_site.streaming_orchestrator.continue_story_streaming") as mock_streaming:

        # Mock campaign data
        campaign_data = {
            "id": "test-campaign",
            "title": "Test Campaign",
            "selected_prompts": [],
            "use_default_world": False,
        }
        story_context = []
        mock_firestore.get_campaign_by_id.return_value = (campaign_data, story_context)

        # Mock game state - must return a proper GameState instance
        game_state = GameState(debug_mode=False)
        mock_firestore.get_campaign_game_state.return_value = game_state

        # Mock user settings
        mock_firestore.get_user_settings.return_value = {"debug_mode": False}

        yield {
            "firestore": mock_firestore,
            "streaming": mock_streaming,
        }


def test_empty_phase2_causes_validation_failure_and_user_only_persist(mock_services):
    """Reproduce production bug: empty Phase 2 → validation fails → only user persisted.

    THIS IS THE BUG: When Phase 2 returns empty, streaming_orchestrator validation
    fails and only user input gets persisted. Frontend then shows:
    "Scene #3: [Error: Empty response from server]"
    """
    from mvp_site.stream_events import StreamEvent

    # Mock continue_story_streaming to return events with EMPTY raw_response_text
    # This simulates what happens when Phase 2 returns no chunks
    def mock_streaming_events(*args, **kwargs):
        # Status event
        yield StreamEvent(type="status", payload={"message": "Preparing..."})

        # Chunk event (Phase 1 - has tool_requests)
        yield StreamEvent(
            type="chunk",
            payload={"text": '{"narrative": "Rolling...", "tool_requests": [', "sequence": 0}
        )
        yield StreamEvent(
            type="chunk",
            payload={"text": '{"tool": "roll_dice", "args": {"notation": "1d20"}}]}', "sequence": 1}
        )

        # Tool events
        yield StreamEvent(
            type="tool_start",
            payload={"tool_name": "roll_dice", "args": {"notation": "1d20"}}
        )
        yield StreamEvent(
            type="tool_result",
            payload={"tool_name": "roll_dice", "result": {"total": 15}}
        )

        # Phase transition
        yield StreamEvent(
            type="phase_transition",
            payload={"phase": "post_tools", "reset_text": True}
        )

        # CRITICAL: Done event with parsed narrative BUT empty raw_response_text
        # This is what happens when Phase 2 returns no chunks - parse_structured_response
        # provides fallback but raw JSON is empty
        yield StreamEvent(
            type="done",
            payload={
                "full_narrative": "The story awaits your input...",  # Fallback from parse
                "raw_response_text": "",  # EMPTY - this triggers validation failure
                "chunk_count": 2,
                "agent_used": "TestAgent",
                "agent_mode": "test",
                "model_used": "gemini-2.5-flash",
                "provider_used": "gemini",
                "has_structured_response": True,
                "state_updates": {},
                "structured_response": {"narrative": "The story awaits your input..."},
                "user_scene_number": 1,
            },
        )

    mock_services["streaming"].return_value = mock_streaming_events()

    # Execute streaming flow
    events = list(stream_story_with_game_state(
        user_id="test-user",
        campaign_id="test-campaign",
        user_input="I attack",
        mode="character",
    ))

    # Extract event types
    event_types = [e.type for e in events]
    warning_events = [e for e in events if e.type == "warning"]

    # Print debug info
    print(f"\n=== INTEGRATION TEST EVENTS ({len(events)}) ===")
    for i, event in enumerate(events):
        payload_keys = list(event.payload.keys()) if isinstance(event.payload, dict) else []
        print(f"{i}: type={event.type}, payload_keys={payload_keys}")
        if event.type == "warning":
            print(f"   message: {event.payload.get('message')}")
        elif event.type == "done":
            print(f"   full_narrative length: {len(event.payload.get('full_narrative', ''))}")

    # Check persistence calls
    add_story_calls = mock_services["firestore"].add_story_entry.call_args_list
    print(f"\n=== PERSISTENCE CALLS ({len(add_story_calls)}) ===")
    for i, call in enumerate(add_story_calls):
        args = call[0]  # positional args
        kwargs = call[1]  # keyword args
        actor = args[2] if len(args) > 2 else "unknown"
        text = args[3] if len(args) > 3 else "unknown"
        print(f"{i}: actor={actor}, text_length={len(str(text))}")

    # ASSERTION 1: Should have warning about validation failure
    assert warning_events, "Should have warning event for validation failure"
    warning_msg = warning_events[0].payload.get("message", "")
    assert "validation failed" in warning_msg.lower(), \
        f"Warning should mention validation failure, got: {warning_msg}"

    # ASSERTION 2: Should only persist user entry (actor='user'), not AI entry (actor='gemini')
    # This is the BUG - only user input persisted
    user_persists = [call for call in add_story_calls if call[0][2] == "user"]
    ai_persists = [call for call in add_story_calls if call[0][2] == "gemini"]

    print(f"\n=== BUG CHECK ===")
    print(f"User persists: {len(user_persists)}")
    print(f"AI persists: {len(ai_persists)}")

    assert len(user_persists) == 1, "Should persist exactly one user entry"
    assert len(ai_persists) == 0, \
        f"BUG REPRODUCED: AI response should NOT be persisted when validation fails, but got {len(ai_persists)}"


def test_after_fix_empty_response_yields_error_not_done(mock_services):
    """After fix: empty Phase 2 should yield error event, preventing validation failure."""
    from mvp_site.stream_events import StreamEvent

    def mock_streaming_events_with_fix(*args, **kwargs):
        yield StreamEvent(type="status", payload={"message": "Preparing..."})

        # With the fix, when Phase 2 is empty, continue_story_streaming should
        # yield error event instead of done event with empty narrative
        yield StreamEvent(
            type="error",
            payload={
                "message": "LLM returned empty response. This may indicate a model error or timeout.",
                "error_type": "empty_response",
                "chunk_count": 0,
            },
        )

    mock_services["streaming"].return_value = mock_streaming_events_with_fix()

    events = list(stream_story_with_game_state(
        user_id="test-user",
        campaign_id="test-campaign",
        user_input="I attack",
        mode="character",
    ))

    error_events = [e for e in events if e.type == "error"]
    warning_events = [e for e in events if e.type == "warning"]

    # After fix: Should have error event from llm_service, not validation warning
    assert error_events, "Should have error event for empty response"
    error_payload = error_events[0].payload
    assert error_payload.get("error_type") == "empty_response", \
        f"Error should have type 'empty_response', got: {error_payload.get('error_type')}"

    # Should NOT have validation failure warning (error caught earlier)
    validation_warnings = [
        w for w in warning_events
        if "validation failed" in w.payload.get("message", "").lower()
    ]
    assert len(validation_warnings) == 0, \
        "Should NOT have validation warning when error is caught in llm_service"
