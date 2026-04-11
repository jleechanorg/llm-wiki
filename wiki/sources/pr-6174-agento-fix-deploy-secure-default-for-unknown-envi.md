---
title: "PR #6174: [agento] fix(deploy): secure default for unknown environments and add preview case"
type: source
tags: []
date: 2026-04-10
source_file: raw/prs-worldarchitect-ai/pr-6174.md
sources: []
last_updated: 2026-04-10
---

## Summary
- Add `else` clause to set `PRODUCTION_MODE=true` for any `ENVIRONMENT` value not explicitly matching dev/preview/staging/stable, preventing silent auth bypass for unknown environments
- Explicitly add `preview` to the CI smoke test bypass case alongside `dev`

## Metadata
- **PR**: #6174
- **Merged**: 2026-04-10
- **Author**: jleechan2015
- **Stats**: +48/-21 in 5 files
- **Labels**: none

## Connections
