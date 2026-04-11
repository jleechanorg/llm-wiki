---
title: "Entity Tracking Production Implementation Tests"
type: source
tags: [python, testing, entity-tracking, production, entity-id-format]
source_file: "raw/test_entity_tracking_production.py"
last_updated: 2026-04-08
---

## Summary
Test script validating entity tracking production implementation including entity ID format standardization, string ID preservation, and SceneManifest creation. Tests verify that entity IDs follow the `pc_name_001` format convention with proper prefix and numeric suffix.

## Key Claims
- **Entity ID Format**: Entity IDs follow underscore format like `pc_name_001` with prefixes (pc_, npc_, scene_) and 3-digit numeric suffix
- **Existing String ID Preservation**: Custom string_ids from game_state are preserved when valid
- **Invalid ID Regeneration**: Invalid string_ids with wrong prefix are regenerated with proper format (e.g., `faction_*` → `npc_*`)
- **SceneManifest Structure**: SceneManifest includes scene_id, session_number, turn_number, player_characters, npcs, and timestamp

## Key Test Cases
1. `test_entity_id_format_standardization` - Verifies PC IDs match `pc_[a-z_]+_\d{3}` and NPC IDs match `npc_[a-z_]+_\d{3}`
2. `test_existing_string_ids_preserved` - Verifies custom string_ids like `pc_custom_hero_999` are preserved
3. `test_invalid_string_ids_regenerated` - Verifies invalid prefixes are regenerated with correct format
4. `test_scene_manifest_creation` - Verifies SceneManifest creation from game state

## Technical Details
- Uses regex validation: `re.search(r"^pc_[a-z_]+_\d{3}$", pc.entity_id)`
- Tests NPC presence filtering (hidden NPCs excluded from expected entities)
- Validates HP display format: "HP: 25/30" (current/max)
- Session/turn tracking: scene_s1_t5 format

## Connections
- [[EntityTracking]] — production implementation being tested
- [[EntityIDFormat]] — the format standardization pattern
- [[SceneManifest]] — data structure created from game state

## Contradictions
- None identified
