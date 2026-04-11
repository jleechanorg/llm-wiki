---
title: "PR #277: [agento] chore: add pre-push merge-conflict check and CR resolution workflow to CLAUDE.md"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-277.md
sources: []
last_updated: 2026-03-29
---

## Summary
PRs 263/266/267/273/276 are blocked at 5-6/7 green conditions due to three systemic failure patterns: (1) workers pushed to PRs with merge conflicts (dirty), (2) CR CHANGES_REQUESTED resolution without using the existing `extract-unresolved-comments.sh` and `cr-loop-guard.sh` scripts, (3) skeptic VERDICT: SKIPPED not guarded in the `approved-and-green` reaction.

## Metadata
- **PR**: #277
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +26/-0 in 1 files
- **Labels**: none

## Connections
