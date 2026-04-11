---
title: "PR #5499: Centralize MCP smoke suite execution"
type: source
tags: []
date: 2026-02-14
source_file: raw/prs-worldarchitect-ai/pr-5499.md
sources: []
last_updated: 2026-02-14
---

## Summary
- **Centralize smoke test execution** - GitHub Actions and local scripts now invoke canonical `testing_mcp/test_smoke.py` suite for both mock and real modes, eliminating test duplication
- **Fix 7 critical invariant and state management bugs** - Combat state staleness, character updates overwriting enriched state, filtered invariant failures, world_events schema enforcement
- **Strengthen mock mode determinism** - Rich mock payloads with dice mechanics, world_events, action_resolution, and game_

## Metadata
- **PR**: #5499
- **Merged**: 2026-02-14
- **Author**: jleechan2015
- **Stats**: +2267/-1472 in 27 files
- **Labels**: none

## Connections
