"""End-to-end tests for streaming SSE contract: character / think / god modes.

These tests verify the streaming endpoint /interaction/stream returns correct SSE
done payloads for each mode. Only the LOWEST-LEVEL Gemini API call is mocked
(generate_content_stream_sync), letting all internal routing, prompt-building,
JSON-parsing, and orchestration logic run normally.

TDD REGRESSION RATIONALE
-------------------------
The CI "Mock API" job originally used MOCK_SERVICES_MODE=true, which swaps the
entire LLM service module with a simplified fake that uses ad-hoc string matching
on prompt content:

    if "god mode:" in prompt.lower() or "god:" in prompt.lower():
        return json.dumps(GOD_MODE_RESPONSE, indent=2)

Input "GOD_MODE_UPDATE_STATE:{...}" does NOT contain "god mode:" or "god:", so
the mock fell back to FULL_STRUCTURED_RESPONSE which has god_mode_response: "".
The streaming done payload validator then raised:
    "god mode stream done payload missing god_mode_response"

The correct mock pattern (used in test_end2end/) patches ONLY the external API
call at the boundary, letting all internal logic run.  This test suite documents
and enforces that pattern.

See roadmap/2026-02-22-streaming-contract-ci-failure-postmortem.md
"""
from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

# Set before importing app modules so the clock-skew patch fires correctly.
os.environ.setdefault("TESTING_AUTH_BYPASS", "true")
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")
os.environ.setdefault("CEREBRAS_API_KEY", "test-cerebras-key")

from mvp_site import main
from mvp_site.tests.fake_firestore import FakeFirestoreClient
from mvp_site.tests.test_end2end import End2EndBaseTestCase

# ---------------------------------------------------------------------------
# Canned streaming responses (each is split into 3 chunks to simulate real SSE)
# ---------------------------------------------------------------------------

_CHARACTER_RESPONSE = {
    "narrative": "You whisper a warning to your companions. They nod gravely, hands moving to weapons.",
    "god_mode_response": "",
    "planning_block": {
        "thinking": "The player is being cautious.",
        "choices": {
            "advance": {"text": "Advance", "description": "Move forward", "risk_level": "medium"},
            "wait": {"text": "Wait", "description": "Hold position", "risk_level": "low"},
        },
    },
    "session_header": "[SESSION_HEADER]\nTimestamp: Evening\nLocation: Dungeon\nStatus: Active",
    "resources": "HP: 45/50",
    "entities_mentioned": ["companions"],
    "location_confirmed": "Dungeon",
    "state_updates": {},
    "debug_info": {"dm_notes": ["Cautious approach"], "state_rationale": "No state changes"},
}

_THINK_RESPONSE = {
    "narrative": "You pause to assess the tactical situation carefully.",
    "god_mode_response": "",
    "planning_block": {
        "thinking": "Consider all options before acting.",
        "choices": {
            "stealth": {"text": "Stealth approach", "description": "Sneak past guards", "risk_level": "medium"},
            "negotiate": {"text": "Negotiate", "description": "Talk your way through", "risk_level": "low"},
            "fight": {"text": "Fight", "description": "Direct combat", "risk_level": "high"},
        },
    },
    "session_header": "[SESSION_HEADER]\nTimestamp: Evening\nLocation: Dungeon\nStatus: Active",
    "resources": "HP: 45/50",
    "entities_mentioned": [],
    "location_confirmed": "Dungeon",
    "state_updates": {},
    "debug_info": {"dm_notes": ["Think mode"], "state_rationale": "No state changes"},
}

_GOD_MODE_RESPONSE = {
    "narrative": "",
    "god_mode_response": (
        "God Mode Overview:\n"
        "- Player HP: 45/50\n"
        "- Location: Dungeon\n"
        "- Custom campaign state updated: streaming_smoke_mode=contract"
    ),
    "planning_block": {
        "thinking": "Administrative command processed.",
        "choices": {
            "return_story": {"text": "Return to Story", "description": "Exit god mode", "risk_level": "safe"},
        },
    },
    "session_header": "[SESSION_HEADER]\nTimestamp: Evening\nLocation: Dungeon\nStatus: Active",
    "resources": "HP: 45/50",
    "entities_mentioned": [],
    "location_confirmed": "Dungeon",
    "state_updates": {},
    "debug_info": {"dm_notes": ["God mode query"], "state_rationale": "State updated"},
}


def _streaming_chunks(response_dict: dict) -> list[str]:
    """Split a JSON dict into 3 string chunks simulating real SSE token streaming."""
    full = json.dumps(response_dict)
    third = max(1, len(full) // 3)
    return [full[:third], full[third : 2 * third], full[2 * third :]]


def _parse_sse_events(response_data: bytes) -> list[dict]:
    """Extract all SSE event payloads from a raw SSE byte stream."""
    events: list[dict] = []
    for block in response_data.decode("utf-8").split("\n\n"):
        block = block.strip()
        if block.startswith("data: "):
            try:
                events.append(json.loads(block[6:]))
            except json.JSONDecodeError:
                pass
    return events


def _done_event(events: list[dict]) -> dict | None:
    for e in events:
        if e.get("type") == "done":
            return e
    return None


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

_CAMPAIGN_ID = "campaign-streaming-contract"
_GAME_STATE = {
    "user_id": "test-user-streaming-contract",
    "story_text": "You stand at the entrance to the dungeon.",
    "player_character_data": {
        "entity_id": "player_character",
        "display_name": "Thorin",
        "name": "Thorin",
        "hp_current": 45,
        "hp_max": 50,
        "level": 5,
        "class_name": "Fighter",
    },
    "world_data": {
        "current_location_name": "Dungeon",
        "world_time": {
            "year": 1492,
            "month": "Mirtul",
            "day": 10,
            "hour": 20,
            "minute": 0,
            "time_of_day": "Evening",
        },
    },
    "npc_data": {},
    "combat_state": {"in_combat": False},
    "custom_campaign_state": {},
}


def _setup_campaign(fake_firestore: FakeFirestoreClient, user_id: str) -> None:
    """Populate fake Firestore with the campaign and game-state documents."""
    base = (
        fake_firestore.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(_CAMPAIGN_ID)
    )
    base.set(
        {
            "title": "Streaming Contract Test",
            "setting": "Fantasy dungeon",
            "selected_prompts": ["narrative", "mechanics"],
            "use_default_world": False,
        }
    )
    base.collection("game_states").document("current_state").set(_GAME_STATE)


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------


class TestStreamingContractEnd2End(End2EndBaseTestCase):
    """Streaming SSE contract: character / think / god done-payloads are correct.

    Mock strategy: patch ONLY mvp_site.llm_providers.gemini_provider.generate_content_stream_sync
    This is the lowest external boundary — all internal routing, agent selection,
    prompt building, JSON parsing, and orchestration run with real production code.
    """

    CREATE_APP = main.create_app
    AUTH_PATCH_TARGET = "mvp_site.main.auth.verify_id_token"
    TEST_USER_ID = "test-user-streaming-contract"

    def setUp(self) -> None:
        super().setUp()
        # CRITICAL: do NOT set MOCK_SERVICES_MODE=true — that is the fragile pattern
        # we are replacing.  Force it off so the real code path runs.
        os.environ["MOCK_SERVICES_MODE"] = "false"
        os.environ["ENABLE_EXPLICIT_CACHE"] = "false"

    def _stream(
        self,
        user_input: str,
        mode: str,
        llm_response: dict,
    ) -> tuple[int, list[dict]]:
        """Post to streaming endpoint with a mocked LLM response.

        Patches:
          - mvp_site.firestore_service.get_db → FakeFirestoreClient
          - mvp_site.llm_providers.gemini_provider.generate_content_stream_sync
            → iterator of 3 string chunks that concatenate to valid JSON

        IMPORTANT: response.data is accessed inside the patch context because Flask's
        test client consumes streaming responses lazily (the generator runs when .data
        is accessed, not during client.post()).  If .data were accessed outside the
        with-patch block the mock would already be removed and the real API would run.

        Returns (status_code, parsed_sse_events).
        """
        fake_firestore = FakeFirestoreClient()
        _setup_campaign(fake_firestore, self.TEST_USER_ID)

        chunks = _streaming_chunks(llm_response)

        with (
            patch("mvp_site.firestore_service.get_db", return_value=fake_firestore),
            patch(
                "mvp_site.llm_providers.gemini_provider.generate_content_stream_sync",
                return_value=iter(chunks),
            ),
        ):
            response = self.client.post(
                f"/api/campaigns/{_CAMPAIGN_ID}/interaction/stream",
                headers=self.test_headers,
                json={"input": user_input, "mode": mode},
            )
            # CRITICAL: Flask test client consumes streaming response lazily — response.data
            # triggers generator execution.  Access .data inside the patch context so the
            # mock is still active when generate_content_stream_sync is called.
            events = _parse_sse_events(response.data)

        return response.status_code, events

    # ------------------------------------------------------------------
    # character mode
    # ------------------------------------------------------------------

    def test_character_streaming_contract_returns_narrative(self) -> None:
        """character mode streaming done payload contains non-empty narrative."""
        status, events = self._stream(
            "I whisper quietly to my companions about the danger ahead.",
            "character",
            _CHARACTER_RESPONSE,
        )
        self.assertEqual(status, 200)
        done = _done_event(events)
        self.assertIsNotNone(done, f"No done event in: {[e.get('type') for e in events]}")
        payload = done["payload"]
        structured = payload.get("structured_response") or {}
        narrative = payload.get("narrative") or structured.get("narrative")
        self.assertIsInstance(narrative, str)
        self.assertTrue(narrative.strip(), "character done payload must have non-empty narrative")

    # ------------------------------------------------------------------
    # think mode
    # ------------------------------------------------------------------

    def test_think_streaming_contract_returns_planning_block(self) -> None:
        """think mode streaming done payload contains a planning_block dict."""
        status, events = self._stream(
            "THINK: Evaluate options for bypassing the warded gate.",
            "think",
            _THINK_RESPONSE,
        )
        self.assertEqual(status, 200)
        done = _done_event(events)
        self.assertIsNotNone(done, f"No done event in: {[e.get('type') for e in events]}")
        payload = done["payload"]
        structured = payload.get("structured_response") or {}
        planning_block = payload.get("planning_block") or structured.get("planning_block")
        self.assertIsInstance(planning_block, dict, "think done payload must have planning_block dict")

    # ------------------------------------------------------------------
    # god mode — GOD MODE: prefix (plain text)
    # ------------------------------------------------------------------

    def test_god_streaming_contract_god_mode_prefix_input(self) -> None:
        """GOD MODE: prefix input → done payload has non-empty god_mode_response."""
        status, events = self._stream(
            "GOD MODE: Provide a brief overview of the current campaign state.",
            "god",
            _GOD_MODE_RESPONSE,
        )
        self.assertEqual(status, 200)
        done = _done_event(events)
        self.assertIsNotNone(done, f"No done event in: {[e.get('type') for e in events]}")
        payload = done["payload"]
        structured = payload.get("structured_response") or {}
        god_mode_response = payload.get("god_mode_response") or structured.get("god_mode_response")
        self.assertIsInstance(god_mode_response, str)
        self.assertTrue(god_mode_response.strip(), "god done payload must have non-empty god_mode_response")

    # ------------------------------------------------------------------
    # god mode — GOD_MODE_UPDATE_STATE: prefix (structured state update)
    # THE CRITICAL REGRESSION: this input FAILED with MOCK_SERVICES_MODE=true
    # ------------------------------------------------------------------

    def test_god_streaming_contract_state_update_input(self) -> None:
        """GOD_MODE_UPDATE_STATE:{...} input → done payload has non-empty god_mode_response.

        REGRESSION TEST: This is the exact input used in the smoke test's
        god_streaming_contract scenario.  With the old MOCK_SERVICES_MODE=true
        approach, mock_llm_service.py could not detect this input as god mode
        (it only matched 'god mode:' / 'god:' substrings), so it fell back to
        FULL_STRUCTURED_RESPONSE which has god_mode_response: "" — causing the
        streaming contract validator to raise:
            "god mode stream done payload missing god_mode_response"

        With the correct mock pattern (patching generate_content_stream_sync
        at the external API boundary), the internal code path is agnostic to
        input format and always gets a proper god_mode_response from the mock.
        """
        status, events = self._stream(
            'GOD_MODE_UPDATE_STATE:{"custom_campaign_state":{"streaming_smoke_mode":"contract"}}',
            "god",
            _GOD_MODE_RESPONSE,
        )
        self.assertEqual(status, 200)
        done = _done_event(events)
        self.assertIsNotNone(done, f"No done event in: {[e.get('type') for e in events]}")
        payload = done["payload"]
        structured = payload.get("structured_response") or {}
        god_mode_response = payload.get("god_mode_response") or structured.get("god_mode_response")
        self.assertIsInstance(god_mode_response, str)
        self.assertTrue(
            god_mode_response.strip(),
            "god done payload must have non-empty god_mode_response "
            "(regression: MOCK_SERVICES_MODE=true module-swap failed for this input)",
        )


if __name__ == "__main__":
    unittest.main()
