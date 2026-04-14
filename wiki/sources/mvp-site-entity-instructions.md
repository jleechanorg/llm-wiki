---
title: "mvp_site entity_instructions"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/entity_instructions.py
---

## Summary
Consolidated module for entity tracking and preloading to prevent entity disappearing in AI narratives. Implements multiple mitigation strategies: EntityInstructionGenerator (Option 5), EntityPreloader (Option 3), and LocationEntityEnforcer. Generates explicit AI instructions requiring entity mentions and presence.

## Key Claims
- EntityInstructionGenerator creates mandatory/conditional/background instructions for different entity types (player_character, npc_referenced, location_npc, story_critical)
- EntityPreloader generates entity manifest text to inject into AI prompts ensuring all active entities are explicitly mentioned
- EntityValidator validates AI output for missing entities and implements retry logic
- LocationEntityEnforcer ensures location-appropriate NPCs are included in scenes

## Connections
- [[EntityTracking]] — SceneManifest and create_from_game_state imported for entity manifest generation
- [[GameState]] — uses game_state to generate entity manifests for each turn
- [[Validation]] — EntityValidator provides entity presence validation with retry suggestions