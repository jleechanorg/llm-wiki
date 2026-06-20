---
title: "TestFactionSettingsEndToEnd"
type: entity
tags: [testing, unittest, settings, e2e]
sources: [faction-settings-endtoend-persistence-tests]
last_updated: 2026-04-08
---

Test class that verifies faction_minigame_enabled and other settings persist correctly through round-trip validation (save → retrieve → verify).

## Test Methods
- test_faction_minigame_enabled_roundtrip — validates True persists
- test_faction_minigame_enabled_false_roundtrip — validates False persists  
- test_spicy_mode_roundtrip — validates spicy_mode persists
- test_auto_save_roundtrip — validates auto_save persists
- test_theme_roundtrip — validates theme persists

## Related
- [FakeFirestoreClient](FakeFirestoreClient.md) — test infrastructure
- [End2EndBaseTestCase](End2EndBaseTestCase.md) — base test class
- [[FactionRankingCalculationTests]] — related faction tests
