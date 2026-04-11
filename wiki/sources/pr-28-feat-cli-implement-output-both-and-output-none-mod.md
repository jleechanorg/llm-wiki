---
title: "PR #28: feat(cli): implement --output=both and --output=none modes for branch-entry"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-/pr-28.md
sources: []
last_updated: 2026-03-29
---

## Summary
The `blog-cli branch-entry` command had a `--output` flag with three documented values (`file`, `both`, `none`) but only `file` was implemented. The design doc (Section B) specifies:

| Mode | Write file | POST to MCP |
|---|---|---|
| `file` (default) | ✅ | ❌ |
| `both` | ✅ | ✅ (best-effort) |
| `none` | ❌ | ❌ |

This PR wires up the missing modes.

## Metadata
- **PR**: #28
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +208/-6 in 2 files
- **Labels**: none

## Connections
