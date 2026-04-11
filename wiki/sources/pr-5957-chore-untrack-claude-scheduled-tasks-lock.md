---
title: "PR #5957: chore: untrack .claude/scheduled_tasks.lock"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldarchitect-ai/pr-5957.md
sources: []
last_updated: 2026-03-14
---

## Summary
- `.claude/scheduled_tasks.lock` is already listed in `.gitignore` (line 99, added in commit `884a4c692`)
- However it was previously committed, so git still tracks it despite the gitignore entry
- `git rm --cached` removes it from tracking without deleting the local file

## Metadata
- **PR**: #5957
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +0/-1 in 1 files
- **Labels**: none

## Connections
