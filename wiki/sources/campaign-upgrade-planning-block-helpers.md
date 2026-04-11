---
title: "Campaign Upgrade Planning Block Helpers"
type: source
tags: [worldarchitect, game-state, planning-blocks, campaign-upgrade, choice-normalization]
source_file: "raw/campaign-upgrade-planning-block-helpers.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Server-side helpers for campaign upgrade planning blocks that normalize choice formats and enforce campaign upgrade choice injection when the CampaignUpgradeAgent is selected. Handles JSON parsing, choice ID collision resolution, and automatic choice injection for divine/multiverse ascension ceremonies.

## Key Claims
- **Choice Format Normalization**: Converts planning_block choices from dict format (key-value) to list format with unique IDs, preventing collision errors via retry logic (up to 1000 retries)
- **Server-Side Enforcement**: Injects minimal upgrade choice when LLM fails to provide one but CampaignUpgradeAgent mode is active
- **Upgrade Type Detection**: Queries `campaign_divine.get_pending_upgrade_type()` to determine if multiverse (Sovereign Ascension) or divine (Divine Ascension) upgrade is available
- **JSON Parsing Safety**: Gracefully handles malformed JSON, None values, and type coercion errors in planning_block data
- **Choice ID Generation**: Falls back to text-based ID generation (lowercase, spaces→underscores, 30-char max) when no ID provided

## Key Code Patterns
```python
def normalize_planning_block_choices(planning_block, *, log_prefix):
    # Converts dict-format to list-format choices
    # Handles string-valued choices, ID collision retries

def inject_campaign_upgrade_choice_if_needed(planning_block, game_state_dict, agent_mode):
    # Enforces upgrade choice when MODE_CAMPAIGN_UPGRADE active
    # Injects "Begin Sovereign Ascension" or "Begin Divine Ascension"
```

## Connections
- [[Campaign Divine/Multiverse Upgrade Detection Logic]] — upgrade type detection used here
- [[Game State]] — game_state_dict provides player data for upgrade eligibility

## Contradictions
- None identified
