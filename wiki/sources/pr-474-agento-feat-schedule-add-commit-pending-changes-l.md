---
title: "PR #474: [agento] feat(schedule): add commit-pending-changes launchd job (every 30 min)"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldai_claw/pr-474.md
sources: []
last_updated: 2026-04-02
---

## Summary
Automated job that periodically checks `~/.openclaw` for uncommitted changes to git-tracked files, stages+commits them on a feature branch, and opens/updates a PR. Untracked files trigger a Slack warning but are never auto-added.

## Metadata
- **PR**: #474
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +846/-0 in 4 files
- **Labels**: none

## Connections
