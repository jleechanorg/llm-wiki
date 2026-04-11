---
title: "PR #68: [agento][bd-u8p] Enforce gh pr merge guardrail in agent hooks/wrappers"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-68.md
sources: []
last_updated: 2026-03-23
---

## Summary
Agents (Claude Code, Cursor, etc.) were able to run `gh pr merge` despite CLAUDE.md and workflow rules prohibiting it. Prompt-based rules are advisory — this enforces the policy in code as a hard guardrail.

## Metadata
- **PR**: #68
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +80/-17 in 3 files
- **Labels**: none

## Connections
