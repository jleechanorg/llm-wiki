---
title: "Campaign Prompt Building Utilities"
type: source
tags: [utility, campaign, prompt-building, dnd-5e, world-logic]
source_file: "raw/mvp_site_all/campaign_prompt_builder.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Pure utility module for campaign prompt building, shared between world_logic.py and tests. Extracted to avoid circular dependencies and code duplication. Provides field formatting functions and random D&D 5e character/setting generation.

## Key Claims
- **Code Deduplication** — Extracted from world_logic.py to avoid import-unsafe dependencies
- **Random Campaign Generation** — Provides 10 D&D 5e character archetypes and 10 setting descriptions for fallback prompts
- **Field Conversion** — Converts literal escape sequences (\\n, \\t) to actual characters before formatting
- **Backward Compatibility** — Exports `_build_campaign_prompt_impl` alias for existing world_logic.py imports

## Key Functions
| Function | Purpose |
|----------|--------|
| `_convert_and_format_field` | Format field with escape sequence conversion |
| `_build_campaign_prompt` | Build campaign prompt from components |
| `_build_campaign_prompt_impl` | Backwards compatibility alias |

## Random Content Constants
**Characters**: warrior, rogue, wizard, paladin, ranger, bard, cleric, barbarian, monk, druid

**Settings**: Waterdeep, Feywild, Underdark, Icewind Dale, Calimshan, Sword Coast, Barovia, Sharn, Chult, Cyre

## Connections
- [[logging_util]] — Uses logging_util.info for random campaign generation feedback
- [[Game Mechanics Protocol]] — Aligns with D&D 5e character archetypes and settings
