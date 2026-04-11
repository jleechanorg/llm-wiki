---
title: "PR #420: [agento] fix(scm-github): reset AO-managed files before dirty check"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldai_claw/pr-420.md
sources: []
last_updated: 2026-04-09
---

## Summary
- Fix execution order in `checkoutPR`: reset AO-managed files FIRST, then re-check dirty state
- Previously threw "uncommitted changes" BEFORE reaching the reset loop when AGENTS.md (or any non-`AO_MANAGED` file) was dirty
- Also adds missing third git status mock in existing test
- Handles staged-only changes (idx='M', wt=' ') via `git reset HEAD` + `git checkout`

Supersedes #417 for the checkoutPR fix. PR #417 covers reviewDecision normalization (separate area of scm-github/index.ts).

## Metadata
- **PR**: #420
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +86/-33 in 2 files
- **Labels**: none

## Connections
