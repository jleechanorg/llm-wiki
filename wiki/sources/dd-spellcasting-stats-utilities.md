---
title: "D&D 5e Spellcasting and Stats Utilities"
type: source
tags: [dnd-5e, game-mechanics, python, utility, spellcasting, worldarchitect]
source_file: "raw/dd-spellcasting-stats-utilities.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python utility module providing shared stats and spells display functions used by both the GET /api/campaigns/{id}/stats endpoint and the scripts/fetch_campaign_gamestate.py CLI tool. Ensures consistent output between API and CLI interfaces.

## Key Claims
- **Consistent Output**: Single source of truth for stats calculations across API and CLI
- **Spellcasting Ability Mapping**: Maps all D&D 5e classes and subclasses to INT/WIS/CHA spellcasting ability
- **Multi-class Support**: Handles multi-class characters by using first spellcasting class
- **Fallback Detection**: Infers spellcasting ability from character data (spell slots, spells known)

## Key Code Patterns
```python
SPELLCASTING_ABILITY_MAP = {
    "wizard": "int",
    "cleric": "wis",
    "sorcerer": "cha",
    # ... full mapping
}

def calc_modifier(score: int) -> int:
    return (score - 10) // 2

def get_proficiency_bonus(level: int) -> int:
    return PROFICIENCY_BY_LEVEL.get(level, 2)
```

## Connections
- [[DND5eMechanics]] — underlying D&D 5e rules system
- [[CampaignStatsAPI]] — API endpoint consuming these utilities
- [[FetchCampaignGamestate]] — CLI tool using same utilities
- [[CharacterSheet]] — player character data format

## Contradictions
- None identified
