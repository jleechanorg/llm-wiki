---
title: "PR #516: [agento] fix(canary): add --prefix to npm ls so SDK version is detected correctly"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldai_claw/pr-516.md
sources: []
last_updated: 2026-04-05
---

## Summary
- Fix check 5 (SDK protocol version) in `staging-canary.sh` — `npm ls` was running from the worktree directory (no node_modules), returning empty and triggering the fail-closed error
- Add `--prefix ~/.openclaw` so `npm ls` resolves from the correct install location
- Also add `~/.openclaw` as a fallback path in the secondary node resolve
- Both staging (port 18810) and prod (port 18789) canaries now pass 9/9

## Metadata
- **PR**: #516
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +4/-3 in 1 files
- **Labels**: none

## Connections
