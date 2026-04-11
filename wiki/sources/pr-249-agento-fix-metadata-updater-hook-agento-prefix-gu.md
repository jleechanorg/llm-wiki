---
title: "PR #249: [agento] fix: metadata-updater hook -- [agento] prefix guardrail + cmd parsing fixes"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-249.md
sources: []
last_updated: 2026-03-28
---

## Summary
The `.claude/metadata-updater.sh` PreToolUse/PostToolUse hook had several gaps:
1. No enforcement of the mandatory `[agento]` prefix on `gh pr create` titles (bd-pfx)
2. Command stripping didn't handle leading `FOO=bar` env assignment prefixes
3. `git checkout`/`git switch` patterns were combined in a way that could miss edge cases
4. `sed` character class `[&|\/]` incorrectly escaped `|` and `/` in BRE

## Metadata
- **PR**: #249
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +17/-8 in 1 files
- **Labels**: none

## Connections
