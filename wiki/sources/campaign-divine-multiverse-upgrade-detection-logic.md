---
title: "Campaign Divine/Multiverse Upgrade Detection Logic"
type: source
tags: [worldarchitect, game-state, upgrade-detection, campaign-tiers, divine-potential, multiverse]
source_file: "raw/campaign-divine-multiverse-upgrade-detection-logic.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Extracted upgrade detection logic from game_state.py that determines when players can upgrade their campaign tier: mortal → divine → sovereign. Uses thresholds for divine potential, level, universe control, and narrative milestone flags.

## Key Claims
- **Three Campaign Tiers**: mortal (default), divine, and sovereign — each represents the player's cosmic scale
- **Divine Upgrade Triggers**: divine_potential >= 100, level >= 25, OR narrative milestone flag set
- **Multiverse Upgrade Triggers**: universe_control >= 70 OR narrative milestone flag set
- **Type Coercion Safety**: Uses coerce_int_safe to handle Firestore-persisted string values
- **Firestore Null Guard**: Guards against null player_character_data with isinstance check

## Key Functions
- `get_campaign_tier()` — returns current tier constant
- `is_divine_upgrade_available()` — checks mortal→divine eligibility
- `is_multiverse_upgrade_available()` — checks any→sovereign eligibility
- `is_campaign_upgrade_available()` — union check for any upgrade
- `get_pending_upgrade_type()` — returns "divine", "multiverse", or None

## Connections
- [[GameState]] — the source module this was extracted from
- [[FirestorePersistence]] — why null guards exist (Firestore can persist nulls)
- [[NarrativeMilestones]] — sets upgrade flags via story progression

- [[CampaignTier]] — concept page for tier mechanics

## Contradictions
- []
