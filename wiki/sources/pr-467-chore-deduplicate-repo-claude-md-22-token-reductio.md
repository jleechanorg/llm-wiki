---
title: "PR #467: chore: deduplicate repo CLAUDE.md (~22% token reduction)"
type: source
tags: []
date: 2026-04-01
source_file: raw/prs-worldai_claw/pr-467.md
sources: []
last_updated: 2026-04-01
---

## Summary
`~/.claude/CLAUDE.md` (global, 43k chars) and the repo `CLAUDE.md` (was 36k chars) have significant overlap. Claude Code loads both, so duplicate sections waste context tokens and trigger the performance warning (`⚠Large CLAUDE.md will impact performance`).

## Metadata
- **PR**: #467
- **Merged**: 2026-04-01
- **Author**: jleechan2015
- **Stats**: +33/-209 in 1 files
- **Labels**: none

## Connections
