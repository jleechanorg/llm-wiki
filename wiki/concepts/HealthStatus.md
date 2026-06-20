---
title: "HealthStatus"
type: concept
tags: [schema, pydantic, hp, game-mechanic]
sources: []
last_updated: 2026-04-08
---

## Description
Pydantic model for tracking NPC health points. Contains hp (current) and hp_max (maximum) fields. Used in NPC creation to ensure characters have valid health state.

## Related
- [NPC](NPC.md) — uses HealthStatus for health tracking
- [Pydantic](Pydantic.md) — validation library providing schema enforcement
