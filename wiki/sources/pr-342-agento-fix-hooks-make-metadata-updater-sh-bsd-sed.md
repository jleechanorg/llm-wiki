---
title: "PR #342: [agento] fix(hooks): make metadata-updater.sh BSD-sed compatible + remove git show-ref guard"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldai_claw/pr-342.md
sources: []
last_updated: 2026-04-02
---

## Summary
The `metadata-updater.sh` PostToolUse/PreToolUse hook runs on every Bash invocation in Claude Code sessions. Five bugs prevent it from working correctly in AO worktrees on macOS (BSD sed) and in non-git contexts.

## Metadata
- **PR**: #342
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +16/-17 in 1 files
- **Labels**: none

## Connections
