---
title: "PR #22: fix: prevent JSON leak and generic fallback choices"
type: source
tags: []
date: 2026-02-26
source_file: raw/prs-worldai_claw/pr-22.md
sources: []
last_updated: 2026-02-26
---

## Summary
- **claw-477**: Strip embedded JSON blocks from scene_text even when JSON parsing succeeds, preventing mixed-JSON turn outputs from leaking raw JSON into player-facing text
- **claw-g03**: Fix parseTurnResult to use proper choice coercion (`_coerceChoiceList` + `_isGenericChoiceFallback`) instead of `||` operator which incorrectly treats empty arrays as falsy
- **Evidence**: Add backend provenance (PID, port, cmdline) to methodology.md for better reproducibility

## Metadata
- **PR**: #22
- **Merged**: 2026-02-26
- **Author**: jleechan2015
- **Stats**: +137/-6 in 4 files
- **Labels**: none

## Connections
