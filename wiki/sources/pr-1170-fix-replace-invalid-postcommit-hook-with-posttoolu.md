---
title: "PR #1170: fix: Replace invalid PostCommit hook with PostToolUse for git commits"
type: source
tags: []
date: 2025-08-04
source_file: raw/prs-worldarchitect-ai/pr-1170.md
sources: []
last_updated: 2025-08-04
---

## Summary
- Fix Claude CLI diagnostic error: PostCommit is not a valid hook type
- Replace PostCommit with PostToolUse using 'Bash(git commit*)' matcher to trigger after git commit operations
- Update all documentation and comments to reflect the correct hook type

## Metadata
- **PR**: #1170
- **Merged**: 2025-08-04
- **Author**: jleechan2015
- **Stats**: +32/-21 in 4 files
- **Labels**: none

## Connections
