---
title: "PR #722: Fix secondo CLI auth path and stabilize token fallback"
type: source
tags: []
date: 2025-11-13
source_file: raw/prs-/pr-722.md
sources: []
last_updated: 2025-11-13
---

## Summary
- point the repo helper to the exported ~/.claude/scripts/secondo-cli.sh so the slash command stays in sync with worldarchitect updates automatically
- normalize DEFAULT_MAX_OUTPUT_TOKENS in backend/src/config/llmDefaults.ts so resolveSafeOutputLimit can’t yield undefined values when shared config emits bad data
- refreshed the Firebase token and captured new smoke runs for both the global CLI and repo wrapper, keeping evidence under /tmp/ai_universe/debug_single2/evidence

## Metadata
- **PR**: #722
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +20/-268 in 2 files
- **Labels**: none

## Connections
