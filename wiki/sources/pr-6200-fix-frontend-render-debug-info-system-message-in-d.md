---
title: "PR #6200: fix(frontend): render debug_info.system_message in debug mode"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6200.md
sources: []
last_updated: 2026-04-11
---

## Summary
- **Problem:** `debug_info.system_message` is captured from LLM responses starting with `[System Message:]` in `narrative_response_schema.py:3720-3733`, but was never rendered in the UI
- **Fix:** Added rendering for `debug_info.system_message` in the debug info section of `app.js` when `debugMode` is enabled

## Metadata
- **PR**: #6200
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +5/-0 in 1 files
- **Labels**: none

## Connections
