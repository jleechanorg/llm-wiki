---
title: "PR #6138: Fix CharacterCreationAgent hijacking LevelUpAgent"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldarchitect-ai/pr-6138.md
sources: []
last_updated: 2026-04-07
---

## Summary
When a user clicks "Level Up Now", the system was assigning `character_creation_in_progress=True` as a legacy artifact. Because `CharacterCreationAgent` holds a higher precedence over `LevelUpAgent` in our routing layer, the user request gets hijacked into Character Creation processing rather than properly opening the Level Up procedure. This left the user seeing the generic Level Up Rewards box mapped to a Finish button rather than offering their proper planning block with selection choices.

## Metadata
- **PR**: #6138
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +2733/-16 in 6 files
- **Labels**: none

## Connections
