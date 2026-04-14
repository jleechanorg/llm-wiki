---
title: "show_sariel_test_summary.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Utility script that displays a summary of what the Sariel campaign integration test validates. Shows the field validation coverage and test scenarios.

## Key Claims
- Loads prompts from `sariel_campaign_prompts.json`
- Displays 7 game state top-level fields, up to 20 player character fields, 8+ NPC fields per entity, and 7 entity tracking fields
- Estimates ~450+ fields validated across 10 interactions
- Key test scenarios include: initial campaign setup, "Cassian Problem" (entity reference handling), location changes, NPC interactions

## Key Quotes
> "This comprehensive test ensures the game state remains consistent and all entities are properly tracked throughout a real campaign."

## Connections
- [[test_sariel_campaign_integration]] — the actual test this summarizes
- [[capture]] — provides the captured responses used for validation