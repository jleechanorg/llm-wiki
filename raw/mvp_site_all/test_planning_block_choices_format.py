"""TDD tests for PlanningBlock.choices canonical list format (PR #4534)."""

import json
import unittest

from mvp_site.campaign_upgrade import normalize_planning_block_choices
from mvp_site.narrative_response_schema import NarrativeResponse


class TestPlanningBlockChoicesCanonicalList(unittest.TestCase):
    """Planning choices are canonicalized to list[PlanningChoice]."""

    def test_schema_validation_accepts_list_format(self):
        planning_block = {
            "thinking": "Analyze options",
            "choices": [
                {
                    "id": "explore_cave",
                    "text": "Explore cave",
                    "description": "Enter the cave",
                    "risk_level": "medium",
                },
                {
                    "id": "talk_guard",
                    "text": "Talk to guard",
                    "description": "Ask for passage",
                    "risk_level": "low",
                },
            ],
        }
        schema = NarrativeResponse(narrative="Test", planning_block=planning_block)
        validated = schema.planning_block
        self.assertIsInstance(validated["choices"], list)
        self.assertEqual(validated["choices"][0]["id"], "explore_cave")
        self.assertEqual(validated["choices"][1]["id"], "talk_guard")

    def test_schema_validation_converts_dict_to_list(self):
        planning_block = {
            "thinking": "Analyze options",
            "choices": {
                "explore_cave": {
                    "text": "Explore cave",
                    "description": "Enter the cave",
                    "risk_level": "medium",
                },
                "talk_guard": {
                    "text": "Talk to guard",
                    "description": "Ask for passage",
                    "risk_level": "low",
                },
            },
        }
        schema = NarrativeResponse(narrative="Test", planning_block=planning_block)
        choices = schema.planning_block["choices"]
        self.assertIsInstance(choices, list)
        ids = [choice["id"] for choice in choices]
        self.assertIn("explore_cave", ids)
        self.assertIn("talk_guard", ids)

    def test_normalize_helper_converts_dict_to_list(self):
        planning_block = {
            "choices": {
                "option_a": {"text": "A", "description": "desc", "risk_level": "low"},
                "option_b": {"text": "B", "description": "desc", "risk_level": "low"},
            }
        }
        normalized = normalize_planning_block_choices(planning_block)
        self.assertIsInstance(normalized["choices"], list)
        self.assertEqual([c["id"] for c in normalized["choices"]], ["option_a", "option_b"])

    def test_normalize_helper_preserves_list_and_ids(self):
        planning_block = {
            "choices": [
                {"id": "one", "text": "One", "description": "desc", "risk_level": "low"},
                {"id": "two", "text": "Two", "description": "desc", "risk_level": "low"},
            ]
        }
        normalized = normalize_planning_block_choices(planning_block)
        self.assertIsInstance(normalized["choices"], list)
        self.assertEqual([c["id"] for c in normalized["choices"]], ["one", "two"])

    def test_duplicate_ids_get_deterministic_suffix_and_id_sync(self):
        planning_block = {
            "choices": [
                {"id": "attack", "text": "Attack", "description": "desc", "risk_level": "high"},
                {"id": "attack", "text": "Attack again", "description": "desc", "risk_level": "high"},
                {"id": "attack", "text": "Attack third", "description": "desc", "risk_level": "high"},
            ]
        }
        normalized = normalize_planning_block_choices(planning_block)
        ids = [c["id"] for c in normalized["choices"]]
        self.assertEqual(ids, ["attack", "attack_1", "attack_2"])

    def test_json_string_input_normalizes_to_list(self):
        planning_block_json = json.dumps(
            {
                "thinking": "Test",
                "choices": [
                    {
                        "id": "choice_1",
                        "text": "Choice 1",
                        "description": "First choice",
                        "risk_level": "low",
                    }
                ],
            }
        )
        normalized = normalize_planning_block_choices(planning_block_json)
        self.assertIsInstance(normalized["choices"], list)
        self.assertEqual(normalized["choices"][0]["id"], "choice_1")


if __name__ == "__main__":
    unittest.main()
