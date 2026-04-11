---
title: "PR #290: [agento] fix: remove unsupported manifest fields from plugin.json"
type: source
tags: []
date: 2026-04-01
source_file: raw/prs-/pr-290.md
sources: []
last_updated: 2026-04-01
---

## Summary
- Removes only the `scripts` field from `.claude-plugin/plugin.json` (the only unsupported manifest key)
- `commands`, `agents`, and `skills` are valid schema fields and are preserved
- `.coderabbit.yaml` added to enable formal CR approval workflow

## Metadata
- **PR**: #290
- **Merged**: 2026-04-01
- **Author**: jleechan2015
- **Stats**: +13/-1 in 2 files
- **Labels**: none

## Connections
