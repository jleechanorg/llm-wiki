"""Tests for list-canonical planning_block normalization."""

import os
import unittest

os.environ["WORLDAI_DEV_MODE"] = "true"
os.environ["TESTING_AUTH_BYPASS"] = "true"
os.environ["USE_MOCKS"] = "true"
os.environ["MOCK_SERVICES_MODE"] = "true"

from mvp_site import campaign_upgrade


class TestNormalizePlanningBlockChoices(unittest.TestCase):
    """normalize_planning_block_choices returns list-format choices."""

    def test_list_preserves_canonical_ids(self):
        planning_block = {
            "choices": [
                {"id": "level_up_now", "text": "Level Up", "description": "desc", "risk_level": "safe"},
                {"id": "continue_adventuring", "text": "Continue", "description": "desc", "risk_level": "safe"},
            ]
        }
        result = campaign_upgrade.normalize_planning_block_choices(planning_block)
        self.assertEqual(
            [choice["id"] for choice in result["choices"]],
            ["level_up_now", "continue_adventuring"],
        )

    def test_dict_input_converts_to_list_and_uses_keys_as_id(self):
        planning_block = {
            "choices": {
                "search_the_room": {"text": "Search", "description": "desc", "risk_level": "low"},
                "talk_to_guard": {"text": "Talk", "description": "desc", "risk_level": "low"},
            }
        }
        result = campaign_upgrade.normalize_planning_block_choices(planning_block)
        ids = [choice["id"] for choice in result["choices"]]
        self.assertEqual(ids, ["search_the_room", "talk_to_guard"])

    def test_missing_or_empty_ids_fallback_to_text(self):
        planning_block = {
            "choices": [
                {"id": "", "text": "Inspect Artifact", "description": "desc", "risk_level": "low"},
                {"id": "   ", "text": "Leave Room", "description": "desc", "risk_level": "low"},
            ]
        }
        result = campaign_upgrade.normalize_planning_block_choices(planning_block)
        ids = [choice["id"] for choice in result["choices"]]
        self.assertEqual(ids, ["inspect_artifact", "leave_room"])

    def test_duplicate_ids_get_deterministic_suffix(self):
        planning_block = {
            "choices": [
                {"id": "attack", "text": "Attack", "description": "desc", "risk_level": "high"},
                {"id": "attack", "text": "Attack Bow", "description": "desc", "risk_level": "high"},
            ]
        }
        result = campaign_upgrade.normalize_planning_block_choices(planning_block)
        self.assertEqual(
            [choice["id"] for choice in result["choices"]],
            ["attack", "attack_1"],
        )

    def test_empty_inputs_become_empty_list(self):
        self.assertEqual(
            campaign_upgrade.normalize_planning_block_choices(None)["choices"],
            [],
        )
        self.assertEqual(
            campaign_upgrade.normalize_planning_block_choices({})["choices"],
            [],
        )


if __name__ == "__main__":
    unittest.main()
