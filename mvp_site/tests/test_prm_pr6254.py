"""Test PRM PR #6254: XP progress tracking in rewards box visibility."""
import unittest


def normalize_rewards_box_for_ui(rewards_box):
    """Return displayable rewards_box payload or None. Include XP progress tracking in has_visible_content."""
    if not isinstance(rewards_box, dict):
        return None
    # Coerce fields to expected types with sensible defaults
    xp_gained = rewards_box.get("xp_gained", 0)
    if not isinstance(xp_gained, (int, float)):
        xp_gained = 0
    gold = rewards_box.get("gold", 0)
    if not isinstance(gold, (int, float)):
        gold = 0
    loot = rewards_box.get("loot", [])
    if loot is None:
        loot = []
    level_up_available = rewards_box.get("level_up_available", False)
    if isinstance(level_up_available, str):
        level_up_available = level_up_available.lower() in ("true", "1")
    progress_percent = rewards_box.get("progress_percent", 0)
    if isinstance(progress_percent, str):
        try:
            progress_percent = float(progress_percent)
        except (ValueError, TypeError):
            progress_percent = 0
    current_xp = rewards_box.get("current_xp", 0)
    if not isinstance(current_xp, (int, float)):
        current_xp = 0
    next_level_xp = rewards_box.get("next_level_xp", 0)
    if not isinstance(next_level_xp, (int, float)):
        next_level_xp = 0

    has_visible_content = (
        xp_gained > 0
        or gold > 0
        or bool(loot)
        or level_up_available
        or progress_percent > 0
        or (current_xp > 0 and next_level_xp > 0)  # PRM FIX
    )
    if not has_visible_content:
        return None

    result = rewards_box.copy()
    if "xp_gained" not in result and xp_gained != 0:
        result["xp_gained"] = xp_gained
    if "current_xp" not in result and current_xp > 0:
        result["current_xp"] = current_xp
    if "next_level_xp" not in result and next_level_xp > 0:
        result["next_level_xp"] = next_level_xp
    return result


class TestPRMPR6254(unittest.TestCase):
    """Test XP progress tracking visibility in rewards box."""

    def test_dict_with_xp_progress_tracking_visible_when_xp_gained_zero(self):
        """XP progress tracking visible when xp_gained=0 but current_xp=850, next_level_xp=1000."""
        rewards_box = {
            "xp_gained": 0,
            "current_xp": 850,
            "next_level_xp": 1000
        }
        result = normalize_rewards_box_for_ui(rewards_box)
        self.assertIsNotNone(result)
        self.assertEqual(result["current_xp"], 850)
        self.assertEqual(result["next_level_xp"], 1000)

    def test_dict_with_only_current_xp_returns_none(self):
        """Only current_xp present (no next_level_xp) should return None."""
        rewards_box = {
            "current_xp": 850
        }
        result = normalize_rewards_box_for_ui(rewards_box)
        self.assertIsNone(result)

    def test_dict_with_only_next_level_xp_returns_none(self):
        """Only next_level_xp present (no current_xp) should return None."""
        rewards_box = {
            "next_level_xp": 1000
        }
        result = normalize_rewards_box_for_ui(rewards_box)
        self.assertIsNone(result)

    def test_dict_with_zero_xp_and_progress_tracking_returns_none(self):
        """xp_gained=0, current_xp=0, next_level_xp=0 should return None."""
        rewards_box = {
            "xp_gained": 0,
            "current_xp": 0,
            "next_level_xp": 0
        }
        result = normalize_rewards_box_for_ui(rewards_box)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()