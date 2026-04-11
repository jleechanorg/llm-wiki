---
title: "PR #157: chore: remove PreToolUse merge policy enforcement from metadata-updater hook"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-157.md
sources: []
last_updated: 2026-03-24
---

## Summary
- Removes PreToolUse `gh pr merge` enforcement block from `.claude/metadata-updater.sh`
- Hook now operates exclusively as a PostToolUse metadata updater (tracks `gh pr create`, `git checkout -b`, `gh pr merge`)
- The PreToolUse deny was redundant with `agentRules` ("NEVER MERGE") and caused confusion with bypassPermissions mode

## Metadata
- **PR**: #157
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +8/-15 in 1 files
- **Labels**: none

## Connections
