---
title: "PR #6162: fix(world-logic): global time_events persistence and backfill hardening"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6162.md
sources: []
last_updated: 2026-04-09
---

## Summary
Global `time_events` and `faction_updates` were being incorrectly filtered out during scene changes because the logic treated them as scene-scoped. Additionally, sparse LLM payloads for `world_events` would clobber existing global markers during the backfill process.

## Metadata
- **PR**: #6162
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +396/-75 in 5 files
- **Labels**: none

## Connections
