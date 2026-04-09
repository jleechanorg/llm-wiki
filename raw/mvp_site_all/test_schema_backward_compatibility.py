"""TDD tests for schema backward-compatibility (REV-79o, REV-hp8, REV-6zg).

This test ensures schema validation does NOT break existing campaigns:
- REV-79o: Enforced schema validation rejects existing campaign game_state payloads
- REV-hp8: level <= 20 schema cap blocks divine/sovereign progression
- REV-6zg: Lowercase-only world_time.time_of_day validation breaks existing campaigns

Expected behavior:
- Schema validation should handle existing campaign data gracefully
- Divine/sovereign levels (>20) should be accepted
- Title Case time_of_day values should be accepted (or normalized)
"""

import copy
import unittest
from datetime import datetime

from mvp_site.campaign_upgrade import normalize_planning_block_choices
from mvp_site.game_state import (
    GameState,
    _extract_int_like,
    canonicalize_state_updates_in_place,
    migrate_legacy_state_for_schema,
    validate_and_correct_state,
)
from mvp_site.schemas.validation import validate_game_state


class TestSchemaBackwardCompatibility(unittest.TestCase):
    """Test that schema validation doesn't break existing campaigns."""

    def _validate_with_migration(self, game_state: dict) -> list[str]:
        """Helper: apply migration then validate (proper backward compat flow)."""
        migrated_state, _ = migrate_legacy_state_for_schema(game_state)
        return validate_game_state(migrated_state)

    def test_legacy_character_gold_falls_back_to_resources_gold_new_first(self):
        """Legacy campaigns may store gold in player_character_data.gold.

        Requirement: read path prefers canonical player_character_data.resources.gold,
        but falls back to legacy player_character_data.gold when canonical is absent.
        """
        # Legacy-only gold
        legacy_state = {
            "player_character_data": {
                "name": "Legacy Hero",
                "gold": 123,
                "level": 2,
            }
        }
        gs = GameState.from_dict(legacy_state)
        assert gs is not None
        assert isinstance(gs.player_character_data, dict)
        assert gs.player_character_data.get("resources", {}).get("gold") == 123

        # New-first: canonical wins over legacy flat field
        mixed_state = {
            "player_character_data": {
                "name": "Mixed Hero",
                "gold": 999,
                "resources": {"gold": 50},
                "level": 2,
            }
        }
        gs2 = GameState.from_dict(mixed_state)
        assert gs2 is not None
        assert isinstance(gs2.player_character_data, dict)
        assert gs2.player_character_data.get("resources", {}).get("gold") == 50

    def test_legacy_migration_session_id_uses_campaign_seed(self):
        """Legacy migration should generate stable campaign-anchored session IDs."""
        legacy_state = {
            "player_character_data": {"name": "Legacy Hero"},
            "world_data": {"current_location": "tavern"},
        }

        migrated_a, _ = migrate_legacy_state_for_schema(
            copy.deepcopy(legacy_state), migration_seed="user-a:campaign-a"
        )
        migrated_b, _ = migrate_legacy_state_for_schema(
            copy.deepcopy(legacy_state), migration_seed="user-b:campaign-b"
        )

        self.assertIn("session_id", migrated_a)
        self.assertIn("session_id", migrated_b)
        self.assertNotEqual(
            migrated_a["session_id"],
            migrated_b["session_id"],
            "Different campaigns should not share the same fallback legacy session_id",
        )

        migrated_a_repeat, _ = migrate_legacy_state_for_schema(
            copy.deepcopy(legacy_state), migration_seed="user-a:campaign-a"
        )
        self.assertEqual(
            migrated_a["session_id"],
            migrated_a_repeat["session_id"],
            "Same campaign seed should produce deterministic session_id",
        )

        self.assertTrue(migrated_a["session_id"].startswith("legacy-migrated-"))

    def test_extract_int_like_parses_formatted_and_signed_currency_strings(self):
        """Gold parser should handle separators and preserve sign semantics."""
        self.assertEqual(_extract_int_like("1,000 gp"), 1000)
        self.assertEqual(_extract_int_like("12 345 gold"), 12345)
        self.assertEqual(_extract_int_like("-50 gp"), -50)

    def test_state_update_gold_conflict_prefers_noncanonical_write(self):
        """State updates should preserve misplaced gold write when both paths are present."""
        state_updates = {
            "player_character_data": {
                "resources": {"gold": 10},
                "equipment": {"backpack": [{"stats": {"gold": 25}}]},
            }
        }

        canonicalize_state_updates_in_place(state_updates)

        pc = state_updates["player_character_data"]
        self.assertEqual(pc.get("resources", {}).get("gold"), 25)
        self.assertNotIn("gold", pc["equipment"]["backpack"][0]["stats"])

    def test_validate_and_correct_normalizes_player_character_data_shape_drift(self):
        """REV-a5v3.2: normalize inventory/equipment drift and move non-schema fields."""
        state = {
            "game_state_version": 1,
            "session_id": "test-session",
            "turn_number": 1,
            "player_character_data": {
                "name": "Drift Hero",
                "class": "Fighter",
                "inventory": {"rope": "Silk Rope"},
                "equipment": ["Torch", "Rations"],
                "mysterious_lore_blob": {"text": "very long lore"},
            },
            "custom_campaign_state": {},
        }

        normalized, corrections = validate_and_correct_state(state, return_corrections=True)
        pc = normalized["player_character_data"]
        self.assertIsInstance(pc.get("inventory"), list)
        self.assertIsInstance(pc.get("equipment"), dict)
        self.assertIn("backpack", pc.get("equipment", {}))
        self.assertNotIn("mysterious_lore_blob", pc)
        extras = normalized.get("custom_campaign_state", {}).get(
            "player_character_data_extras", {}
        )
        self.assertIn("mysterious_lore_blob", extras)
        self.assertTrue(
            any("Moved non-schema player_character_data fields" in c for c in corrections)
        )

    def test_validate_and_correct_preserves_schema_valid_spells_prepared(self):
        """REV-spells-prepared: canonicalization must keep schema-defined spell fields."""
        state = {
            "game_state_version": 1,
            "session_id": "test-session",
            "turn_number": 1,
            "player_character_data": {
                "name": "Lyra Nightwhisper",
                "class": "Wizard",
                "level": 1,
                "spells_prepared": [
                    {
                        "name": "Magic Missile",
                        "level": 1,
                        "description": "Three glowing darts of magical force",
                    }
                ],
            },
            "custom_campaign_state": {},
        }

        normalized, corrections = validate_and_correct_state(state, return_corrections=True)
        pc = normalized["player_character_data"]
        extras = normalized.get("custom_campaign_state", {}).get(
            "player_character_data_extras", {}
        )

        self.assertIn("spells_prepared", pc)
        self.assertEqual(pc["spells_prepared"][0]["name"], "Magic Missile")
        self.assertNotIn("spells_prepared", extras)
        self.assertFalse(
            any("spells_prepared" in correction for correction in corrections),
            f"spells_prepared should remain canonical, got corrections: {corrections}",
        )

    def test_validate_and_correct_normalizes_social_hp_enum_drift(self):
        """REV-a5v3.1: normalize unsupported severity/skill enum values."""
        state = {
            "game_state_version": 1,
            "session_id": "test-session",
            "turn_number": 1,
            "social_hp_challenge": {
                "npc_name": "Guard Captain",
                "objective": "Gain access",
                "social_hp": 10,
                "social_hp_max": 20,
                "status": "RESISTING",
                "request_severity": "standard",
                "skill_used": "Investigation / Persuasion",
            },
        }

        normalized, _ = validate_and_correct_state(state, return_corrections=True)
        challenge = normalized.get("social_hp_challenge", {})
        self.assertEqual(challenge.get("request_severity"), "information")
        self.assertEqual(challenge.get("skill_used"), "Persuasion")

    def test_validate_and_correct_normalizes_god_mode_directives_and_arc_timestamps(self):
        """REV-a5v3.3/4: directives become objects and lore-time timestamps are repaired."""
        state = {
            "game_state_version": 1,
            "session_id": "test-session",
            "turn_number": 1,
            "custom_campaign_state": {
                "god_mode_directives": [
                    "Always enforce torchlight realism",
                    {"rule": "Never skip dawn prayer", "added": "yesterday-at-sundown"},
                ],
                "arc_milestones": {
                    "wedding_tour": {
                        "status": "in_progress",
                        "updated_at": "0 ABY-III",
                    }
                },
            },
        }

        normalized, _ = validate_and_correct_state(state, return_corrections=True)
        ccs = normalized.get("custom_campaign_state", {})
        directives = ccs.get("god_mode_directives", [])
        self.assertIsInstance(directives, list)
        self.assertTrue(all(isinstance(d, dict) for d in directives))
        self.assertTrue(all(isinstance(d.get("rule"), str) for d in directives))
        self.assertTrue(all(isinstance(d.get("added"), str) for d in directives))

        milestone = ccs.get("arc_milestones", {}).get("wedding_tour", {})
        self.assertIsInstance(milestone.get("updated_at"), str)
        self.assertTrue("T" in milestone.get("updated_at", ""))
        self.assertEqual(milestone.get("updated_at_lore"), "0 ABY-III")

    def test_divine_level_accepted_rev_hp8(self):
        """REV-hp8: Schema should accept levels > 20 for divine/sovereign progression.

        Existing campaigns have characters at level 21+ (divine/sovereign tiers).
        Schema validation must not reject these valid game states.
        """
        # Existing campaign with divine-tier character (level 21)
        game_state = {
            "world_data": {
                "world_time": {
                    "day": 1,
                    "hour": 12,
                    "minute": 0,
                    "second": 0,
                    "microsecond": 0,
                    "time_of_day": "noon",
                },
                "current_location": "Divine Sanctum",
            },
            "player_character_data": {
                "name": "Divine Hero",
                "level": 21,  # Divine tier (>20)
                "hp_current": 200,
                "hp_max": 200,
                "xp": 355000,  # XP for level 21
            },
            "narrative": "You have ascended to divine power.",
        }

        # Should NOT raise ValueError (after migration)
        errors = self._validate_with_migration(game_state)
        self.assertEqual(
            errors,
            [],
            f"Schema validation should accept level 21 (divine tier), got errors: {errors}",
        )

    def test_title_case_time_of_day_accepted_rev_6zg(self):
        """REV-6zg: Schema should accept Title Case time_of_day from existing campaigns.

        Existing campaigns may have time_of_day in Title Case (e.g., "Morning", "Evening").
        Schema validation should either accept these or normalize them gracefully.
        """
        # Existing campaign with Title Case time_of_day
        game_state = {
            "world_data": {
                "world_time": {
                    "day": 1,
                    "hour": 8,
                    "minute": 0,
                    "second": 0,
                    "microsecond": 0,
                    "time_of_day": "Morning",  # Title Case (existing format)
                },
                "current_location": "Village Square",
            },
            "player_character_data": {
                "name": "Hero",
                "level": 5,
                "hp_current": 50,
                "hp_max": 50,
            },
            "narrative": "Morning light fills the square.",
        }

        # Should NOT raise ValueError (after migration)
        errors = self._validate_with_migration(game_state)
        self.assertEqual(
            errors,
            [],
            f"Schema validation should accept Title Case time_of_day, got errors: {errors}",
        )

    def test_existing_campaign_payload_accepted_rev_79o(self):
        """REV-79o: Schema validation should accept real existing campaign payloads.

        This tests that actual game state structures from existing campaigns
        can pass validation without errors.
        """
        # Realistic existing campaign payload
        game_state = {
            "world_data": {
                "world_time": {
                    "day": 15,
                    "hour": 14,
                    "minute": 30,
                    "second": 45,
                    "microsecond": 123456,
                    "time_of_day": "afternoon",  # lowercase is fine
                },
                "current_location": "Adventurer's Guild",
                "campaign_state": "active",
            },
            "player_character_data": {
                "name": "Seasoned Adventurer",
                "level": 12,
                "hp_current": 85,
                "hp_max": 120,
                "xp": 51500,
            },
            "narrative": "You discuss your next quest with the guild master.",
            "planning_block": {
                "thinking": "The guild has several quests available.",
                "choices": {
                    "accept_dragon_quest": {
                        "id": "accept_dragon_quest",
                        "text": "Accept the dragon quest",
                        "description": "A dangerous but lucrative mission",
                        "risk_level": "high",
                    },
                    "gather_herbs": {
                        "id": "gather_herbs",
                        "text": "Gather healing herbs",
                        "description": "A simple gathering mission",
                        "risk_level": "low",
                    },
                },
            },
        }

        # Legacy dict-format choices are normalized to canonical list format.
        game_state["planning_block"] = normalize_planning_block_choices(
            game_state.get("planning_block")
        )

        # Should NOT raise ValueError after normalization
        errors = self._validate_with_migration(game_state)
        self.assertEqual(
            errors,
            [],
            f"Schema validation should accept existing campaign payload, got errors: {errors}",
        )

    def test_sovereign_level_accepted_rev_hp8(self):
        """REV-hp8: Schema should accept sovereign-tier levels (25+)."""
        game_state = {
            "world_data": {
                "world_time": {
                    "day": 1,
                    "hour": 12,
                    "minute": 0,
                    "second": 0,
                    "microsecond": 0,
                    "time_of_day": "noon",
                },
                "current_location": "Throne of Eternity",
            },
            "player_character_data": {
                "name": "Sovereign Ruler",
                "level": 25,  # Sovereign tier
                "hp_current": 500,
                "hp_max": 500,
                "xp": 610000,
            },
            "narrative": "You rule from the eternal throne.",
        }

        errors = self._validate_with_migration(game_state)
        self.assertEqual(
            errors,
            [],
            f"Schema validation should accept level 25 (sovereign tier), got errors: {errors}",
        )

    def test_all_title_case_variants_accepted_rev_6zg(self):
        """REV-6zg: Test all Title Case time_of_day variants from existing campaigns."""
        title_case_variants = [
            "Dawn",
            "Morning",
            "Midday",
            "Afternoon",
            "Evening",
            "Night",
            "Deep Night",
            "Midnight",
            "Noon",
            "Day",
            "Dusk",
        ]

        for time_of_day in title_case_variants:
            with self.subTest(time_of_day=time_of_day):
                game_state = {
                    "world_data": {
                        "world_time": {
                            "day": 1,
                            "hour": 12,
                            "minute": 0,
                            "second": 0,
                            "microsecond": 0,
                            "time_of_day": time_of_day,
                        },
                        "current_location": "Test Location",
                    },
                    "player_character_data": {
                        "name": "Test Hero",
                        "level": 5,
                        "hp_current": 50,
                        "hp_max": 50,
                    },
                    "narrative": f"It is {time_of_day}.",
                }

                errors = self._validate_with_migration(game_state)
                self.assertEqual(
                    errors,
                    [],
                    f"Schema should accept Title Case '{time_of_day}', got errors: {errors}",
                )

    def test_legacy_npc_status_string_accepted(self):
        """Backward compatibility: legacy NPC status strings should validate.

        testing_mcp seed data and existing campaigns use statuses like "healthy".
        Schema validation enforcement must not reject those payloads.
        """
        game_state = {
            "world_data": {
                "world_time": {
                    "day": 1,
                    "hour": 12,
                    "minute": 0,
                    "second": 0,
                    "microsecond": 0,
                    "time_of_day": "noon",
                },
                "current_location": "Test Arena",
            },
            "player_character_data": {
                "name": "Aric",
                "level": 1,
                "hp_current": 12,
                "hp_max": 12,
            },
            "npc_data": {
                "npc_goblin_001": {
                    "name": "Goblin",
                    "hp_current": 7,
                    "hp_max": 7,
                    "status": "healthy",
                }
            },
            "narrative": "A goblin watches from the shadows.",
        }

        errors = self._validate_with_migration(game_state)
        self.assertEqual(
            errors,
            [],
            f"Schema should accept legacy npc status 'healthy', got errors: {errors}",
        )


if __name__ == "__main__":
    unittest.main()
