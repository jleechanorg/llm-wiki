"""
Test coverage for firestore_service.py inventory deduplication logic.
Addresses missing coverage identified in PR #3746 (lines 497-498, 506-507).
"""

from mvp_site.firestore_service import _handle_inventory_safeguard


def test_inventory_safeguard_handles_non_dict_items():
    """Test that inventory merge handles non-dict items (strings) correctly."""
    existing_inventory = ["Sword", "Shield", "Potion"]  # String items
    new_inventory = {
        "items": ["Sword", "Bow", "Arrow"]  # Upgrading to dict with items list
    }

    # Place existing inventory in state_to_update
    state_to_update = {"inventory": existing_inventory}

    # Call with correct signature: (state_to_update, key, value)
    result = _handle_inventory_safeguard(state_to_update, "inventory", new_inventory)

    assert result is True  # Handled
    # Should merge existing ["Sword", "Shield", "Potion"] + new ["Bow", "Arrow"]
    # "Sword" is duplicate, should be skipped
    merged_items = state_to_update["inventory"]["items"]
    assert "Sword" in merged_items
    assert "Shield" in merged_items
    assert "Potion" in merged_items
    assert "Bow" in merged_items
    assert "Arrow" in merged_items
    # Should have exactly 5 items (Sword, Shield, Potion from existing + Bow, Arrow from new)
    assert len(merged_items) == 5


def test_inventory_safeguard_handles_complex_dict_items():
    """Test that inventory merge handles complex dict items with JSON serialization."""
    existing_inventory = [
        {"name": "Longsword", "damage": "1d8"},
        {"name": "Shield", "ac_bonus": 2},
    ]
    new_inventory = {
        "items": [
            {"name": "Longsword", "damage": "1d8"},  # Duplicate
            {"name": "Bow", "damage": "1d8"},  # New item
        ],
        "gold": 100,  # Additional field in dict
    }

    # Place existing inventory in state_to_update
    state_to_update = {"inventory": existing_inventory}

    # Call with correct signature: (state_to_update, key, value)
    result = _handle_inventory_safeguard(state_to_update, "inventory", new_inventory)

    assert result is True
    merged_items = state_to_update["inventory"]["items"]

    # Should have 3 items: Longsword, Shield (from existing), Bow (new)
    assert len(merged_items) == 3
    assert {"name": "Longsword", "damage": "1d8"} in merged_items
    assert {"name": "Shield", "ac_bonus": 2} in merged_items
    assert {"name": "Bow", "damage": "1d8"} in merged_items

    # Gold field should be preserved
    assert state_to_update["inventory"]["gold"] == 100


def test_inventory_safeguard_handles_unserializable_items():
    """Test that items that can't be JSON serialized fall back to str() for deduplication."""

    class UnserializableItem:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return f"Item({self.name})"

    # This will trigger the TypeError exception branch in the code
    existing_inventory = [UnserializableItem("Sword")]
    new_inventory = {"items": [UnserializableItem("Sword"), UnserializableItem("Bow")]}

    # Place existing inventory in state_to_update
    state_to_update = {"inventory": existing_inventory}

    # This should not crash, should use str() fallback
    # Call with correct signature: (state_to_update, key, value)
    result = _handle_inventory_safeguard(state_to_update, "inventory", new_inventory)

    assert result is True
    # Should have merged the items using str() for comparison
    assert len(state_to_update["inventory"]["items"]) >= 2


def test_inventory_safeguard_preserves_existing_duplicates():
    """Test that existing duplicate items are preserved (not deduplicated)."""
    # Player has 3 potions (intentional duplicates)
    existing_inventory = ["Potion", "Potion", "Potion", "Sword"]
    new_inventory = {
        "items": ["Bow"]  # Adding new item
    }

    # Place existing inventory in state_to_update
    state_to_update = {"inventory": existing_inventory}

    # Call with correct signature: (state_to_update, key, value)
    result = _handle_inventory_safeguard(state_to_update, "inventory", new_inventory)

    assert result is True
    merged_items = state_to_update["inventory"]["items"]

    # All 3 potions should be preserved
    potion_count = sum(1 for item in merged_items if item == "Potion")
    assert potion_count == 3
    assert "Sword" in merged_items
    assert "Bow" in merged_items
    assert len(merged_items) == 5  # 3 Potions + Sword + Bow
