---
title: "Campaign Coherence"
type: concept
tags: ["game-design", "validation", "dnd", "state-management"]
sources: ["llm_wiki-raw-secondo_campaign_analysis_iteration_005.md-9798155f"]
last_updated: 2026-04-07
---

The property of a game campaign (especially D&D/faction campaigns) maintaining consistent internal state across all turns. Coherence violations include:

## Coherence Categories

1. **Timestamp Progression** — Time must always move forward; never backward
2. **Gold Calculations** — Faction treasury must match explicit transactions
3. **Level Progression** — Levels must increment incrementally (1→2→3), never skip
4. **Tutorial Messaging** — Clear phase indicators, never ambiguous completion language
5. **State Consistency** — All game state (inventory, NPCs, locations) must remain consistent

## Validation Methods

- **Multi-model analysis** — Run through multiple LLMs and compare (see [[Second Opinion Workflow]])
- **Automated sanity checks** — Script to verify timestamp monotonicity, recompute gold
- **Manual audit** — Scene-by-scene review of consistency categories

## Related Concepts

- [[TimestampTracking]] — tracking time across campaign turns
- [[GoldCalculation]] — proper handling of faction vs. personal gold
- [[LevelProgression]] — incremental level-up rules
- [[FactionCampaigns]] — campaigns with multiple NPC factions