---
title: "PR #32: test: testing_mcp improvements — filter fix, companion ticks, faction endpoint, strong assertions"
type: source
tags: []
date: 2026-03-02
source_file: raw/prs-worldai_claw/pr-32.md
sources: []
last_updated: 2026-03-02
---

## Summary
- **wc-6aa**: Renamed 4 tests whose names contained `turn`/`returns` as substrings, silently excluded by `-k "not ... turn ..."` filter
- **wc-c58**: Living world tests now use campaign-linked sessions; `world_events` field asserted every turn
- **wc-1m1**: Added `test_catchup_companion_action_payload` — verifies EXPLORER companion generates tick actions
- **wc-h8g**: Added `GET /campaigns/:id/factions` endpoint to app.ts; test asserts nested faction structure (`identity.{id,name,tier}`, `capabi

## Metadata
- **PR**: #32
- **Merged**: 2026-03-02
- **Author**: jleechan2015
- **Stats**: +611/-51 in 8 files
- **Labels**: none

## Connections
