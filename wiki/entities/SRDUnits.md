---
title: "SRD Units Module"
type: entity
tags: [srd, units, faction, reference]
sources: [faction-tool-definitions-lambda]
last_updated: 2026-04-08
---

Standard Reference Units module (mvp_site.faction.srd_units) providing unit group creation and unit type definitions. Used across faction tools for soldier and elite unit handling.

## Unit Types
- elite_6, veteran, assassin — elite unit variants
- soldiers — base unit type
- fortifications — defensive structures (levels 0-3)

## Connections
- [[FactionToolDefinitions]] — used in battle and combat calculations
- [[FactionBattleSim]] — unit instantiation
