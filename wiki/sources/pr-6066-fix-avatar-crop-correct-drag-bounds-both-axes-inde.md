---
title: "PR #6066: fix(avatar-crop): correct drag bounds — both axes independently draggable"
type: source
tags: []
date: 2026-04-01
source_file: raw/prs-worldarchitect-ai/pr-6066.md
sources: []
last_updated: 2026-04-01
---

## Summary
- Fix avatar drag-to-reposition so both horizontal and vertical axes are independently draggable regardless of image aspect ratio
- Root cause: `Math.min(0, ...)` as upper bound locked one axis to zero

## Metadata
- **PR**: #6066
- **Merged**: 2026-04-01
- **Author**: jleechan2015
- **Stats**: +2/-2 in 1 files
- **Labels**: none

## Connections
