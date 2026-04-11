---
title: "PR #215: [agento] fix: [agento] PR title prefix via PreToolUse hook"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-215.md
sources: []
last_updated: 2026-03-27
---

## Summary
Adds a PreToolUse guardrail in METADATA_UPDATER_SCRIPT that denies gh pr create titles not prefixed with [agento]. PostToolUse falls through to metadata tracking.

Fixes 4 bash-embedding bugs: `${'$'}` consumed `{` from following `${HOME}`, double-quoted BASH_REMATCH prevented array expansion, double-quoted AO_SESSION was literal, and `|| \` continuations broken in execSync stdin piping. All fixed with plain JS string concatenation.

## Metadata
- **PR**: #215
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +401/-137 in 5 files
- **Labels**: none

## Connections
