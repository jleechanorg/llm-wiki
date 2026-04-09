"""Unit test for cache prompt structure equivalence.

This test validates that LLMRequest.to_explicit_cache_parts() correctly splits
content without requiring a real campaign or API calls.
"""

from __future__ import annotations

import json

from mvp_site.llm_request import LLMRequest
from mvp_site.llm_service import json_default_serializer


def test_cache_parts_equivalence():
    """Test that explicit cache parts merge to equal implicit prompt."""
    # Create sample LLMRequest with realistic data
    story_history = [
        {"sequence_id": f"seq_{i}", "content": f"Story entry {i}"} for i in range(20)
    ]

    request = LLMRequest(
        user_action="I examine my surroundings",
        user_id="test_user_123",
        game_mode="character",
        game_state={"campaign_id": "test_campaign", "hp": 100, "level": 5},
        story_history=story_history,
        checkpoint_block="Sequence ID: 20",
        core_memories=["Memory 1", "Memory 2"],
        sequence_ids=[f"seq_{i}" for i in range(20)],
        entity_tracking={"entities": {"player": {"name": "Aric"}}},
        selected_prompts=["combat", "narrative"],
        use_default_world=False,
    )

    # Get implicit caching prompt (single JSON blob)
    implicit_json = request.to_json()

    # Get explicit caching parts (split cacheable/uncacheable)
    cached_entry_count = 15  # Cache first 15 entries
    cacheable_json, uncacheable_json = request.to_explicit_cache_parts(
        cached_entry_count
    )

    # Merge explicit parts
    explicit_merged = dict(cacheable_json)

    # Merge story_history arrays
    if "story_history" in uncacheable_json:
        explicit_merged["story_history"] = cacheable_json.get(
            "story_history", []
        ) + uncacheable_json.get("story_history", [])

    # Add all other uncacheable fields
    for key, value in uncacheable_json.items():
        if key != "story_history":
            explicit_merged[key] = value

    # Validate equivalence
    differences = []

    # Check field presence
    implicit_keys = set(implicit_json.keys())
    explicit_keys = set(explicit_merged.keys())

    missing_in_explicit = implicit_keys - explicit_keys
    extra_in_explicit = explicit_keys - implicit_keys

    if missing_in_explicit:
        differences.append(f"Missing fields in explicit: {missing_in_explicit}")
    if extra_in_explicit:
        differences.append(f"Extra fields in explicit: {extra_in_explicit}")

    # Compare field values
    common_keys = implicit_keys & explicit_keys
    for key in common_keys:
        implicit_val = implicit_json[key]
        explicit_val = explicit_merged[key]

        if implicit_val != explicit_val:
            differences.append(
                f"Value mismatch for '{key}': "
                f"implicit_len={len(str(implicit_val))}, "
                f"explicit_len={len(str(explicit_val))}"
            )

    # CRITICAL: Validate field ordering (prefix-based caching depends on this!)
    implicit_order = list(implicit_json.keys())
    explicit_order = list(explicit_merged.keys())

    if implicit_order != explicit_order:
        print("❌ Field ordering mismatch!")
        print(f"  Implicit order: {implicit_order}")
        print(f"  Explicit order: {explicit_order}")
        assert False, "Field ordering must be identical for prefix-based caching!"

    # CRITICAL: Validate actual JSON payloads (what gets sent to Gemini!)
    implicit_json_str = json.dumps(implicit_json, default=json_default_serializer)
    explicit_json_str = json.dumps(explicit_merged, default=json_default_serializer)

    if implicit_json_str != explicit_json_str:
        print("❌ JSON payload mismatch!")
        print(f"  Implicit JSON: {len(implicit_json_str)} bytes")
        print(f"  Explicit JSON: {len(explicit_json_str)} bytes")
        assert False, "JSON payloads must be byte-for-byte identical!"

    # Assert equivalence
    if differences:
        print("❌ Prompt structure differences detected:")
        for diff in differences:
            print(f"  - {diff}")
        assert False, f"Found {len(differences)} differences"

    # Verify cache split is correct
    assert len(cacheable_json["story_history"]) == 15, (
        "Cacheable should have 15 entries"
    )
    assert len(uncacheable_json["story_history"]) == 5, (
        "Uncacheable should have 5 entries"
    )
    assert cacheable_json["story_history"] == story_history[:15], (
        "Cacheable entries don't match"
    )
    assert uncacheable_json["story_history"] == story_history[15:], (
        "Uncacheable entries don't match"
    )

    print(
        "✅ Prompt equivalence validated - content, ordering, AND JSON payloads identical"
    )
    print(f"   Cacheable entries: {len(cacheable_json['story_history'])}")
    print(f"   Uncacheable entries: {len(uncacheable_json['story_history'])}")
    print(f"   Total fields: {len(implicit_keys)}")


def test_cache_parts_with_zero_cached():
    """Test cache split when no entries are cached yet."""
    story_history = [{"sequence_id": f"seq_{i}"} for i in range(5)]

    request = LLMRequest(
        user_action="Test action",
        user_id="test_user",
        game_mode="character",
        story_history=story_history,
    )

    cacheable, uncacheable = request.to_explicit_cache_parts(cached_entry_count=0)

    # All story entries should be in uncacheable when cache is empty
    assert len(cacheable.get("story_history", [])) == 0
    assert len(uncacheable["story_history"]) == 5

    print("✅ Zero-cached case validated")


def test_cache_parts_with_all_cached():
    """Test cache split when all entries are already cached."""
    story_history = [{"sequence_id": f"seq_{i}"} for i in range(10)]

    request = LLMRequest(
        user_action="Test action",
        user_id="test_user",
        game_mode="character",
        story_history=story_history,
    )

    cacheable, uncacheable = request.to_explicit_cache_parts(cached_entry_count=10)

    # All story entries should be in cacheable
    assert len(cacheable["story_history"]) == 10
    assert len(uncacheable["story_history"]) == 0

    print("✅ All-cached case validated")


def test_campaign_id_in_game_state_triggers_explicit_cache_condition():
    """Test that campaign_id in game_state satisfies explicit caching condition.

    BEAD-3qy: The explicit caching condition in llm_service.py requires:
    1. gemini_request.game_state exists
    2. gemini_request.game_state is a dict
    3. game_state.get("campaign_id") returns truthy value
    4. gemini_request.story_history exists

    This test validates that LLMRequest built with campaign_id satisfies all conditions.
    """
    story_history = [
        {"sequence_id": f"seq_{i}", "content": f"Story entry {i}"} for i in range(10)
    ]

    # Build request with campaign_id in game_state (simulating fix from BEAD-3qy)
    request = LLMRequest(
        user_action="I attack the dragon",
        user_id="test_user_123",
        game_mode="character",
        game_state={"campaign_id": "test_campaign_abc123", "hp": 100},
        story_history=story_history,
    )

    # Verify condition 1: game_state exists
    assert request.game_state is not None, "game_state must exist"

    # Verify condition 2: game_state is a dict
    assert isinstance(request.game_state, dict), "game_state must be dict"

    # Verify condition 3: campaign_id is truthy
    campaign_id = request.game_state.get("campaign_id")
    assert campaign_id, f"campaign_id must be truthy, got: {campaign_id}"
    assert campaign_id == "test_campaign_abc123"

    # Verify condition 4: story_history exists
    assert request.story_history is not None, "story_history must exist"
    assert len(request.story_history) > 0, "story_history must not be empty"

    # Verify JSON serialization preserves campaign_id
    json_output = request.to_json()
    assert "campaign_id" in json_output.get("game_state", {}), (
        "campaign_id must be preserved in JSON output"
    )

    print("✅ All explicit caching trigger conditions satisfied")
    print(f"   campaign_id: {campaign_id}")
    print(f"   story_history entries: {len(request.story_history)}")


def test_build_full_content_for_retry_centralized():
    """Test that build_full_content_for_retry is centralized and produces correct output.

    TDD: This tests the centralized helper function that builds full content
    for cache retry scenarios. The function should exist in llm_service.py
    and produce JSON identical to gemini_request.to_json() serialized.
    """
    from mvp_site.llm_service import build_full_content_for_retry

    story_history = [
        {"sequence_id": f"seq_{i}", "content": f"Story entry {i}"} for i in range(20)
    ]

    request = LLMRequest(
        user_action="I examine my surroundings",
        user_id="test_user_123",
        game_mode="character",
        game_state={"campaign_id": "test_campaign", "hp": 100, "level": 5},
        story_history=story_history,
        checkpoint_block="Sequence ID: 20",
        core_memories=["Memory 1", "Memory 2"],
        sequence_ids=[f"seq_{i}" for i in range(20)],
        entity_tracking={"entities": {"player": {"name": "Aric"}}},
        selected_prompts=["combat", "narrative"],
        use_default_world=False,
    )

    # Call the centralized function
    full_content_str = build_full_content_for_retry(request)

    # Verify it's a valid JSON string
    assert isinstance(full_content_str, str), "Result must be a string"

    # Verify it can be parsed as JSON
    parsed = json.loads(full_content_str)
    assert isinstance(parsed, dict), "Parsed result must be a dict"

    # Verify it matches to_json() output
    expected = request.to_json()
    assert parsed == expected, "Must match gemini_request.to_json()"

    # Verify serialization format (indent=2 for readability)
    expected_str = json.dumps(expected, indent=2, default=json_default_serializer)
    assert full_content_str == expected_str, (
        "Must use indent=2 and json_default_serializer"
    )

    print("✅ build_full_content_for_retry centralized function validated")
    print(f"   Output size: {len(full_content_str)} bytes")
    print(f"   Fields: {list(parsed.keys())}")


if __name__ == "__main__":
    test_cache_parts_equivalence()
    test_cache_parts_with_zero_cached()
    test_cache_parts_with_all_cached()
    test_campaign_id_in_game_state_triggers_explicit_cache_condition()
    test_build_full_content_for_retry_centralized()
    print("\n🎉 All cache prompt structure tests passed!")
