---
title: "Faction Settings Persistence End-to-End Tests"
type: source
tags: [python, testing, settings, persistence, e2e, faction-minigame, bugfix]
source_file: "raw/test_faction_settings_persistence_end2end.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end tests verifying that faction_minigame_enabled and other previously broken settings persist correctly through a complete save → retrieve → verify round-trip flow. Tests validate the fix for Bug #1 where faction_minigame_enabled was silently dropped from settings updates.

## Key Claims
- **Bug #1**: faction_minigame_enabled was silently dropped because update_user_settings_unified() had no validation block for it
- **Settings Tested**: faction_minigame_enabled, spicy_mode, auto_save, theme
- **Test Pattern**: Round-trip validation (save → retrieve → verify)
- **Test Infrastructure**: Uses FakeFirestoreClient instead of mocking firestore_service functions

## Key Quotes
> "This test validates the fix for Bug #1 where faction_minigame_enabled was silently dropped because it had no validation block in update_user_settings_unified()."

## Connections
- [[FactionCombatPowerCalculationTests]] — related faction settings tests
- [[FactionRankingCalculationTests]] — faction ranking system
- [[DebugModeEnd2EndTests]] — similar settings persistence pattern

## Contradictions
- None identified
