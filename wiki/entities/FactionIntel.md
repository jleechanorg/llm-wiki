---
title: "Faction Intel Module"
type: entity
tags: [faction, intel, spy, operations]
sources: [faction-tool-definitions-lambda]
last_updated: 2026-04-08
---

Module in mvp_site.faction.intel that executes intel/spy operations against target factions. Returns success tier, detection status, intel gathered, and combat buffs.

## Usage
Called via faction_intel_operation tool with spies deployed, target's shadow networks, wards, and spymaster modifiers.

## Connections
- [[FactionToolDefinitions]] — exposed via tool definition
- [[FactionRankings]] — related faction operations
