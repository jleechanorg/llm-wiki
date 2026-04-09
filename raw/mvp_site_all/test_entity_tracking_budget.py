"""
Test that entity tracking tokens are properly accounted for in the scaffold budget.

This test reproduces the bug where entity tracking (entity_preload_text,
entity_specific_instructions, entity_tracking_instruction) is added AFTER
truncation, causing the final prompt to exceed the context window limit.

Bug details from production logs:
- Model: qwen-3-235b-a22b-instruct-2507
- Input used: 97,923 tokens
- Max allowed: 94,372 tokens (80% of 117,964)
- Overage: ~3,500 tokens (from entity tracking not budgeted)

Fix: Added ENTITY_TRACKING_TOKEN_RESERVE constant (10,500 tokens) that is
explicitly added to scaffold budget before truncation calculation.
"""

import json
import unittest

from mvp_site import llm_service
from mvp_site.token_utils import estimate_tokens


class TestEntityTrackingBudget(unittest.TestCase):
    """Test that entity tracking is properly budgeted in scaffold estimation."""

    def test_entity_tracking_must_be_included_in_scaffold_budget(self):
        """
        Verify that entity tracking tokens are included in scaffold budget.

        Fix implemented: ENTITY_TRACKING_TOKEN_RESERVE constant (10,500 tokens)
        is now added to scaffold budget before truncation calculation.
        """
        # Entity tracking that gets added AFTER truncation
        # These are realistic sizes for a game with 10+ NPCs
        entity_preload_text = "E" * 8000  # ~2000 tokens - NPC summaries
        entity_specific_instructions = (
            "F" * 6000
        )  # ~1500 tokens - per-turn instructions
        entity_tracking_instruction = "G" * 4000  # ~1000 tokens - tracking rules
        timeline_log = "H" * 12000  # ~3000 tokens - story timeline

        # Total entity tracking overhead
        entity_overhead = (
            entity_preload_text
            + entity_specific_instructions
            + entity_tracking_instruction
            + timeline_log
        )
        entity_overhead_tokens = estimate_tokens(entity_overhead)

        # THE KEY ASSERTION: ENTITY_TRACKING_TOKEN_RESERVE must cover entity overhead
        self.assertGreaterEqual(
            llm_service.ENTITY_TRACKING_TOKEN_RESERVE,
            entity_overhead_tokens,
            f"ENTITY_TRACKING_TOKEN_RESERVE ({llm_service.ENTITY_TRACKING_TOKEN_RESERVE}) "
            f"must be >= entity tracking overhead ({entity_overhead_tokens} tokens).",
        )

    def test_entity_tracking_reserve_covers_production_overhead(self):
        """
        Verify ENTITY_TRACKING_TOKEN_RESERVE covers the production error case.

        From production logs:
        - Model: qwen-3-235b-a22b-instruct-2507
        - Overage: ~3,500 tokens (entity tracking not budgeted)
        """
        # Entity tracking overhead from production error
        production_overhead_tokens = 3500

        # The fix uses explicit reserve instead of percentage
        self.assertGreaterEqual(
            llm_service.ENTITY_TRACKING_TOKEN_RESERVE,
            production_overhead_tokens,
            f"ENTITY_TRACKING_TOKEN_RESERVE ({llm_service.ENTITY_TRACKING_TOKEN_RESERVE}) "
            f"must cover production overhead ({production_overhead_tokens} tokens).",
        )


class TestScaffoldBudgetCalculation(unittest.TestCase):
    """Test the scaffold budget calculation logic."""

    def test_entity_tracking_reserve_covers_max_overhead(self):
        """
        Verify ENTITY_TRACKING_TOKEN_RESERVE covers maximum possible entity tracking.
        """
        # Maximum entity tracking sizes (worst case with many NPCs)
        MAX_ENTITY_PRELOAD_TOKENS = 3000  # 10+ NPCs with full descriptions
        MAX_ENTITY_INSTRUCTIONS_TOKENS = 2000  # Complex entity instructions
        MAX_ENTITY_TRACKING_TOKENS = 1500  # Tracking rules
        MAX_TIMELINE_LOG_TOKENS = 4000  # Long story timeline

        TOTAL_ENTITY_OVERHEAD = (
            MAX_ENTITY_PRELOAD_TOKENS
            + MAX_ENTITY_INSTRUCTIONS_TOKENS
            + MAX_ENTITY_TRACKING_TOKENS
            + MAX_TIMELINE_LOG_TOKENS
        )

        self.assertGreaterEqual(
            llm_service.ENTITY_TRACKING_TOKEN_RESERVE,
            TOTAL_ENTITY_OVERHEAD,
            f"ENTITY_TRACKING_TOKEN_RESERVE ({llm_service.ENTITY_TRACKING_TOKEN_RESERVE}) "
            f"must be >= max entity overhead ({TOTAL_ENTITY_OVERHEAD}).",
        )

    def test_entity_tracking_reserve_constant_exists(self):
        """Verify the ENTITY_TRACKING_TOKEN_RESERVE constant exists and is reasonable."""
        self.assertTrue(
            hasattr(llm_service, "ENTITY_TRACKING_TOKEN_RESERVE"),
            "ENTITY_TRACKING_TOKEN_RESERVE constant must exist in llm_service",
        )
        self.assertGreater(
            llm_service.ENTITY_TRACKING_TOKEN_RESERVE,
            5000,
            "ENTITY_TRACKING_TOKEN_RESERVE should be > 5000 tokens for safety",
        )
        self.assertLess(
            llm_service.ENTITY_TRACKING_TOKEN_RESERVE,
            20000,
            "ENTITY_TRACKING_TOKEN_RESERVE should be < 20000 to leave room for story",
        )


class TestEntityTierBudgeting(unittest.TestCase):
    """Test tiered entity tracking respects budget ordering."""

    def _build_token_count(self, entity_tracking_data: dict[str, list[dict[str, str]]]) -> int:
        return estimate_tokens(json.dumps(entity_tracking_data, separators=(",", ":")))

    def test_dormant_entities_included_when_budget_allows(self):
        npc_data = {
            "Ava": {"name": "Ava", "role": "Guard", "location": "Inn"},
            "Borin": {"name": "Borin", "role": "Merchant", "location": "Inn"},
            "Cora": {"name": "Cora", "role": "Scout", "location": "Woods"},
            "Dain": {"name": "Dain", "role": "Blacksmith", "location": "Forge"},
        }
        story_context = [
            {"text": "Ava speaks quietly to the party by the hearth."},
        ]

        entity_tracking_data, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="Inn",
            max_tokens=None,
        )

        assert len(entity_tracking_data["active_entities"]) == 1
        assert len(entity_tracking_data["present_entities"]) == 1
        assert len(entity_tracking_data["dormant_entities"]) == 2

    def test_budget_drops_dormant_before_present_or_active(self):
        npc_data = {
            "Ava": {"name": "Ava", "role": "Guard", "location": "Inn"},
            "Borin": {"name": "Borin", "role": "Merchant", "location": "Inn"},
            "Cora": {"name": "Cora", "role": "Scout", "location": "Woods"},
            "Dain": {"name": "Dain", "role": "Blacksmith", "location": "Forge"},
        }
        story_context = [
            {"text": "Ava speaks quietly to the party by the hearth."},
        ]

        full_tracking, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="Inn",
            max_tokens=None,
        )

        without_dormant = {
            "active_entities": full_tracking["active_entities"],
            "present_entities": full_tracking["present_entities"],
            "dormant_entities": [],
        }

        # Add a small margin to avoid brittle dependence on exact token matching.
        budget = self._build_token_count(without_dormant) + 2

        trimmed_tracking, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="Inn",
            max_tokens=budget,
        )

        assert len(trimmed_tracking["active_entities"]) == len(
            without_dormant["active_entities"]
        )
        assert len(trimmed_tracking["present_entities"]) == len(
            without_dormant["present_entities"]
        )
        assert trimmed_tracking["dormant_entities"] == []

    def test_build_trimmed_entity_tracking_handles_malformed_npc_entries(self):
        npc_data = {
            "Ava": {"name": "Ava", "role": "Guard", "location": "Inn"},
            "Borin": ["status: wounded", "location: Inn"],
            "Cora": "friendly greeting",
            "Dain": ["status_update_only", 12],
        }
        story_context = [
            {"text": "Ava speaks quietly to the party by the hearth."},
        ]

        full_tracking, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="Inn",
            max_tokens=None,
        )

        assert len(full_tracking["active_entities"]) == 1
        assert len(full_tracking["present_entities"]) == 1
        assert len(full_tracking["dormant_entities"]) == 2

    def test_budget_drops_present_after_dormant_exhausted(self):
        """When budget is very tight, present entities are dropped after dormant."""
        # Create NPCs: 1 active (mentioned), 3 present (at location), 2 dormant (elsewhere)
        npc_data = {
            "Ava": {"name": "Ava", "role": "Guard", "location": "Inn"},
            "Borin": {"name": "Borin", "role": "Merchant", "location": "Inn"},
            "Cora": {"name": "Cora", "role": "Innkeeper", "location": "Inn"},
            "Dain": {"name": "Dain", "role": "Bard", "location": "Inn"},
            "Eve": {"name": "Eve", "role": "Scout", "location": "Woods"},
            "Finn": {"name": "Finn", "role": "Smith", "location": "Forge"},
        }
        story_context = [
            {"text": "Ava greets the party warmly."},
        ]

        # Get full tracking first
        full_tracking, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="Inn",
            max_tokens=None,
        )

        # Should have: 1 active (Ava), 3 present (Borin, Cora, Dain), 2 dormant (Eve, Finn)
        self.assertEqual(len(full_tracking["active_entities"]), 1)
        self.assertEqual(len(full_tracking["present_entities"]), 3)
        self.assertEqual(len(full_tracking["dormant_entities"]), 2)

        # Build a target with active only (no present, no dormant)
        active_only = {
            "active_entities": full_tracking["active_entities"],
            "present_entities": [],
            "dormant_entities": [],
        }
        # Budget that fits active only (plus small margin)
        budget = self._build_token_count(active_only) + 2

        trimmed_tracking, log_summary = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="Inn",
            max_tokens=budget,
        )

        # Active preserved, present dropped, dormant dropped
        self.assertEqual(len(trimmed_tracking["active_entities"]), 1)
        self.assertEqual(len(trimmed_tracking["present_entities"]), 0)
        self.assertEqual(len(trimmed_tracking["dormant_entities"]), 0)
        # Log should show dropped counts
        self.assertIn("dropped=", log_summary)
        self.assertIn("present:", log_summary)

    def test_budget_drops_active_when_extremely_tight(self):
        """When budget is extremely tight, even active entities are dropped."""
        # Create NPCs: 3 active (mentioned), 2 present, 2 dormant
        npc_data = {
            "Ava": {"name": "Ava", "role": "Guard", "location": "Inn"},
            "Borin": {"name": "Borin", "role": "Merchant", "location": "Inn"},
            "Cora": {"name": "Cora", "role": "Scout", "location": "Inn"},
            "Dain": {"name": "Dain", "role": "Bard", "location": "Inn"},
            "Eve": {"name": "Eve", "role": "Smith", "location": "Inn"},
            "Finn": {"name": "Finn", "role": "Mage", "location": "Woods"},
            "Gwen": {"name": "Gwen", "role": "Healer", "location": "Forge"},
        }
        story_context = [
            {"text": "Ava, Borin, and Cora discuss the plan."},
        ]

        # Get full tracking first
        full_tracking, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="Inn",
            max_tokens=None,
        )

        # Should have: 3 active (Ava, Borin, Cora), 2 present (Dain, Eve), 2 dormant (Finn, Gwen)
        self.assertEqual(len(full_tracking["active_entities"]), 3)
        self.assertEqual(len(full_tracking["present_entities"]), 2)
        self.assertEqual(len(full_tracking["dormant_entities"]), 2)

        # Build a target with only 1 active (force dropping 2 active entities)
        one_active = {
            "active_entities": full_tracking["active_entities"][:1],
            "present_entities": [],
            "dormant_entities": [],
        }
        # Budget that fits only 1 active (plus small margin)
        budget = self._build_token_count(one_active) + 2

        trimmed_tracking, log_summary = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="Inn",
            max_tokens=budget,
        )

        # Should have dropped to 1 active, 0 present, 0 dormant
        self.assertLessEqual(len(trimmed_tracking["active_entities"]), 1)
        self.assertEqual(len(trimmed_tracking["present_entities"]), 0)
        self.assertEqual(len(trimmed_tracking["dormant_entities"]), 0)
        # Log should show active drops
        self.assertIn("dropped=", log_summary)
        self.assertIn("active:", log_summary)

    def test_dormant_entities_capped_at_max(self):
        """Dormant entities must be capped at ENTITY_TIER_DORMANT_MAX even without budget."""
        # Create 30 NPCs that will all be dormant (not mentioned, not at current location)
        npc_data = {
            f"NPC_{i}": {"name": f"NPC_{i}", "role": "Villager", "location": f"Zone_{i}"}
            for i in range(30)
        }
        story_context = []  # No mentions -> no active entities

        entity_tracking_data, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="Tavern",  # No NPC is here
            max_tokens=None,  # No budget constraint
        )

        # All 30 should be dormant (none active, none present)
        self.assertEqual(len(entity_tracking_data["active_entities"]), 0)
        self.assertEqual(len(entity_tracking_data["present_entities"]), 0)

        # Dormant must be capped
        self.assertTrue(
            hasattr(llm_service, "ENTITY_TIER_DORMANT_MAX"),
            "ENTITY_TIER_DORMANT_MAX constant must exist in llm_service",
        )
        self.assertLessEqual(
            len(entity_tracking_data["dormant_entities"]),
            llm_service.ENTITY_TIER_DORMANT_MAX,
            f"Dormant entities ({len(entity_tracking_data['dormant_entities'])}) "
            f"should be capped at ENTITY_TIER_DORMANT_MAX ({llm_service.ENTITY_TIER_DORMANT_MAX})",
        )


class TestLocationDictRegression(unittest.TestCase):
    """Regression tests for AttributeError when location fields are dicts instead of strings.

    Production bug: world_data["current_location_name"] stored as dict (e.g.
    {"id": "loc_ashwood_keep_001", "name": "Ashwood Keep"}) instead of a plain string,
    causing AttributeError: 'dict' object has no attribute 'strip' in _tier_entities().
    """

    def _minimal_npc(self, name, location):
        return {"name": name, "role": "Guard", "location": location}

    def test_current_location_as_dict_does_not_crash(self):
        """Dict current_location is coerced to string; NPC mentioned in story lands in ACTIVE."""
        npc_data = {"Aldric": self._minimal_npc("Aldric", "Ashwood Keep")}
        story_context = [{"text": "Aldric stands guard at the gate."}]
        location_dict = {"id": "loc_ashwood_keep_001", "name": "Ashwood Keep"}

        result, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location=location_dict,
        )
        # Dict coerced to "Ashwood Keep"; Aldric mentioned in story -> ACTIVE (not just PRESENT)
        self.assertEqual(len(result["active_entities"]), 1)
        self.assertEqual(len(result["present_entities"]), 0)
        self.assertEqual(len(result["dormant_entities"]), 0)

    def test_current_location_dict_enables_present_matching(self):
        """Dict current_location is coerced to string and enables PRESENT tier matching.

        _tier_entities coerces current_location dict before the comparison loop, so
        NPCs at the extracted location are correctly placed in PRESENT (not DORMANT).
        """
        npc_data = {
            "Aldric": self._minimal_npc("Aldric", "Ashwood Keep"),
            "Faraway": self._minimal_npc("Faraway", "The Docks"),
        }
        story_context = []  # No mentions -> no active
        location_dict = {"id": "loc_ashwood_keep_001", "name": "Ashwood Keep"}

        result, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location=location_dict,
        )
        # Dict coerced to "Ashwood Keep"; Aldric matches -> PRESENT, Faraway -> DORMANT
        self.assertEqual(len(result["active_entities"]), 0)
        self.assertEqual(len(result["present_entities"]), 1)
        self.assertEqual(len(result["dormant_entities"]), 1)

    def test_npc_location_as_dict_enables_present_matching(self):
        """NPC dict location is coerced to string and enables PRESENT tier matching."""
        npc_data = {
            "Aldric": {
                "name": "Aldric",
                "role": "Guard",
                "current_location": {"id": "loc_ashwood_keep_001", "name": "Ashwood Keep"},
            }
        }
        story_context = []
        result, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="Ashwood Keep",
        )
        # Dict coerced to "Ashwood Keep"; matches current_location -> PRESENT
        self.assertEqual(len(result["active_entities"]), 0)
        self.assertEqual(len(result["present_entities"]), 1)
        self.assertEqual(len(result["dormant_entities"]), 0)

    def test_current_location_as_dict_with_id_only(self):
        """current_location dict with only 'id' key coerces to id string for matching."""
        npc_data = {"Aldric": self._minimal_npc("Aldric", "loc_ashwood_keep_001")}
        story_context = []
        location_dict = {"id": "loc_ashwood_keep_001"}

        result, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location=location_dict,
        )
        # Dict {"id": "loc_ashwood_keep_001"} coerced to "loc_ashwood_keep_001"; Aldric matches -> PRESENT
        self.assertEqual(len(result["active_entities"]), 0)
        self.assertEqual(len(result["present_entities"]), 1)
        self.assertEqual(len(result["dormant_entities"]), 0)

    def test_current_location_as_dict_with_none_name_uses_id(self):
        """current_location dict with name=None falls back to id for location matching."""
        npc_data = {"Aldric": self._minimal_npc("Aldric", "loc_ashwood_keep_001")}
        story_context = []
        location_dict = {"id": "loc_ashwood_keep_001", "name": None}

        result, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location=location_dict,
        )
        # Dict {"name": None, "id": "..."} coerces to id string; Aldric matches -> PRESENT
        self.assertEqual(len(result["active_entities"]), 0)
        self.assertEqual(len(result["present_entities"]), 1)
        self.assertEqual(len(result["dormant_entities"]), 0)

    def test_npc_location_dict_with_none_name_uses_id(self):
        """NPC current_location dict with name=None falls back to id for matching."""
        npc_data = {
            "Aldric": {
                "name": "Aldric",
                "role": "Guard",
                "current_location": {"id": "loc_ashwood_keep_001", "name": None},
            }
        }
        story_context = []
        result, _ = llm_service._build_trimmed_entity_tracking(
            npc_data=npc_data,
            story_context=story_context,
            current_location="loc_ashwood_keep_001",
        )
        # Dict {"name": None, "id": "..."} coerces to id string; Aldric matches -> PRESENT
        self.assertEqual(len(result["active_entities"]), 0)
        self.assertEqual(len(result["present_entities"]), 1)
        self.assertEqual(len(result["dormant_entities"]), 0)


if __name__ == "__main__":
    unittest.main()
