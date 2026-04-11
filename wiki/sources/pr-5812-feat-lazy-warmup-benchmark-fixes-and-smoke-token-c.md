---
title: "PR #5812: feat: lazy warmup, benchmark fixes, and SMOKE_TOKEN centralization"
type: source
tags: []
date: 2026-03-03
source_file: raw/prs-worldarchitect-ai/pr-5812.md
sources: []
last_updated: 2026-03-03
---

## Summary
- **Lazy startup warmup**: All lazy modules (`firestore_service`, `gemini_provider`, `llm_service`, `openclaw_provider`, `world_logic`) now preload inside `create_app()` before the first user request, eliminating the cold-request init penalty per worker
- **SMOKE_TOKEN centralization**: New composite action `.github/actions/run-mcp-smoke-tests/` is the single source of truth for `SMOKE_TOKEN → mcp-smoke-tests.mjs` env mapping; fixes auto-deploy smoke tests that were broken since Jan 31
- **Bench

## Metadata
- **PR**: #5812
- **Merged**: 2026-03-03
- **Author**: jleechan2015
- **Stats**: +887/-144 in 8 files
- **Labels**: none

## Connections
