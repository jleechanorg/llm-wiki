---
title: "PR #817: fix: address monitoring middleware metrics edge cases"
type: source
tags: [codex]
date: 2025-11-24
source_file: raw/prs-/pr-817.md
sources: []
last_updated: 2025-11-24
---

## Summary
- prevent double-counting in monitoring middleware and handle falsy/Buffer response bodies while still emitting inbound size metrics
- expand monitoring middleware tests to cover Buffer responses, falsy payloads, and correct sizing
- fix dashboard docs widget count and explicitly list deprecated metrics mappings

## Metadata
- **PR**: #817
- **Merged**: 2025-11-24
- **Author**: jleechan2015
- **Stats**: +71/-7 in 3 files
- **Labels**: codex

## Connections
