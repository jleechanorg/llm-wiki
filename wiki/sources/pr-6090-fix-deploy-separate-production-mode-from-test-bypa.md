---
title: "PR #6090: fix(deploy): separate PRODUCTION_MODE from test bypass flags"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldarchitect-ai/pr-6090.md
sources: []
last_updated: 2026-04-04
---

## Summary
The dev deployment was failing because  set  for ALL environments and then added / for dev/preview. This is a fatal combo -  raises  when  AND any bypass flag is set.

## Metadata
- **PR**: #6090
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +203/-8 in 3 files
- **Labels**: none

## Connections
