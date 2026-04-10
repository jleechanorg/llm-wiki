---
title: "Field Validation"
type: concept
tags: [testing, validation, game-state, integration-test]
sources: [sariel-campaign-integration-test-expected-output, sariel-campaign-integration-test-execution]
last_updated: 2026-04-08
---

## Summary
The process of verifying that game state fields are correctly persisted and retrieved across campaign interactions. The integration test validates 5834 total fields across 10 interactions.

## Validation Scope
- **Player Character**: 15-18 fields (name, class, level, race, hp_current, hp_max, stats, inventory, gold, backstory)
- **NPCs**: 8 fields each (name, type, hp_current, hp_max, location)
- **World Data**: 5 entries
- **Combat State**: in_combat boolean

## Metrics
- **Total Fields**: 5834 across 10 interactions
- **Average per Interaction**: 583.4 fields

## Related Pages
- [[SarielCampaignIntegrationTestExpectedOutput]] — detailed field counts per interaction
- [[SarielCampaignIntegrationTestExecution]] — execution summary
