---
title: "Sariel Campaign Integration Test - Execution Summary"
type: source
tags: [testing, integration-test, sariel, entity-tracking, field-validation]
source_file: "raw/sariel-campaign-integration-test-execution.md"
sources: [sariel-test-files-analysis, sariel-campaign-replay-desync-measurement]
last_updated: 2026-04-08
---

## Summary
Comprehensive integration test validating 580+ fields across 10 campaign interactions. Tests entity tracking accuracy including the Cassian Problem edge case, location-based entity inference, and game state consistency. Requires Gemini API key for execution.

## Key Claims
- **580+ Fields Validated** — game state (70), player character (200+), NPC (240+), entity tracking (70)
- **10 Interaction Test Sequence** — from initial campaign creation through full replay
- **Cassian Problem Edge Case** — tests entity reference handling when referenced NPC is not present in current scene
- **Location-Based Entity Inference** — validates context-aware NPC presence (Valerius in study, Lady Cressida in chambers)
- **Test Execution** — requires GEMINI_API_KEY, runs via Flask test client with TESTING_AUTH_BYPASS

## Field Validation Breakdown

### Game State Fields (70 total)
- game_state_version, player_character_data, world_data
- npc_data, custom_campaign_state, combat_state
- last_state_update_timestamp

### Player Character Fields (200+ total)
- Basic: name, class, level, race
- Vitals: hp_current, hp_max
- Stats: STR, DEX, CON, INT, WIS, CHA (6 fields)
- Resources: gold, experience
- Equipment: inventory, equipment, spells
- Status: conditions, backstory

### NPC Fields (240+ total)
- name, type, faction, hp_current, hp_max
- location, status, relationship

### Entity Tracking Fields (70 total)
- interaction number, player input, location
- expected entities, found entities, missing entities
- success status

## Special Test Cases

### The Cassian Problem (Interaction #2)
Player says: "ask for forgiveness. tell cassian i was scared and helpless"
Tests whether system correctly tracks Cassian even when not physically present in the scene.

### Location-Based Entity Tracking
- Valerius's Study → expects Valerius present
- Lady Cressida's Chambers → expects Lady Cressida
Tests contextual entity inference from location context.

## Test Execution
```bash
TESTING_AUTH_BYPASS=true vpython mvp_site/test_sariel_campaign_integration.py
```

Results saved to `sariel_integration_test_results.json` for post-run analysis.

## Connections
- [[SarielTestFilesAnalysis]] — documents original test file complexity
- [[SarielCampaignReplayDesyncMeasurement]] — measures entity tracking desync
- [[IntegrationTestsWithRealAPICalls]] — real API test infrastructure
- [[Cassian]] — edge case for entity reference handling
- [[EntityTracking]] — core concept being tested

## Contradictions
- None identified — this test validates the entity tracking system rather than challenging it
