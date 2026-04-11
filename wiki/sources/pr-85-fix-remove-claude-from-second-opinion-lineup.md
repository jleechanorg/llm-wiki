---
title: "PR #85: fix: remove claude from second opinion lineup"
type: source
tags: [codex]
date: 2025-09-29
source_file: raw/prs-/pr-85.md
sources: []
last_updated: 2025-09-29
---

## Summary
- drop Claude from the second opinion agent model definitions and default selections while keeping configurable providers intact
- streamline staggered secondary execution to reuse shared caller mappings without special casing
- update secondary model unit tests to reflect the Claude-free registry mocks

## Metadata
- **PR**: #85
- **Merged**: 2025-09-29
- **Author**: jleechan2015
- **Stats**: +153/-141 in 3 files
- **Labels**: codex

## Connections
