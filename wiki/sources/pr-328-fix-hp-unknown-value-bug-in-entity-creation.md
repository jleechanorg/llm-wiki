---
title: "PR #328: Fix HP unknown value bug in entity creation"
type: source
tags: []
date: 2025-07-06
source_file: raw/prs-worldarchitect-ai/pr-328.md
sources: []
last_updated: 2025-07-06
---

## Summary
- Fix ValueError when HP field contains 'unknown' instead of numeric value during entity creation
- Add defensive parsing in HealthStatus.__init__ to handle non-numeric HP values
- Set reasonable defaults for 'unknown' or invalid HP values

## Metadata
- **PR**: #328
- **Merged**: 2025-07-06
- **Author**: jleechan2015
- **Stats**: +1067/-73 in 10 files
- **Labels**: none

## Connections
