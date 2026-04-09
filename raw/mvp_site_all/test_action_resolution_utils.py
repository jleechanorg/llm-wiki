"""Tests for action_resolution_utils helper functions."""

import unittest
from typing import Any

from mvp_site.action_resolution_utils import (
    add_action_resolution_to_response,
    extract_dice_audit_events_from_action_resolution,
    extract_dice_rolls_from_action_resolution,
    has_action_resolution_dice,
)


class TestExtractDiceRollsFromActionResolution(unittest.TestCase):
    """Test extract_dice_rolls_from_action_resolution function"""

    def test_extract_single_roll(self):
        """Test extraction of single dice roll"""
        action_resolution = {
            "mechanics": {
                "rolls": [
                    {
                        "purpose": "Attack",
                        "notation": "1d20+5",
                        "result": 17,
                        "total": 22,
                        "dc": None,
                        "success": None,
                    }
                ]
            }
        }
        result = extract_dice_rolls_from_action_resolution(action_resolution)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "1d20+5 = 22 (Attack)")

    def test_extract_roll_with_dc_and_success(self):
        """Test extraction of roll with DC and success"""
        action_resolution = {
            "mechanics": {
                "rolls": [
                    {
                        "purpose": "Stealth (Soul Siphon Deception)",
                        "notation": "1d20+149",
                        "result": 164,
                        "total": 313,
                        "dc": 45,
                        "success": True,
                    }
                ]
            }
        }
        result = extract_dice_rolls_from_action_resolution(action_resolution)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0],
            "1d20+149 = 313 vs DC 45 - Success (Stealth (Soul Siphon Deception))",
        )

    def test_extract_roll_with_dc_and_failure(self):
        """Test extraction of roll with DC and failure"""
        action_resolution = {
            "mechanics": {
                "rolls": [
                    {
                        "purpose": "Persuasion",
                        "notation": "1d20+5",
                        "result": 12,
                        "total": 17,
                        "dc": 18,
                        "success": False,
                    }
                ]
            }
        }
        result = extract_dice_rolls_from_action_resolution(action_resolution)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "1d20+5 = 17 vs DC 18 - Failure (Persuasion)")

    def test_extract_multiple_rolls(self):
        """Test extraction of multiple dice rolls"""
        action_resolution = {
            "mechanics": {
                "rolls": [
                    {
                        "purpose": "Parallel Logic Coordination",
                        "notation": "1d20+42",
                        "result": 56,
                        "total": 98,
                        "dc": 25,
                        "success": True,
                    },
                    {
                        "purpose": "Stealth (Soul Siphon Deception)",
                        "notation": "1d20+149",
                        "result": 164,
                        "total": 313,
                        "dc": 45,
                        "success": True,
                    },
                ]
            }
        }
        result = extract_dice_rolls_from_action_resolution(action_resolution)
        self.assertEqual(len(result), 2)
        self.assertEqual(
            result[0], "1d20+42 = 98 vs DC 25 - Success (Parallel Logic Coordination)"
        )
        self.assertEqual(
            result[1],
            "1d20+149 = 313 vs DC 45 - Success (Stealth (Soul Siphon Deception))",
        )

    def test_extract_empty_rolls(self):
        """Test extraction with empty rolls array"""
        action_resolution = {"mechanics": {"rolls": []}}
        result = extract_dice_rolls_from_action_resolution(action_resolution)
        self.assertEqual(result, [])

    def test_extract_no_mechanics(self):
        """Test extraction with no mechanics field"""
        action_resolution = {}
        result = extract_dice_rolls_from_action_resolution(action_resolution)
        self.assertEqual(result, [])

    def test_extract_no_rolls_field(self):
        """Test extraction with no rolls field"""
        action_resolution = {"mechanics": {}}
        result = extract_dice_rolls_from_action_resolution(action_resolution)
        self.assertEqual(result, [])

    def test_extract_invalid_roll_format(self):
        """Test extraction handles invalid roll format gracefully"""
        action_resolution = {
            "mechanics": {
                "rolls": [
                    {"purpose": "Attack"},  # Missing notation and result
                    "not a dict",  # Invalid type
                ]
            }
        }
        result = extract_dice_rolls_from_action_resolution(action_resolution)
        self.assertEqual(result, [])

    def test_extract_roll_without_purpose(self):
        """Test extraction of roll without purpose"""
        action_resolution = {
            "mechanics": {
                "rolls": [
                    {
                        "notation": "1d20+5",
                        "result": 17,
                        "total": 22,
                        "dc": None,
                        "success": None,
                    }
                ]
            }
        }
        result = extract_dice_rolls_from_action_resolution(action_resolution)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "1d20+5 = 22")


class TestExtractDiceAuditEventsFromActionResolution(unittest.TestCase):
    """Test extract_dice_audit_events_from_action_resolution function"""

    def test_extract_string_audit_events(self):
        """Test extraction of string audit events"""
        action_resolution = {
            "mechanics": {
                "audit_events": [
                    {
                        "source": "code_execution",
                        "label": "Attack",
                        "notation": "1d20+5",
                        "rolls": [12],
                        "modifier": 5,
                        "total": 17,
                    },
                    {
                        "source": "code_execution",
                        "label": "Damage",
                        "notation": "1d8+3",
                        "rolls": [5],
                        "modifier": 3,
                        "total": 8,
                    },
                ]
            }
        }
        result = extract_dice_audit_events_from_action_resolution(action_resolution)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["label"], "Attack")
        self.assertEqual(result[1]["label"], "Damage")

    def test_extract_dict_audit_events(self):
        """Test extraction of dict audit events (converted to string)"""
        action_resolution = {
            "mechanics": {
                "audit_events": [
                    {"type": "attack_roll", "result": 17},
                    {"type": "damage_roll", "result": 8},
                ]
            }
        }
        result = extract_dice_audit_events_from_action_resolution(action_resolution)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], dict)
        self.assertIsInstance(result[1], dict)

    def test_extract_empty_audit_events(self):
        """Test extraction with empty audit_events array"""
        action_resolution = {"mechanics": {"audit_events": []}}
        result = extract_dice_audit_events_from_action_resolution(action_resolution)
        self.assertEqual(result, [])


class TestAddActionResolutionNormalization(unittest.TestCase):
    """Test add_action_resolution_to_response normalization behavior."""

    def test_add_action_resolution_normalizes_missing_total(self):
        class MockResponse:
            def __init__(self) -> None:
                self.action_resolution = {
                    "mechanics": {
                        "rolls": [
                            {
                                "purpose": "Attack",
                                "notation": "1d20+5",
                                "result": 8,
                                "dc": 15,
                                "success": False,
                            }
                        ]
                    }
                }
                self.outcome_resolution = None

        mock = MockResponse()
        unified_response: dict[str, Any] = {}
        add_action_resolution_to_response(mock, unified_response)

        rolls = unified_response["action_resolution"]["mechanics"]["rolls"]
        self.assertEqual(rolls[0].get("total"), 8)

    def test_add_action_resolution_normalizes_label_to_purpose(self):
        """Test that 'label' is normalized to 'purpose' for frontend compatibility."""

        class MockResponse:
            def __init__(self) -> None:
                self.action_resolution = {
                    "mechanics": {
                        "rolls": [
                            {
                                "label": "Level 9 HP Increase",
                                "notation": "1d6-1",
                                "total": 2,
                            }
                        ]
                    }
                }
                self.outcome_resolution = None

        mock = MockResponse()
        unified_response: dict[str, Any] = {}
        add_action_resolution_to_response(mock, unified_response)

        rolls = unified_response["action_resolution"]["mechanics"]["rolls"]
        self.assertEqual(rolls[0].get("purpose"), "Level 9 HP Increase")
        # Label should still be present
        self.assertEqual(rolls[0].get("label"), "Level 9 HP Increase")

    def test_add_action_resolution_preserves_existing_purpose(self):
        """Test that existing 'purpose' is not overwritten by 'label'."""

        class MockResponse:
            def __init__(self) -> None:
                self.action_resolution = {
                    "mechanics": {
                        "rolls": [
                            {
                                "purpose": "Attack Roll",
                                "label": "Should Not Override",
                                "notation": "1d20+5",
                                "total": 18,
                            }
                        ]
                    }
                }
                self.outcome_resolution = None

        mock = MockResponse()
        unified_response: dict[str, Any] = {}
        add_action_resolution_to_response(mock, unified_response)

        rolls = unified_response["action_resolution"]["mechanics"]["rolls"]
        self.assertEqual(rolls[0].get("purpose"), "Attack Roll")

    def test_extract_no_mechanics(self):
        """Test extraction with no mechanics field"""
        action_resolution = {}
        result = extract_dice_audit_events_from_action_resolution(action_resolution)
        self.assertEqual(result, [])


class TestAddActionResolutionToResponse(unittest.TestCase):
    """Test add_action_resolution_to_response function"""

    def test_does_not_extract_dice_rolls_from_action_resolution(self):
        """Test that dice_rolls are not extracted from action_resolution"""

        class MockResponse:
            def __init__(self):
                self.action_resolution = {
                    "mechanics": {
                        "rolls": [
                            {
                                "purpose": "Attack",
                                "notation": "1d20+5",
                                "result": 17,
                                "total": 22,
                                "dc": 18,
                                "success": False,
                            }
                        ]
                    }
                }

        mock_response = MockResponse()
        unified_response = {}

        add_action_resolution_to_response(mock_response, unified_response)

        self.assertNotIn("dice_rolls", unified_response)

    def test_does_not_override_existing_dice_rolls(self):
        """Test that add_action_resolution_to_response does not overwrite dice_rolls"""

        class MockResponse:
            def __init__(self):
                self.action_resolution = {
                    "mechanics": {
                        "rolls": [
                            {
                                "purpose": "Attack",
                                "notation": "1d20+5",
                                "result": 17,
                                "total": 22,
                            }
                        ]
                    }
                }
                self.dice_rolls = ["Existing roll"]

        mock_response = MockResponse()
        unified_response = {"dice_rolls": ["Existing roll"]}

        add_action_resolution_to_response(mock_response, unified_response)

        self.assertEqual(unified_response["dice_rolls"], ["Existing roll"])

    def test_does_not_extract_dice_audit_events(self):
        """Test that dice_audit_events are not extracted from action_resolution"""

        class MockResponse:
            def __init__(self):
                self.action_resolution = {
                    "mechanics": {"audit_events": ["Event 1", "Event 2"]}
                }

        mock_response = MockResponse()
        unified_response = {}

        add_action_resolution_to_response(mock_response, unified_response)

        self.assertNotIn("dice_audit_events", unified_response)

    def test_no_action_resolution_no_extraction(self):
        """Test that nothing is extracted if action_resolution is missing"""

        class MockResponse:
            pass

        mock_response = MockResponse()
        unified_response = {}

        add_action_resolution_to_response(mock_response, unified_response)

        # Should not have dice_rolls or dice_audit_events
        self.assertNotIn("dice_rolls", unified_response)
        self.assertNotIn("dice_audit_events", unified_response)

    def test_preserves_empty_dice_rolls(self):
        """Test that empty dice_rolls stays untouched when action_resolution has rolls."""

        class MockResponse:
            def __init__(self):
                self.action_resolution = {
                    "mechanics": {
                        "rolls": [
                            {
                                "purpose": "Persuasion",
                                "notation": "1d20+5",
                                "result": 12,
                                "total": 17,
                                "dc": 18,
                                "success": False,
                            }
                        ]
                    }
                }

        mock_response = MockResponse()
        unified_response = {"dice_rolls": []}

        add_action_resolution_to_response(mock_response, unified_response)

        self.assertEqual(unified_response["dice_rolls"], [])

    def test_legacy_outcome_resolution_backfills_action_resolution(self):
        """Test that legacy payloads with only outcome_resolution backfill action_resolution."""

        class MockResponse:
            def __init__(self):
                self.action_resolution = None
                self.outcome_resolution = {
                    "mechanics": {
                        "rolls": [
                            {
                                "purpose": "Legacy Attack",
                                "notation": "1d20+3",
                                "result": 14,
                                "total": 17,
                            }
                        ]
                    }
                }

        mock_response = MockResponse()
        unified_response: dict[str, Any] = {}

        add_action_resolution_to_response(mock_response, unified_response)

        # action_resolution must be populated from outcome_resolution
        self.assertIn("action_resolution", unified_response)
        self.assertIn("outcome_resolution", unified_response)
        rolls = unified_response["action_resolution"]["mechanics"]["rolls"]
        self.assertEqual(rolls[0]["purpose"], "Legacy Attack")

    def test_legacy_outcome_resolution_no_action_resolution_attr(self):
        """Test backfill when structured_response has no action_resolution attribute at all."""

        class MockResponse:
            def __init__(self):
                self.outcome_resolution = {"mechanics": {"rolls": []}}

        mock_response = MockResponse()
        unified_response: dict[str, Any] = {}

        add_action_resolution_to_response(mock_response, unified_response)

        self.assertIn("action_resolution", unified_response)
        self.assertIn("outcome_resolution", unified_response)


class TestHasActionResolutionDice(unittest.TestCase):
    """Test has_action_resolution_dice helper."""

    def test_has_action_resolution_dice_true_for_rolls(self):
        action_resolution = {
            "mechanics": {"rolls": [{"notation": "1d20+5", "result": 12}]}
        }
        self.assertTrue(has_action_resolution_dice(action_resolution))

    def test_has_action_resolution_dice_true_for_audit_events(self):
        action_resolution = {"mechanics": {"audit_events": [{"label": "Attack"}]}}
        self.assertTrue(has_action_resolution_dice(action_resolution))

    def test_has_action_resolution_dice_false_for_empty(self):
        action_resolution = {"mechanics": {"rolls": [], "audit_events": []}}
        self.assertFalse(has_action_resolution_dice(action_resolution))

    def test_has_action_resolution_dice_false_for_invalid(self):
        self.assertFalse(has_action_resolution_dice(None))
        self.assertFalse(has_action_resolution_dice({}))
