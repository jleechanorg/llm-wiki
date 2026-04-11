---
title: "PR #3126: fix(agents): Support mode='god' parameter in get_agent_for_input"
type: source
tags: []
date: 2026-01-05
source_file: raw/prs-worldarchitect-ai/pr-3126.md
sources: []
last_updated: 2026-01-05
---

## Summary
- **Fixed:** `get_agent_for_input()` now honors `mode='god'` parameter from UI, not just "GOD MODE:" text prefix
- **Root Cause:** Agent selection only checked text prefix, ignoring mode parameter passed from UI dropdown
- **Impact:** Users switching to god mode via UI now correctly route to `GodModeAgent`

## Metadata
- **PR**: #3126
- **Merged**: 2026-01-05
- **Author**: jleechan2015
- **Stats**: +411/-83 in 14 files
- **Labels**: none

## Connections
