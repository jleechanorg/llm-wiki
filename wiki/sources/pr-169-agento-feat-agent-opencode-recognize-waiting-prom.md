---
title: "PR #169: [agento] feat(agent-opencode): recognize waiting prompts in detectActivity"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-169.md
sources: []
last_updated: 2026-03-25
---

## Summary
OpenCode emits specific UI patterns when waiting for user input (press Enter, `[y/n]` prompts, menus, question marks). The `detectActivity()` method in `agent-opencode` was returning `"active"` for all non-empty output, losing this signal.

## Metadata
- **PR**: #169
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +92/-1 in 2 files
- **Labels**: none

## Connections
