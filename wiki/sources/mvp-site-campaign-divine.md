---
title: "Campaign Divine Upgrade Detection"
type: source
tags: [campaign-tiers, divine-upgrade, multiverse, ascension]
sources: []
last_updated: 2026-04-14
---

## Summary

Extracted upgrade detection logic for campaign tier system (mortal -> divine -> sovereign). Handles divine upgrade triggers (divine_potential >= 100 OR level >= 25) and multiverse upgrade triggers (universe_control >= 70). Also provides helper functions for stat modifier calculation used in God Power conversion.

## Key Claims

- **Three Campaign Tiers**: Mortal, Divine, Sovereign (via constants.CAMPAIGN_TIER_*)
- **Divine Upgrade Triggers**: Explicit flag OR (divine_potential >= 100 AND level >= 25)
- **Multiverse Upgrade Triggers**: Explicit flag OR universe_control >= 70
- **Numeric Coercion**: Uses `coerce_int_safe` to handle string values from Firestore persistence
- **Pending Upgrade Priority**: Multiverse takes priority over divine (can upgrade from any tier)
- **Highest Stat Modifier**: `get_highest_stat_modifier()` extracts modifier from player_character_data attributes for GP calculation

## Key Quotes

> "Get the current campaign tier (mortal, divine, or sovereign)"

> "Multiverse takes priority (can upgrade from any tier)"

> "Guard against non-dict player_character_data (Firestore can persist nulls)"

## Connections

- [[CampaignTier]] — tier system (mortal/divine/sovereign)
- [[DivineUpgrade]] — divine upgrade mechanics
- [[MultiverseUpgrade]] — multiverse upgrade mechanics
- [[GodPower]] — stat modifier used in GP conversion

## Contradictions

- None identified