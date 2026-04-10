---
title: "Faction Minigame Mandatory Suggestion"
type: concept
tags: [faction, minigame, worldarchitect]
sources: [game-state-management-protocol]
last_updated: 2026-04-08
---

Faction Minigame Mandatory Suggestion is a required protocol that forces suggestion of faction minigame activation based on army strength thresholds.

**Thresholds**:
- **Suggest at 100+ strength**: If `army_data.total_strength` >= 100 and `faction_minigame.enabled=false`, MUST suggest enabling
- **Strongly recommend at 500+**: If >= 500 and `enabled=false`, MUST strongly recommend

**Header Requirement**: When enabled, must include `faction_header` in root JSON

**Related Concepts**:
- [[FactionMinigameStateAccessUtilities]] — state extraction
- [[FactionArmyManagementSystem]] — management system
- [[FactionMinigameStateAccessUtilities]] — minigame state access
