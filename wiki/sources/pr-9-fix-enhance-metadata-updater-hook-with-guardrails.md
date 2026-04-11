---
title: "PR #9: fix: enhance metadata-updater hook with guardrails and parsing"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-/pr-9.md
sources: []
last_updated: 2026-04-03
---

## Summary
- Add hook_event detection to distinguish PreToolUse vs PostToolUse hooks
- Strip leading cd and env variable prefixes from commands
- Add [agento] prefix guardrail on gh pr create titles
- Add gh pr merge guardrail to block agent-triggered merges by default
- Fix sed escaping bug

🤖 Generated with Claude Code

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Adds enforcement that can deny `gh pr create`/`gh pr merge` executions and changes merge-detection parsing, which could block wo

## Metadata
- **PR**: #9
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +91/-27 in 3 files
- **Labels**: none

## Connections
