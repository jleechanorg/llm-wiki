"""
Unit tests for the /api/campaigns/<id>/spells endpoint.

Covers the fallback message path (lines 2568-2574 in main.py):
when spell_slots are present but spells_known, cantrips, and spells_prepared
are all empty, the summary must prompt the user to set up their spell list.
"""

import os
import sys
import unittest
from unittest.mock import patch

os.environ["TESTING_AUTH_BYPASS"] = "true"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import create_app  # noqa: E402


_CAMPAIGN_ID = "test-spells-campaign"
_BYPASS_HEADERS = {
    "X-Test-Bypass-Auth": "true",
    "X-Test-User-Id": "test-user-spells",
}

_FALLBACK_MESSAGE = 'No spell list recorded. Type: "What spells do I know?" to set them up.'


class _FakeGameState:
    """Minimal game-state stand-in returned by mocked get_campaign_game_state."""

    def __init__(self, pc_data: dict):
        self.player_character_data = pc_data


class TestSpellsEndpointFallback(unittest.TestCase):
    """Tests for the spells summary fallback message path."""

    def setUp(self) -> None:
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def _get_spells(self, pc_data: dict):
        """Call the spells endpoint with a mocked game state."""
        fake_state = _FakeGameState(pc_data)
        with patch(
            "firestore_service.get_campaign_game_state",
            return_value=fake_state,
        ):
            return self.client.get(
                f"/api/campaigns/{_CAMPAIGN_ID}/spells",
                headers=_BYPASS_HEADERS,
            )

    # ------------------------------------------------------------------
    # RED → GREEN: fallback message when slots present but no spell list
    # ------------------------------------------------------------------

    def test_fallback_message_shown_when_slots_present_but_no_spells(self) -> None:
        """Spell slots with no known/cantrip/prepared spells must show the fallback prompt."""
        pc_data = {
            "spell_slots": {
                "1": {"current": 4, "max": 4},
            },
        }
        response = self._get_spells(pc_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"), msg=f"Unexpected failure: {data}")
        self.assertIn(
            _FALLBACK_MESSAGE,
            data["spells_summary"],
            msg="Fallback prompt must appear when spell slots exist but no spell list is recorded",
        )

    def test_fallback_shown_with_resources_spell_slots_format(self) -> None:
        """Spell slots inside resources dict also trigger the fallback when no spells recorded."""
        pc_data = {
            "resources": {
                "spell_slots": {
                    "level_1": {"used": 1, "max": 4},
                }
            },
        }
        response = self._get_spells(pc_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"), msg=f"Unexpected failure: {data}")
        self.assertIn(
            _FALLBACK_MESSAGE,
            data["spells_summary"],
            msg="Fallback prompt must appear for resources.spell_slots format",
        )

    def test_no_fallback_when_spells_known_present(self) -> None:
        """When spells_known is populated, the fallback message must NOT appear."""
        pc_data = {
            "spell_slots": {"1": {"current": 4, "max": 4}},
            "spells_known": [{"name": "Magic Missile", "level": 1}],
        }
        response = self._get_spells(pc_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"), msg=f"Unexpected failure: {data}")
        self.assertNotIn(
            _FALLBACK_MESSAGE,
            data["spells_summary"],
            msg="Fallback prompt must NOT appear when spells_known is populated",
        )

    def test_no_fallback_when_cantrips_present(self) -> None:
        """When cantrips are populated, the fallback message must NOT appear."""
        pc_data = {
            "spell_slots": {"1": {"current": 4, "max": 4}},
            "cantrips": [{"name": "Fire Bolt"}],
        }
        response = self._get_spells(pc_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"), msg=f"Unexpected failure: {data}")
        self.assertNotIn(
            _FALLBACK_MESSAGE,
            data["spells_summary"],
            msg="Fallback prompt must NOT appear when cantrips are populated",
        )

    def test_no_fallback_when_no_spell_slots_at_all(self) -> None:
        """Non-spellcasters with no slots must not see the fallback prompt."""
        pc_data = {
            "class_name": "Fighter",
        }
        response = self._get_spells(pc_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"), msg=f"Unexpected failure: {data}")
        self.assertNotIn(
            _FALLBACK_MESSAGE,
            data["spells_summary"],
            msg="Fallback prompt must NOT appear for non-spellcasters",
        )

    def test_campaign_not_found_returns_404(self) -> None:
        """Missing game state must return 404."""
        with patch(
            "firestore_service.get_campaign_game_state",
            return_value=None,
        ):
            response = self.client.get(
                f"/api/campaigns/{_CAMPAIGN_ID}/spells",
                headers=_BYPASS_HEADERS,
            )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
