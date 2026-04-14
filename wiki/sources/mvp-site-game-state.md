---
title: "mvp_site — Game State (Core D&D 5e Mechanics)"
type: source
tags: [worldarchitect-ai, game-state, D&D-5e, XP-level, monotonicity, schema-migration]
date: 2026-04-14
source_file: raw/mvp_site_all/game_state.py
---

## Summary

Core game state management integrating D&D 5e mechanics: XP/level validation using official XP thresholds, time monotonicity checks to prevent temporal regressions, and schema migration for legacy campaign compatibility. The LLM focuses on narrative; code handles all mathematical operations.

## Key Claims

### XP → Level Mapping (D&D 5e Official Thresholds)
| Level | XP Threshold |
|-------|-------------|
| 1→2 | 300 |
| 2→3 | 900 |
| 3→4 | 2,700 |
| ... | ... |

### Schema Migration
- `SCHEMA_MIGRATION_VERSION = 1` — legacy campaigns migrated once, then strict validation enforced
- Migration fields: `schema_migration_version`, `schema_migrated_at`
- Seed-based legacy session ID generation for stable migration identity

### Time Monotonicity
- `validate_xp_level(strict=False)` — auto-corrects `stored_level > expected_level`
- Validator **always wins** over canonicalizer in same persistence path (see [[LevelUpBug]] chain)
- `_canonicalize_level_from_xp_in_place` → then `validate_and_correct_state` in same path

### Core Integration
- Imports from `campaign_divine.py`: tier detection (mortal→divine→sovereign), stat modifiers, upgrade type
- Uses `dice.execute_dice_tool` for all dice rolls
- Faction tool execution via `execute_faction_tool`
- Pydantic schema validation via `validate_game_state`

## Connections

- [[LevelUpBug]] — canonicalizer self-undo pattern documented here
- [[CampaignTier]] — mortal/divine/sovereign upgrade system
- [[mvp-site-campaign-divine]] — upgrade detection logic
- [[mvp-site-dice]] — dice integration
- [[SocialHP]] — social encounter HP system integrated into game state
- [[SchemaMigration]] — legacy campaign compatibility
