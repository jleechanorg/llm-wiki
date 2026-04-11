---
title: "PR #364: Tighten MessageItem logging guards"
type: source
tags: [codex]
date: 2025-12-12
source_file: raw/prs-/pr-364.md
sources: []
last_updated: 2025-12-12
---

## Summary
- avoid relying on process.env in MessageItem and gate timestamp warnings to dev-only non-test runs
- remove the synthesis debug log so assistant rendering no longer emits console noise

## Metadata
- **PR**: #364
- **Merged**: 2025-12-12
- **Author**: jleechan2015
- **Stats**: +3/-6 in 1 files
- **Labels**: codex

## Connections
