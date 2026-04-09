"""
LLMResponse Serialization Tests

Consolidated tests for LLMResponse.to_dict() serialization:
1. Pydantic model serialization (structured_response → dict)
2. datetime field JSON serialization (model_dump(mode="json"))
3. budget_warnings inclusion and serialization

Bug fixes verified:
- LLMResponse.to_dict() properly serializes Pydantic models
- Line 85: model_dump(mode="json") converts datetime to ISO strings
"""

import json
import unittest
from datetime import datetime
import inspect
from typing import Any
from unittest.mock import Mock

from pydantic import BaseModel

import mvp_site.serialization as serialization_module
from mvp_site.llm_response import LLMResponse
from mvp_site.narrative_response_schema import NarrativeResponse
from mvp_site.serialization import MAX_STRING_LENGTH, json_default_serializer


class MockStructuredResponse(BaseModel):
    """Mock Pydantic model for testing."""

    narrative: str
    state_updates: dict[str, Any]
    entities_mentioned: list[str]


class TestLLMResponseSerialization(unittest.TestCase):
    """Test JSON serialization of LLMResponse with Pydantic structured_response."""

    def test_to_dict_serializes_pydantic_structured_response(self):
        """
        RED TEST: LLMResponse.to_dict() should serialize Pydantic models.

        This test SHOULD FAIL initially because to_dict() returns
        structured_response directly without calling .model_dump().
        """
        # Create Pydantic structured response
        structured = MockStructuredResponse(
            narrative="The knight enters the tavern.",
            state_updates={"hp": 15},
            entities_mentioned=["knight", "tavern"],
        )

        # Create LLMResponse with Pydantic model
        response = LLMResponse(
            narrative_text="The knight enters the tavern.",
            structured_response=structured,
            provider="gemini",
            model="gemini-1.5-flash",
        )

        # Get dict representation
        result_dict = response.to_dict()

        # ASSERTION 1: structured_response should be a dict (not Pydantic model)
        assert isinstance(result_dict["structured_response"], dict), (
            "structured_response should be serialized to dict"
        )

        # ASSERTION 2: Should be JSON serializable
        try:
            json_str = json.dumps(result_dict)
            assert isinstance(json_str, str)
        except TypeError as e:
            self.fail(f"to_dict() result should be JSON serializable, got: {e}")

        # ASSERTION 3: Verify content is preserved
        assert (
            result_dict["structured_response"]["narrative"]
            == "The knight enters the tavern."
        )
        assert result_dict["structured_response"]["state_updates"] == {"hp": 15}
        assert result_dict["structured_response"]["entities_mentioned"] == [
            "knight",
            "tavern",
        ]

    def test_to_dict_handles_dict_structured_response(self):
        """
        Verify to_dict() works when structured_response is already a dict.

        This ensures the fix doesn't break existing dict-based responses.
        """
        structured_dict = {
            "narrative": "The knight leaves.",
            "state_updates": {"location": "forest"},
        }

        response = LLMResponse(
            narrative_text="The knight leaves.",
            structured_response=structured_dict,
            provider="gemini",
            model="gemini-1.5-flash",
        )

        result_dict = response.to_dict()

        # Should return dict unchanged
        assert isinstance(result_dict["structured_response"], dict)
        assert result_dict["structured_response"]["narrative"] == "The knight leaves."

    def test_to_dict_handles_none_structured_response(self):
        """
        Verify to_dict() works when structured_response is None.
        """
        response = LLMResponse(
            narrative_text="Simple narrative.",
            structured_response=None,
            provider="gemini",
            model="gemini-1.5-flash",
        )

        result_dict = response.to_dict()

        # Should handle None gracefully
        assert result_dict["structured_response"] is None

    def test_budget_warnings_included_in_response_dict(self):
        """Budget warnings should be included in response dictionary."""
        warnings = [
            {
                "component": "system_instruction",
                "severity": "warning",
                "message": "System instruction exceeds 40% of budget",
                "measured_tokens": 50000,
                "allocated_tokens": 40000,
            }
        ]

        response = LLMResponse(
            narrative_text="Test narrative",
            structured_response={
                "narrative": "Test narrative",
                "planning": {"action": "test"},
            },
            budget_warnings=warnings,
        )

        response_dict = response.to_dict()

        assert "budget_warnings" in response_dict
        assert len(response_dict["budget_warnings"]) == 1
        assert response_dict["budget_warnings"][0]["component"] == "system_instruction"

    def test_budget_warnings_empty_list_when_none(self):
        """Budget warnings should be empty list when no warnings present."""
        response = LLMResponse(
            narrative_text="Test narrative",
            structured_response={"narrative": "Test narrative"},
        )

        response_dict = response.to_dict()

        assert "budget_warnings" in response_dict
        assert response_dict["budget_warnings"] == []

    def test_budget_warnings_serializable_to_json(self):
        """Budget warnings should be JSON-serializable."""
        warnings = [
            {
                "component": "game_state",
                "severity": "info",
                "message": "Game state compacted to fit budget",
                "measured_tokens": 15000,
                "allocated_tokens": 12000,
            }
        ]

        response = LLMResponse(
            narrative_text="Test narrative",
            structured_response={"narrative": "Test narrative"},
            budget_warnings=warnings,
        )

        response_dict = response.to_dict()
        json_str = json.dumps(response_dict)

        assert isinstance(json_str, str)

        parsed = json.loads(json_str)
        assert len(parsed["budget_warnings"]) == 1
        assert parsed["budget_warnings"][0]["component"] == "game_state"

    def test_legacy_response_includes_budget_warnings(self):
        """Legacy response path should include budget_warnings."""
        warnings = [
            {
                "component": "core_memories",
                "severity": "info",
                "message": "Core memories compacted to fit budget",
            }
        ]

        response = LLMResponse.create_legacy(
            narrative_text="Legacy narrative",
            model="gemini-3-flash-preview",
            budget_warnings=warnings,
        )

        response_dict = response.to_dict()

        assert "budget_warnings" in response_dict
        assert len(response_dict["budget_warnings"]) == 1

    def test_structured_response_includes_budget_warnings(self):
        """Structured response path should include budget_warnings."""
        structured = NarrativeResponse(
            narrative="Structured narrative",
            planning_block={"action": "test"},
        )
        warnings = [
            {
                "component": "entity_tracking",
                "severity": "warning",
                "message": "Entity tracking budget exceeded",
            }
        ]

        response = LLMResponse.create_from_structured_response(
            structured_response=structured,
            model="gemini-3-flash-preview",
            budget_warnings=warnings,
        )

        response_dict = response.to_dict()

        assert "budget_warnings" in response_dict
        assert len(response_dict["budget_warnings"]) == 1

    def test_to_dict_multiple_budget_warnings(self):
        """Multiple warnings should all be included."""
        warnings = [
            {
                "component": "system_instruction",
                "severity": "warning",
                "message": "System instruction exceeds budget",
            },
            {
                "component": "game_state",
                "severity": "info",
                "message": "Game state compacted",
            },
            {
                "component": "story_context",
                "severity": "warning",
                "message": "Story context truncated",
            },
        ]

        response = LLMResponse(
            narrative_text="Test narrative",
            structured_response={"narrative": "Test narrative"},
            budget_warnings=warnings,
        )

        response_dict = response.to_dict()

        assert len(response_dict["budget_warnings"]) == 3
        components = [
            warning["component"] for warning in response_dict["budget_warnings"]
        ]
        assert "system_instruction" in components
        assert "game_state" in components
        assert "story_context" in components


class SamplePydanticModelWithDatetime(BaseModel):
    """Sample model with datetime field to test JSON serialization."""

    name: str
    created_at: datetime
    count: int


class TestPydanticJsonSerialization(unittest.TestCase):
    """Test that Pydantic models with datetime fields serialize to JSON properly.

    Consolidated from test_pydantic_json_serialization.py.
    """

    def test_structured_response_with_datetime_serializes_to_json(self):
        """
        RED TEST: Pydantic model with datetime should serialize to JSON-compatible dict.

        When structured_response contains a Pydantic model with datetime fields,
        to_dict() should use model_dump(mode="json") to convert datetime to string.

        Without mode="json", datetime objects remain as Python datetime objects,
        causing json.dumps() to raise TypeError.
        """
        # Create Pydantic model with datetime
        model_data = SamplePydanticModelWithDatetime(
            name="Test Entity",
            created_at=datetime(2024, 1, 15, 10, 30, 0),
            count=42,
        )

        # Create LLMResponse with Pydantic structured_response
        response = LLMResponse(
            narrative_text="Test narrative",
            structured_response=model_data,  # Pydantic model
            provider="gemini",
            model="gemini-1.5-flash-002",
        )

        # Convert to dict
        response_dict = response.to_dict()

        # ASSERTION: structured_response should be a dict
        self.assertIsInstance(
            response_dict["structured_response"],
            dict,
            "structured_response should be converted to dict",
        )

        # ASSERTION: Should be JSON-serializable (this will fail if datetime not converted)
        try:
            json_str = json.dumps(response_dict)
            self.assertIsInstance(json_str, str)
        except TypeError as e:
            self.fail(
                f"response_dict should be JSON-serializable. "
                f"Failed with: {e}. "
                f"Likely cause: datetime not converted to string by model_dump(mode='json')"
            )

        # Parse back and verify datetime was converted to string
        parsed = json.loads(json_str)
        created_at_value = parsed["structured_response"]["created_at"]

        # ASSERTION: created_at should be a string in JSON (ISO format)
        self.assertIsInstance(
            created_at_value,
            str,
            f"created_at should be string in JSON, got {type(created_at_value)}",
        )

        # ASSERTION: Should be valid ISO format datetime string
        self.assertIn("2024-01-15", created_at_value)

    def test_datetime_structured_response_none_doesnt_crash(self):
        """Verify None structured_response doesn't crash."""
        response = LLMResponse(
            narrative_text="Test",
            structured_response=None,
            provider="gemini",
            model="test",
        )

        response_dict = response.to_dict()
        self.assertIsNone(response_dict["structured_response"])

    def test_datetime_structured_response_plain_dict_unchanged(self):
        """Verify plain dict structured_response works unchanged."""
        plain_dict = {"key": "value", "count": 123}
        response = LLMResponse(
            narrative_text="Test",
            structured_response=plain_dict,
            provider="gemini",
            model="test",
        )

        response_dict = response.to_dict()
        self.assertEqual(response_dict["structured_response"], plain_dict)


class _HugeStringMock(Mock):
    def __str__(self):
        return "x" * (MAX_STRING_LENGTH + 50)


class TestJsonDefaultSerializerMockHandling(unittest.TestCase):
    def test_serializer_module_avoids_unittest_mock_import(self):
        source = inspect.getsource(serialization_module)
        self.assertNotIn("from unittest.mock import Mock", source)

    def test_mock_serializes_to_string_representation(self):
        payload = {"complex": Mock(name="example_mock")}

        serialized = json.dumps(payload, default=json_default_serializer)
        parsed = json.loads(serialized)

        self.assertIsInstance(parsed["complex"], str)
        self.assertIn("example_mock", parsed["complex"])

    def test_mock_string_representation_is_truncated(self):
        payload = {"complex": _HugeStringMock()}

        serialized = json.dumps(payload, default=json_default_serializer)
        parsed = json.loads(serialized)

        self.assertTrue(parsed["complex"].endswith("...[truncated]"))
        self.assertEqual(
            len(parsed["complex"]),
            MAX_STRING_LENGTH + len("...[truncated]"),
        )


if __name__ == "__main__":
    unittest.main()
