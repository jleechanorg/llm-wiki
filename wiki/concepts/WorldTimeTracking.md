---
title: "World Time Tracking"
type: concept
tags: [game-state, time, world-data]
sources: [preventive-guards-unit-tests]
last_updated: 2026-04-08
---

## Description
System for maintaining temporal state in the game world through world_data.world_time with fields: hour (0-23), minute (0-59), time_of_day (morning/afternoon/evening/night/midday).

## Fallback Behavior
When world_time is missing from state, defaults to midday (hour=12, minute=0, time_of_day="midday") rather than leaving undefined.

## Preservation
World time is preserved across turns unless explicitly updated by the LLM. Tests verify that time data survives through enforce_preventive_guards even when the model doesn't emit it.

## Related
- [[PreventiveGuards]] manages time fallback and preservation
- [[LocationTracking]] is another state preservation mechanism
