---
title: "PR #4859: fix(dice): resolve false-positive fabrication detection and prompt leakage"
type: source
tags: []
date: 2026-02-05
source_file: raw/prs-worldarchitect-ai/pr-4859.md
sources: []
last_updated: 2026-02-05
---

## Summary
- Fix false-positive fabrication detection when Gemini uses tool_requests fallback path with real server-side RNG
- Remove dice tool names from code_execution variant prompts to prevent teaching model the tool_requests vocabulary
- Add 5 TDD tests covering both fixes

**Key themes:**
- Dice integrity accuracy (eliminating false positives)
- Prompt engineering discipline (do not name tools in prohibitions)

## Metadata
- **PR**: #4859
- **Merged**: 2026-02-05
- **Author**: jleechan2015
- **Stats**: +263/-41 in 9 files
- **Labels**: none

## Connections
