---
title: "PR #6200: fix(frontend): render debug_info.system_message in debug mode"
type: source
tags: [worldarchitect-ai, debug-info, frontend, system-message, pr-6200]
date: 2026-04-11
source_file: mvp_site/frontend_v1/app.js
---

## Summary
`debug_info.system_message` is captured from LLM responses starting with `[System Message:]` in `narrative_response_schema.py:3720-3733`, but was never rendered in the UI. Added rendering in the debug info panel when `debugMode` is enabled.

## Key Claims
- `system_message` field was being captured but never displayed
- Now shown alongside `agent_name`, `dm_notes`, and `state_rationale` in the debug info panel
- Low risk: UI-only change, no impact to core gameplay logic

## Files Changed
- `mvp_site/frontend_v1/app.js` (+5, -0)

## Testing
None (minor UI rendering fix)

## Connections
- Related to [[StructureDriftPattern]] — debug_info field was previously trapped inside rewards_box block (PRs #6197, #6204)
- Related PRs: #6197 (debug_info emitted on all turns), #6204 (hoist fields out of rewards_box)
