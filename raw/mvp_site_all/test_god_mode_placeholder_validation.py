"""Test god mode narrative validation with placeholder content detection."""

from mvp_site.dice_integrity import _check_god_mode_narrative
from mvp_site.narrative_response_schema import NarrativeResponse


class TestGodModePlaceholderValidation:
    """Test that placeholder content in god mode doesn't trigger false warnings."""

    def test_empty_narrative_passes(self):
        """Empty narrative should not trigger warning."""
        response = NarrativeResponse(
            narrative="",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None

    def test_whitespace_only_passes(self):
        """Whitespace-only narrative should not trigger warning."""
        response = NarrativeResponse(
            narrative="   \n  \t  ",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None

    def test_session_header_placeholder_passes(self):
        """Session header placeholders should not trigger warning."""
        response = NarrativeResponse(
            narrative="[SESSION_HEADER]",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None

    def test_mode_marker_placeholder_passes(self):
        """Mode markers should not trigger warning."""
        response = NarrativeResponse(
            narrative="[Mode: GOD MODE]",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None

    def test_timestamp_metadata_passes(self):
        """Timestamp metadata should not trigger warning."""
        response = NarrativeResponse(
            narrative="Timestamp: 209 AC, Month 5 Day 1",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None

    def test_short_non_prose_passes(self):
        """Short non-prose content (< 50 chars, no periods) should not trigger warning."""
        response = NarrativeResponse(
            narrative="Admin update complete",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None

    def test_short_with_period_passes_if_metadata(self):
        """Short content with metadata markers should pass even with periods."""
        response = NarrativeResponse(
            narrative="Location: Castle. Status: Active.",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None

    def test_actual_narrative_prose_fails(self):
        """Actual narrative prose should trigger warning."""
        response = NarrativeResponse(
            narrative="You stand in the castle courtyard. The guards look at you suspiciously.",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is not None
        assert "GOD_MODE_VIOLATION" in result

    def test_long_non_metadata_fails(self):
        """Long non-metadata content should trigger warning."""
        response = NarrativeResponse(
            narrative="The administrative changes have been applied to the character stats",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is not None
        assert "GOD_MODE_VIOLATION" in result

    def test_combined_placeholders_passes(self):
        """Multiple placeholder patterns should not trigger warning."""
        response = NarrativeResponse(
            narrative="[SESSION_HEADER]\nTimestamp: 209 AC\nStatus: Active",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None

    def test_prose_with_placeholder_substring_should_fail(self):
        """Narrative prose containing placeholder substrings should trigger warning."""
        response = NarrativeResponse(
            narrative="Status: You fight the dragon bravely.",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        # This SHOULD return a warning with the startswith() fix
        assert result is not None, "Prose with embedded placeholder should trigger warning"
        assert "GOD_MODE_VIOLATION" in result

    def test_prose_ending_with_placeholder_should_fail(self):
        """Narrative prose that happens to end with placeholder should trigger warning."""
        response = NarrativeResponse(
            narrative="The battle begins! [SESSION_HEADER]",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is not None, "Prose with trailing placeholder should trigger warning"
        assert "GOD_MODE_VIOLATION" in result

    def test_short_narrative_prose_should_fail(self):
        """Short but actual narrative prose should trigger warning."""
        response = NarrativeResponse(
            narrative="Guards attack",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        # This SHOULD return a warning with the action verb check
        assert result is not None, "Short narrative prose should trigger warning"
        assert "GOD_MODE_VIOLATION" in result

    def test_short_narrative_with_pronoun_should_fail(self):
        """Short narrative with second-person pronoun should trigger warning."""
        response = NarrativeResponse(
            narrative="You feel cold",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is not None, "Short narrative with pronoun should trigger warning"
        assert "GOD_MODE_VIOLATION" in result

    def test_short_metadata_without_action_passes(self):
        """Short metadata fragment without action verbs should pass."""
        response = NarrativeResponse(
            narrative="Loading data",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None, "Short non-narrative metadata should pass"

    def test_placeholder_prefix_with_action_verb_fails(self):
        """Placeholder prefix with action verb content should trigger warning (bypass fix)."""
        response = NarrativeResponse(
            narrative="Location: Die now",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is not None, "Placeholder prefix + action verb should trigger warning"
        assert "GOD_MODE_VIOLATION" in result

    def test_placeholder_prefix_with_pronoun_fails(self):
        """Placeholder prefix with pronoun content should trigger warning (bypass fix)."""
        response = NarrativeResponse(
            narrative="Status: You win",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is not None, "Placeholder prefix + pronoun should trigger warning"
        assert "GOD_MODE_VIOLATION" in result

    def test_placeholder_prefix_legitimate_metadata_passes(self):
        """Legitimate metadata with placeholder prefix should pass."""
        response = NarrativeResponse(
            narrative="Timestamp: 2024-01-01",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None, "Legitimate timestamp metadata should pass"

    def test_status_prefix_legitimate_metadata_passes(self):
        """Status prefix with non-narrative content should pass."""
        response = NarrativeResponse(
            narrative="Status: Active",
            god_mode_response="HP set to 50.",
        )
        result = _check_god_mode_narrative(response)
        assert result is None, "Status metadata without narrative indicators should pass"
