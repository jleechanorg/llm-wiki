---
title: "mvp_site world_time"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/world_time.py
---

## Summary
Temporal management utilities for WorldArchitect.AI. Provides calendar normalization mapping for multiple D&D/Fantasy calendars (Forgotten Realms, Greyhawk) to standard 1-12 months.

## Key Claims
- MONTH_MAP normalizes calendar names to 1-12 (hammer→1, alturiak→2, etc.)
- Supports multiple calendars: Forgotten Realms (hammer, tarsakh), Greyhawk (harvester, thefitz), Eberron, Ravnica, custom
- Temporal comparison and formatting utilities

## Connections
- [[GameState]] — temporal/time management in game state
