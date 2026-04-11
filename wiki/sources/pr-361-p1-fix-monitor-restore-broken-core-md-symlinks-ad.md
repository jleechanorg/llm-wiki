---
title: "PR #361: [P1] fix(monitor): restore broken core MD symlinks; add health check"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-361.md
sources: []
last_updated: 2026-03-23
---

## Summary
Core markdown policy files (SOUL.md, TOOLS.md, USER.md, IDENTITY.md, HEARTBEAT.md, AGENTS.md, MEMORY.md, BOOTSTRAP.md) were inaccessible in git worktrees because git symlinks in `workspace/` were committed with wrong targets (`workspace/FILENAME` instead of `FILENAME`), creating circular disk references. A spurious `workspace/workspace/` directory was also committed.

## Metadata
- **PR**: #361
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +913/-2 in 5 files
- **Labels**: none

## Connections
