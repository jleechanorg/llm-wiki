---
title: "Run Sariel Replays"
type: source
tags: [testing, replay, entity-tracking, sariel, desync]
sources: [mvp-site-run-sariel-replays]
last_updated: 2025-01-15
---

## Summary

Runs 10 Sariel campaign replays to measure entity tracking desync rates. Analyzes how well the LLM tracks entities across conversation turns.

## Key Claims

- **10 campaign replays**: Runs Sariel campaign 10 times
- **Desync measurement**: Measures entity tracking inconsistency
- **Statistical output**: Reports desync rates across replays
- **Replay mode**: Uses captured LLM responses for consistent testing
- **Real service support**: Can run with real or mock providers

## Entity Tracking

Monitors desync in:
- Player character state
- Named NPCs
- Location awareness
- Faction relationships

## Connections

- [[mvp-site-run-real-sariel-capture]] - Capture script
- [[mvp-site-entity-tracking]] - Entity tracking implementation
- [[mvp-site-sariel-campaign]] - Sariel campaign source
