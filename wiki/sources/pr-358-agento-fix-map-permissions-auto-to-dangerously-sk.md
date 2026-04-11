---
title: "PR #358: [agento] fix: map permissions=auto to --dangerously-skip-permissions"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldai_claw/pr-358.md
sources: []
last_updated: 2026-04-03
---

## Summary
- `normalizePermissionMode()` in agent-claude-code returned `undefined` for `permissions: "auto"`, so AO workers configured with `permissions: auto` never received `--dangerously-skip-permissions`
- This caused Claude Code to show approval dialogs even when `bypassPermissions` was intended
- Added `mode === "auto"` → `"permissionless"` mapping, same as `"skip"` already does

## Metadata
- **PR**: #358
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +35/-9 in 5 files
- **Labels**: none

## Connections
