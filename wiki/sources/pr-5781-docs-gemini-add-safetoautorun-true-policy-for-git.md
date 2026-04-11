---
title: "PR #5781: docs(GEMINI): add SafeToAutoRun=true policy for git commit/push"
type: source
tags: []
date: 2026-02-26
source_file: raw/prs-worldarchitect-ai/pr-5781.md
sources: []
last_updated: 2026-02-26
---

## Summary
NEVER set `SafeToAutoRun=false` for `git commit` or `git push`. These are the most common cause of hung commands.

### Changes
- Added a **Safe-to-Auto-Run Commands** table under the Shell Command Safety section listing all git, gh CLI, and build/test commands that must always use `SafeToAutoRun=true`
- Added an `[!IMPORTANT]` callout explicitly prohibiting `SafeToAutoRun=false` for `git commit` and `git push`

### Rationale
A commit is local-only. A push has no destructive local side effects, a

## Metadata
- **PR**: #5781
- **Merged**: 2026-02-26
- **Author**: jleechan2015
- **Stats**: +13/-0 in 1 files
- **Labels**: none

## Connections
