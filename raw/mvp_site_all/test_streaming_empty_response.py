"""Test for streaming empty response bug.

Reproduces: "Error: Empty response from server" when Phase 2 streaming returns no chunks.

Root cause: If tool_requests trigger Phase 2, but Phase 2 stream returns empty,
narrative_text becomes "" and frontend shows error.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

os.environ.setdefault("TESTING_AUTH_BYPASS", "true")
os.environ.setdefault("USE_MOCKS", "true")

from mvp_site.game_state import GameState
from mvp_site.llm_service import continue_story_streaming
from mvp_site.stream_events import StreamEvent


@pytest.fixture
def mock_services():
    """Mock all external services for streaming test."""
    with patch("mvp_site.llm_service.gemini_provider") as mock_gemini, \
         patch("mvp_site.llm_service.execute_tool_requests") as mock_tools, \
         patch("mvp_site.llm_service._prepare_story_continuation") as mock_prepare:

        # Mock prepare to return minimal required structure
        mock_prep = MagicMock()
        mock_prep.agent = MagicMock()
        mock_prep.agent.__class__.__name__ = "TestAgent"
        mock_prep.agent.MODE = "test"
        mock_prep.agent.requires_action_resolution = False
        mock_prep.model_to_use = "gemini-2.5-flash"
        mock_prep.provider_selection.provider = "gemini"
        mock_prep.system_instruction_final = "test"
        mock_prep.gemini_request = MagicMock()
        mock_prep.gemini_request.to_json = lambda: '{}'
        mock_prep.temperature_override = None
        mock_prepare.return_value = mock_prep

        yield {
            "gemini": mock_gemini,
            "tools": mock_tools,
            "prepare": mock_prepare,
        }


def test_empty_phase2_response_returns_error_not_empty_string(mock_services):
    """Phase 2 returning no chunks should NOT yield done event with empty narrative.

    THIS TEST SHOULD FAIL until the bug is fixed - it demonstrates the bug exists.
    """

    # Phase 1: Return JSON with tool_requests (triggers Phase 2)
    phase1_response = '{"narrative": "Rolling dice...", "tool_requests": [{"tool": "roll_dice", "args": {"notation": "1d20"}}]}'
    mock_services["gemini"].generate_content_stream_sync = MagicMock(
        side_effect=[
            iter([phase1_response]),  # Phase 1: Returns tool_requests
            iter([]),  # Phase 2: Returns EMPTY (bug trigger)
        ]
    )

    # Mock tool execution
    mock_services["tools"].return_value = [{"tool": "roll_dice", "result": {"total": 15}}]

    # Mock gemini_request.to_json to return dict not string
    mock_services["prepare"].return_value.gemini_request.to_json = lambda: {}

    # Mock token calculation
    with patch("mvp_site.llm_service._calculate_prompt_and_system_tokens") as mock_calc, \
         patch("mvp_site.llm_service._get_safe_output_token_limit") as mock_limit:
        mock_calc.return_value = (100, 50)
        mock_limit.return_value = 4096

        # Collect events
        events = list(continue_story_streaming(
            user_input="test",
            mode="character",
            story_context=[],
            current_game_state=GameState.from_dict({}),
            selected_prompts=[],
            use_default_world=False,
            user_id="test-user",
            campaign_id="test-campaign",
        ))

    # Extract event types and payloads
    done_events = [e for e in events if e.type == "done"]
    error_events = [e for e in events if e.type == "error"]

    # Debug: Print all events
    print(f"\n=== EVENTS COLLECTED ({len(events)}) ===")
    for i, event in enumerate(events):
        print(f"{i}: type={event.type}, payload_keys={list(event.payload.keys()) if isinstance(event.payload, dict) else 'N/A'}")
        if event.type == "done":
            print(f"   full_narrative length: {len(event.payload.get('full_narrative', ''))}")
            print(f"   full_narrative value: {repr(event.payload.get('full_narrative', ''))[:100]}")
        elif event.type == "error":
            print(f"   error_type: {event.payload.get('error_type')}")
            print(f"   message: {event.payload.get('message')}")

    # ASSERTION: With the fix, empty Phase 2 should yield error event, NOT done event
    print(f"\n=== FIX VERIFICATION ===")
    print(f"done_events: {len(done_events)}")
    print(f"error_events: {len(error_events)}")

    # After fix: Should have error event for empty response
    assert error_events, "Should have error event for empty Phase 2 response"
    error_payload = error_events[0].payload
    assert error_payload.get("error_type") == "empty_response", \
        f"Error should have type 'empty_response', got: {error_payload.get('error_type')}"
    assert "empty" in error_payload.get("message", "").lower(), \
        f"Error message should mention 'empty', got: {error_payload.get('message')}"

    # Should NOT have done event (or if it does, it should not have empty narrative)
    if done_events:
        done_payload = done_events[0].payload
        full_narrative = done_payload.get("full_narrative", "")
        assert full_narrative and full_narrative.strip(), \
            f"If done event exists, narrative must not be empty. Got: {repr(full_narrative)}"


def test_phase1_only_empty_response_is_handled(mock_services):
    """Phase 1 returning empty should also be handled gracefully."""

    # Phase 1: Return EMPTY (no tool_requests, just empty)
    mock_services["gemini"].generate_content_stream_sync = MagicMock(
        return_value=iter([])  # Empty Phase 1
    )

    with patch("mvp_site.llm_service._calculate_prompt_and_system_tokens") as mock_calc, \
         patch("mvp_site.llm_service._get_safe_output_token_limit") as mock_limit:
        mock_calc.return_value = (100, 50)
        mock_limit.return_value = 4096

        events = list(continue_story_streaming(
            user_input="test",
            mode="character",
            story_context=[],
            current_game_state=GameState.from_dict({}),
        ))

    done_events = [e for e in events if e.type == "done"]
    error_events = [e for e in events if e.type == "error"]

    # Should either have error OR done with fallback message
    if done_events:
        assert done_events[0].payload.get("full_narrative"), \
            "Empty Phase 1 response should not yield done event with empty narrative"

    assert error_events or done_events, \
        "Empty response should yield some event"
