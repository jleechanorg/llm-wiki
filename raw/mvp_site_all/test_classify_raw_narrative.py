"""Unit tests for _classify_raw_narrative helper.

TDD RED phase: these tests define the contract for the helper before it exists.
"""

import json
import unittest

from mvp_site.llm_service import _classify_raw_narrative
from mvp_site.narrative_response_schema import JSON_PARSE_FALLBACK_MARKER


class TestClassifyRawNarrative(unittest.TestCase):
    """Contract tests for _classify_raw_narrative(text) -> bool.

    Returns True  when text is a genuine string narrative that should be used
    as the streaming fallback (non-empty, not the marker, not JSON non-string).
    Returns False for empty, marker, or JSON containers/scalars.
    """

    # --- True cases (should use as fallback) ---

    def test_plain_prose_returns_true(self):
        assert _classify_raw_narrative("You wait in silence.")

    def test_short_valid_narrative_returns_true(self):
        """Short narratives (≤20 chars) must NOT be rejected."""
        assert _classify_raw_narrative("You wait.")

    def test_json_quoted_string_narrative_returns_true(self):
        """json.loads('"You wait."') returns str — must be treated as narrative."""
        text = json.dumps("You wait.")  # produces '"You wait."'
        assert _classify_raw_narrative(text)

    def test_multiline_prose_returns_true(self):
        assert _classify_raw_narrative("The door creaks.\nYou step inside.")

    # --- False cases (must NOT be used as fallback) ---

    def test_empty_string_returns_false(self):
        assert not _classify_raw_narrative("")

    def test_whitespace_only_returns_false(self):
        assert not _classify_raw_narrative("   \n\t  ")

    def test_marker_returns_false(self):
        assert not _classify_raw_narrative(JSON_PARSE_FALLBACK_MARKER)

    def test_json_object_returns_false(self):
        assert not _classify_raw_narrative('{"narrative": "You wait."}')

    def test_json_array_returns_false(self):
        assert not _classify_raw_narrative('["item1", "item2"]')

    def test_json_null_returns_false(self):
        assert not _classify_raw_narrative("null")

    def test_json_true_returns_false(self):
        assert not _classify_raw_narrative("true")

    def test_json_false_returns_false(self):
        assert not _classify_raw_narrative("false")

    def test_json_number_returns_false(self):
        assert not _classify_raw_narrative("42")

    def test_json_float_returns_false(self):
        assert not _classify_raw_narrative("3.14")

    def test_no_alpha_chars_returns_false(self):
        """Text with no alphabetic chars is not a narrative."""
        assert not _classify_raw_narrative("12345 !@#$%")

    def test_malformed_json_object_returns_false(self):
        """Malformed JSON (parse fails) starting with { must NOT be classified as narrative.

        Previously this returned True because json.loads raised and text had alpha chars,
        causing raw JSON to be stored as story text (Scene 4 bug).
        """
        malformed = '{"narrative": "You wait.", "state_updates": {"npc_data": {"Kaelen": {"entity_id": "npc_kaelen_001"'
        assert not _classify_raw_narrative(malformed)

    def test_malformed_json_array_returns_false(self):
        """Malformed JSON (parse fails) starting with [ must NOT be classified as narrative."""
        malformed = '["narrative", "extra",'
        assert not _classify_raw_narrative(malformed)


if __name__ == "__main__":
    unittest.main()
